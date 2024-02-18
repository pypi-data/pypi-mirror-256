from abc import abstractmethod
from enum import Enum
from typing import Any, Dict, Mapping, MutableMapping, Optional
from datasets import Dataset
import numpy as np

import sklearn.metrics as metrics


class EvalAverageType(Enum):
    MICRO = "micro"
    MACRO = "macro"
    WEIGHTED = "weighted"
    SAMPLES= "samples"
    BINARY= "binary"
    NONE= None


class EvaluationResult:
    def __init__(self, accuracy:float| np.float16, f1: Any, percision:Any):
        if not isinstance(f1, np.ndarray):
            f1= float(f1)
            
        if not isinstance(percision, np.ndarray):
            percision= float(percision)

        self.accuracy = accuracy
        self.f1 = f1
        self.percision = percision

    def __str__(self):
        return f"Accuracy: {self.accuracy}, F1: {self.f1}, Percision: {self.percision}"

class CrossValidationModel:
    """Implement this interface to create a model that can be cross-validated."""
    @abstractmethod
    def train(self, train_ds: Dataset, val_ds:Dataset)-> 'CrossValidationModel':
        """Train the model using the given dataset and return the trained model."""
        pass
    
    @abstractmethod
    def predict_values(self, values)-> list[Dict[str,Any]]:...
    @abstractmethod
    def get_label_for_id(self, id: int)-> str:...
    
    def evaluate(self, test_ds: Dataset,input_column:str, target_column:str, average: EvalAverageType= EvalAverageType.WEIGHTED)-> EvaluationResult:
        predictions_with_scores= self.predict_values(test_ds[input_column])
        
        predictions= [pred['label'] for pred in predictions_with_scores]
            
        true_values = list(map(lambda x: self.get_label_for_id(x), test_ds[target_column]))

        return EvaluationResult(
            accuracy=float(metrics.accuracy_score(true_values, predictions)),
            f1=metrics.f1_score(true_values, predictions, average=average.value),
            percision=metrics.precision_score(true_values, predictions, average=average.value)
        )