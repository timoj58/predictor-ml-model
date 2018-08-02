import tensorflow as tf
import util.featureset_utils as featureset_utils


def create_feature_columns(player_vocab, team_vocab):
    # sort out the featulre columns
    feature_columns = []

    feature_columns.append(featureset_utils.create_category_indicator_column('home', team_vocab))
     #feature_columns.append(featureset_utils.create_category_indicator_column('away', team_vocab, team_vocab_count))

    #feature_columns.append(tf.feature_column.indicator_column(featureset_utils.create_teams(team_vocab, team_vocab_count)))
    feature_columns.append(tf.feature_column.indicator_column(featureset_utils.create_home_players(player_vocab)))

    feature_columns.append(featureset_utils.create_category_indicator_column('away', team_vocab))
    feature_columns.append(tf.feature_column.indicator_column(featureset_utils.create_away_players(player_vocab)))

    return feature_columns


