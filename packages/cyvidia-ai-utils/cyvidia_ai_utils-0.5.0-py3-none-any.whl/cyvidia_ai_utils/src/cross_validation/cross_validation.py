from typing import  Dict, Mapping, Optional
from datasets import Dataset,concatenate_datasets
from cyvidia_ai_utils.src.cross_validation.cross_validation_model.cross_validation_model import CrossValidationModel, EvalAverageType, EvaluationResult
   
def cross_validate(
    model: CrossValidationModel,
    folds: list[Dataset] | Mapping[str, Dataset],
    target_id_column:str,
    input_text_column:str,
    average: EvalAverageType= EvalAverageType.WEIGHTED
):
    """Cross validate the model using the given folds and target column.
    Returns a dictionary of validation fold index to evaluation result.
    """
    if isinstance(folds, Mapping):
        fold_list: list[Dataset]=[]
        fold_labels:list[str]=[]
        
        for label, fold in folds.items():
            fold_list.append(fold)
            fold_labels.append(label)
    else:
        fold_list= folds
        fold_labels= [str(i) for i in range(len(folds))]
        
    results: Dict[str, EvaluationResult] = {}
    for i, val_ds in enumerate(fold_list):
        train_folds = fold_list[:i] + fold_list[i+1:]
        
        train_ds= concatenate_datasets(train_folds)
        trained_model= model.train(train_ds, val_ds)
        result= trained_model.evaluate(val_ds, target_column=target_id_column, input_column=input_text_column, average=average)
        
        results[fold_labels[i]] = result
    return results
        