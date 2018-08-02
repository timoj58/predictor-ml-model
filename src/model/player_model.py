import dataset.player_dataset as player_dataset
import featureset.player_featureset as player_featureset
import util.vocab_utils as vocab_utils
import util.classifier_utils as classifier_utils
import util.dataset_utils as dataset_utils
import util.model_utils as model_utils
from util.file_utils import on_finish



def create(type, country, player, train, label, label_values, model_dir, file_type, convert):

    aws_model_dir = +type+'/'+country+'/'+player
    tf_models_dir = model_utils.MODELS_DIR+model_dir+'/'+aws_model_dir

    if convert:
        convertValue = label_values
    else:
        convertValue = convert

    (train_x, train_y), (test_x, test_y) = player_dataset.load_data(
        model_utils.MODEL_RES_DIR+'train-'+file_type+type+'-'+country+'-'+player+'.csv',
        model_utils.MODEL_RES_DIR+'test-'+file_type+type+'-'+country+'-'+player+'.csv',
        label, convertValue)

    print ('team vocab started...')
    team_file = vocab_utils.create_vocab(vocab_utils.TEAMS_URL, vocab_utils.TEAMS_FILE, type, country, None);
    print ('team vocab completed')
    print ('player vocab started...')
    player_file = vocab_utils.create_vocab(vocab_utils.PLAYERS_URL,vocab_utils.PLAYERS_FILE, type, country, player);
    print ('player vocab completed')

    # and the other numerics.  they will be read from a CSV / or direct from mongo more likely.  yes.  from mongo.
    # and review checkpoints, to only train with the newest data?  or build from scratch.  lets see.
    #need to add the label field too.

    feature_columns = player_featureset.create_feature_columns(player_file, team_file)


    # Build 2 hidden layer DNN with 10, 10 units respectively.  (from example will enrich at some point).
    classifier = classifier_utils.create(feature_columns,len(label_values), tf_models_dir)

    if train:
        # Train the Model.
        print(len(train_y))
        classifier.train(
            input_fn=lambda:dataset_utils.train_input_fn(train_x, train_y, len(train_y)),steps=1000)

        # Evaluate the model.  w dont really care about this given we cant set up different data.
        eval_result = classifier.evaluate(
            input_fn=lambda:dataset_utils.eval_input_fn(test_x, test_y,len(test_y)))

        print('\nTest set accuracy: {accuracy:0.3f}\n'.format(**eval_result))

    #probably can tidy this all up.  in one call.
    on_finish(tf_models_dir, aws_model_dir)

    return classifier








