from predict.match_predict import predict as predict_process
import dataset.match_dataset as match_dataset


def predict(data, type, country):

    return predict_process(
        data,
        type,
        country,
        'outcome',
        match_dataset.OUTCOMES,
        "match_result",
        "matches-",
        False)

