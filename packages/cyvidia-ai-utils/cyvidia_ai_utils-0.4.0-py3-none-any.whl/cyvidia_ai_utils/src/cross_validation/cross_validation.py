from typing import  Dict
from datasets import Dataset,concatenate_datasets
from cyvidia_ai_utils.src.cross_validation.cross_validation_model.cross_validation_model import CrossValidationModel, EvalAverageType, EvaluationResult
   
def cross_validate(
    model: CrossValidationModel,
    folds: list[Dataset],
    target_id_column:str,
    input_text_column:str,
    average: EvalAverageType= EvalAverageType.WEIGHTED
):
    """Cross validate the model using the given folds and target column.
    Returns a dictionary of validation fold index to evaluation result.
    """
    results: Dict[int, EvaluationResult] = {}
    for i, val_ds in enumerate(folds):
        train_folds = folds[:i] + folds[i+1:]
        
        train_ds= concatenate_datasets(train_folds)
        trained_model= model.train(train_ds, val_ds)
        result= trained_model.evaluate(val_ds, target_column=target_id_column, input_column=input_text_column, average=average)
        
        results[i] = result
    return results
        