from typing import Any, Callable, Dict, Optional
from cyvidia_ai_utils.src.cross_validation.cross_validation_model.cross_validation_model import CrossValidationModel
from transformers import PreTrainedModel, Trainer,PreTrainedTokenizer, pipeline,PreTrainedTokenizerFast
from datasets import Dataset

class TransformerCrossValidationModel(CrossValidationModel):
    def __init__(self, model: PreTrainedModel, tokenizer: PreTrainedTokenizer | PreTrainedTokenizerFast, create_trainer: Callable[[PreTrainedModel, PreTrainedTokenizer | PreTrainedTokenizerFast,Dataset, Dataset],Trainer]):
        self.model = model
        self.tokenizer = tokenizer
        self.create_trainer= create_trainer
        
    def get_label_for_id(self, id: int)-> str:
        return self.model.config.id2label[id]

    def train(self, train_ds, val_ds):
        trainer= self.create_trainer(self.model, self.tokenizer, train_ds, val_ds)
        
        trainer.train()
        
        return TransformerCrossValidationModel(trainer.model, self.tokenizer, self.create_trainer)

    def predict_values(self, values)-> Dict[str,Any]:
        classifier= pipeline("text-classification", model=self.model, tokenizer=self.tokenizer)
        
        return classifier(values)
