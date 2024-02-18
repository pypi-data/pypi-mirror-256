

class BaseLLMLoader():
  def __init__(self, model_path, *args, **kuwargs):
    self.model_path = model_path
    for k, v in kuwargs.items():
      setattr(self, k, v)
  
  def load(self, **kwargs):
    """Implement this method in the subclass"""

class BaseLLMCalculator():
  def __init__(self, *, tokenizer = None, model = None, **kuwargs):
    self.model = model
    self.tokenizer = tokenizer
  
  def _calculate_token_per_second(self, text):
    """Implement this method in the subclass"""
