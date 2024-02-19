import logging
import os 
import time 
import re 
from typing import Any, Dict, List, Optional, Sequence, Union
from uuid import UUID, uuid4 
from langchain.callbacks.base import BaseCallbackHandler 
from langchain_core.documents.base import Document 
from langfuse import Langfuse 
import asyncio
import stripe 

os.environ['OPENAI_API_KEY'] = "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"

from ragas.metrics import faithfulness, answer_relevancy, context_precision 
from ragas.metrics.critique import SUPPORTED_ASPECTS, harmfulness 


os.environ['LANGFUSE_PUBLIC_KEY'] = "pk-lf-875dade5-676c-4c9a-a826-bb45378e0706"
os.environ['LANGFUSE_SECRET_KEY'] = "sk-lf-80fe69a3-7170-4e72-9bee-9a0fd43f90ce"
stripe.api_key = 'sk_test_51OHcovDTU9hgRfhMraaWCNcAWRwv0m1qMyb8SQWFryDPUthpdHHeAtC67BbDiIaYQoVNSsaPsrbB7q8qEipURSeu00HJr4fq5U'


langfuse = Langfuse()

class MutableHandler(BaseCallbackHandler):
    def __init__(self, *args, langfuseHandler, preferences, stripe_subscription_id, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance_id = uuid4()
        self.langfuseHandler = langfuseHandler
        self.langfuse_trace_id = None
        self.langfuse_trace = None 
        self.answer = None 
        self.question = None
        self.documents = []
        self.scores = {}
        self.preferences = preferences
        self.metrics = preferences['metrics']
        self.stripe_subscription_id = stripe_subscription_id
        self.userInput = None 
        self.user_score = None 
        self.thumbs_up = None 
        self.paymentThresholdMet = None


       
    
    def score_with_ragas(self): 
        for m in self.metrics:
            print("Scoring: %s"%(m.name))
            self.scores[m.name] = m.score_single(
                {"question": self.question, "contexts": self.documents, "answer": self.answer}
            )
            print("Scored it: %s is %s"%(m.name, self.scores[m.name]))
        return self.scores
    def on_retriever_end(self, documents, **kwargs): 
        for doc in documents:
            self.documents.append(doc.page_content)
        

    def on_chain_end(self, outputs:Dict[str,Any], *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs:Any) -> Any: 
        try: 
            self.langfuse_trace_id = self.langfuseHandler.trace.id 
            #self.get_and_score_trace()
            '''
            
            trace_id = self.langfuse_trace_id 
            self.langfuse_trace = langfuse.get_trace(id=trace_id)
            trace = self.langfuse_trace 
            self.answer = self.langfuse_trace.output
            self.question = self.langfuse_trace.input
            scores = self.score_with_ragas()
            self.scores = scores 
            self.logScore(trace, scores)
            '''
            
        except Exception as e:
            print(f'Exception occured: {e}')

    def get_and_score_trace(self, userInput = {}):
        trace_id = self.langfuse_trace_id 
        print("Got trace ID")
        self.langfuse_trace = langfuse.get_trace(id=trace_id)
        print("Got trace")
        input_keys = self.langfuse_trace.input.keys() 
        query_key = list(input_keys)[0]
        self.question = self.langfuse_trace.input[query_key]
        print("Got query")
        found_output = False 
        for obs in self.langfuse_trace.observations: 
            if obs.output is not None and not (isinstance(obs.output, list)):
                found_output = True 
                if isinstance(obs.output, dict):
                    self.answer = obs.output[list(obs.output.keys())[0]]
                else:
                    self.answer = obs.output 
        print("Got answer")   
        if not userInput:
            self.scoring_flow()
            return self.evaluate_response()
        if userInput:
            self.scoring_flow()
            print ('Got user input%s'%(userInput))
            self.userInput = userInput 
            user_score = userInput['user_score'] if userInput['user_score'] else None 
            thumbs_up = userInput['thumbs_up'] if userInput['thumbs_up'] is not None else None 
            self.user_score = user_score 
            self.thumbs_up = thumbs_up 
            print('User inputs added as model attributes: %s, %s'%(self.user_score, self.thumbs_up))
            return self.evaluate_response()

    def scoring_flow(self):
        scores = self.score_with_ragas()
        print("Scored!")
        self.logScore()
        
    
    
    def logScore(self):
        for k in self.scores: 
            print("Logging score: (%s, %s)"%(k, self.scores[k]))
            langfuse.score(trace_id=self.langfuse_trace_id, name=k, value=self.scores[k])
            print("Logged %s"%(k))
    def return_documents(self):
        return self.documents 

    def return_trace_id(self):
        return self.langfuse_trace_id
    
    def get_trace_score(self):
        trace_id = self.langfuse_trace_id 
        langfuseTrace = langfuse.get_trace(id=trace_id)
        scores = langfuseTrace.scores 
        return scores 
    
    def get_stored_scores(self):
        return self.scores
    def get_qa(self):
        return (self.question, self.answer)
    

    def meet_threshold(self, scores): 
        thresholds = {} 
        print("Created thresholds dictionary")
        for score_key in scores: 
            thresholds[score_key] = self.preferences['threshold']['evals']
        print("Thresholds added for: (%s)"%(str(thresholds.keys())))
        metThreshold = []
        for score in scores:
            print("Evaluating %s"%(score))
            if scores[score] >= thresholds[score]:
                print("%s threshold met: %s >= %s"%(score, scores[score], thresholds[score])) 
                metThreshold.append(True)
            else:
                print('%s threshold not met: %s < %s'%(score, scores[score], thresholds[score]))
                metThreshold.append(False)
        if False in metThreshold:
            return False 
        else:
            return True
        


    def scoresIn(self):
        trace = langfuse.get_trace(id=self.langfuse_trace_id)
        print('Scores: %s'%(trace.scores))
        if not trace.scores:
            self.scoresIn() 
        else:
            if not len(trace.scores) == len(self.metrics):
                self.scoresIn()
            else:
                return trace.scores 

    def evaluation_flow(self):
        print("Evaluating with trace ID: %s..."%(self.langfuse_trace_id))
        trace = langfuse.get_trace(id=self.langfuse_trace_id)
        '''
        score_dict = {}
        print("Score dictionary instantiated")
        
        print('Now, we run a recursive function that continiously checks for scores')
        scores_rec = self.scoresIn()
        '''
        scores_rec = self.scores
        print('Scores received%s'%(scores_rec))
        '''
        for score in scores_rec: 
            print("Adding %s to the dictionary"%(score.name))
            score_dict[score.name] = score.value 
            print("Added")
        '''
        print("Checking threshold met")
        threshold_met = self.meet_threshold(scores_rec)
         
        
        return threshold_met 
        
    def evaluate_response(self):
        if not self.userInput: 
            threshold_met = self.evaluation_flow()
            if threshold_met: 
                self.paymentThresholdMet = True 
                print("Performance threshold met. Triggering payment!")
                self.mainPayment()
            else:
                self.paymentThresholdMet = False 
                print('Performance threshold not met. No payment triggered.')
        else:
            print('Executing chain with user input')
            threshold_met = self.evaluation_flow()
            qualThreshold = False 
            if self.user_score: 
                print('There\'s a user score')
                user_score = self.user_score 
                print('%s vs. %s'%(user_score, self.preferences['threshold']['user_score']))
                qualThreshold = True if user_score >= self.preferences['threshold']['user_score'] else False 
                print(qualThreshold)
            if self.thumbs_up is not None: 
                print('There\'s also a thumbs up response')
                thumbs_up = self.thumbs_up 
                qualThreshold = True if thumbs_up else False 
                print(qualThreshold)
            if qualThreshold and threshold_met:
                self.paymentThresholdMet = True 
                print("Performance threshold met. Triggering payment!") 
                self.mainPayment() 
            else:
                self.paymentThresholdMet = False 
                print('Performance threshold not met. No payment triggered.')


    def shouldPay(self):
        return self.paymentThresholdMet
             





    def mainPayment(self):
        sub = stripe.Subscription.retrieve(id=self.stripe_subscription_id)
        subscription_items = sub['items']
        subscription_item_id = subscription_items['data'][0]['id']


        usage_quantity=1 
        timestamp = int(time.time())
        idempotency_key = str(uuid4())

        try: 
            stripe.SubscriptionItem.create_usage_record(
                subscription_item_id,
                quantity=usage_quantity,
                timestamp=timestamp,
                action='set',
                idempotency_key=idempotency_key

            )
            print('Monthly invoice incremented by satisfactory response unit price')

        except Exception as e:
            print('Exception encountered %s'%(e))





        
