from typing import Any, Callable, Dict, Optional
from cyvidia_ai_utils.src.cross_validation.cross_validation_model.cross_validation_model import CrossValidationModel
from transformers import BertForSequenceClassification, Trainer,PreTrainedTokenizer, pipeline,PreTrainedTokenizerFast
from datasets import Dataset

class BertCrossValidationModel(CrossValidationModel):
    def __init__(self, model: BertForSequenceClassification, tokenizer: PreTrainedTokenizer | PreTrainedTokenizerFast, create_trainer: Callable[[Dataset, Dataset],Trainer]):
        self.model = model
        self.tokenizer = tokenizer
        self.create_trainer= create_trainer
        
    def get_label_for_id(self, id: int)-> str:
        return self.model.config.id2label[id]

    def train(self, train_ds, val_ds):
        trainer= self.create_trainer(train_ds, val_ds)
        
        trainer.train()
        
        return BertCrossValidationModel(trainer.model, self.tokenizer, self.create_trainer)

    def predict_values(self, values)-> Dict[str,Any]:
        '''Return the predicted values for the given input values.
        return looks like `[{"label": "POSITIVE", "score": 0.9999}, {"label": "NEGATIVE", "score": 0.7001}]`
        '''
        classifier= pipeline("text-classification", model=self.model, tokenizer=self.tokenizer)
        
        return classifier(values)
