from LLMagic.base import BaseLLMCalculator
from typing import List
from time import time

class MixtralSpeedCalculator(BaseLLMCalculator):

    def _calculate_token_per_second(self, text:str, time_taken:float):
        """Calculate token per second"""
        if self.tokenizer:
            tokens = self.tokenizer.tokenize(text.encode("utf-8"))
        else:
            tokens = self.model.tokenize()
        return len(tokens) / time_taken
    
    def calculate(self, prompts: List[str], **kwargs):
        """Calculate speed of Mixtral model"""
        results = {
            "prompt": [],
            "response": [],
            "speed": []
        }
        for prompt in prompts:
            start = time()
            answer = self.model(prompt)
            end = time()
            results["prompt"].append(prompt)
            results["response"].append(answer)
            results["speed"].append(self._calculate_token_per_second(answer, end - start))
        
        return results
        

