from typing import  Dict, Mapping, Callable
from datasets import Dataset,concatenate_datasets
from cyvidia_ai_utils.src.cross_validation.cross_validation_model.cross_validation_model import CrossValidationModel
from cyvidia_ai_utils.src.cross_validation.evaluation_result import EvalAverageType, EvaluationResult
   
def cross_validate(
    create_model_instance: Callable[[],CrossValidationModel],
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
        
        model= create_model_instance()
        model.train(train_ds, val_ds)
        result= __evaluate_model(model, val_ds, target_column=target_id_column, input_column=input_text_column, average=average)
        
        results[fold_labels[i]] = result
    return results

def __evaluate_model(model: 'CrossValidationModel',test_ds: Dataset,input_column:str, target_column:str, average: EvalAverageType= EvalAverageType.WEIGHTED)-> EvaluationResult:
    predictions_with_scores= model.predict_values(test_ds[input_column])

    predictions= [pred['label'] for pred in predictions_with_scores]
        
    true_values = list(map(lambda x: model.get_label_for_id(x), test_ds[target_column]))

    return EvaluationResult.from_values(true_values, predictions, average)          
        