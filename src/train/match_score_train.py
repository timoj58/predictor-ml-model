import util.model_utils as model_utils
import util.cache_utils as cache_utils
import util.receipt_utils as receipt_utils
import util.training_utils as training_utils
import dataset.match_dataset as match_dataset
import util.train_history_utils as train_history_utils
from util.config_utils import get_dir_cfg
from util.config_utils import get_learning_cfg
import logging

logger = logging.getLogger(__name__)


local_dir = get_dir_cfg()['local']
history_file = get_dir_cfg()['country_scores_train_history_file']


def train(receipt):

    logger.info ('starting...')

    # so get types.
    types = cache_utils.get_types(cache_utils.TYPES_URL)

    for type in types:
        logger.info (type)
        countries = cache_utils.get_countries(cache_utils.COUNTRIES_URL, type)
        for country in countries:
            logger.info (country)
            train_country(type, country, receipt)

    receipt_utils.put_receipt(receipt_utils.TRAIN_RECEIPT_URL, receipt, None)


def train_country(type, country, receipt):

    learning_cfg = get_learning_cfg(country, "match_score")


    previous_vocab_date=train_history_utils.get_previous_vocab_date(country)
    history = train_history_utils.init_history('in progress',learning_cfg)



    training_utils.train_match(
                         type=type,
                         country=country,
                         data_range=training_utils.create_data_range(learning_cfg=learning_cfg, history_file=history_file, type=type, country=country),
                         label='scoreOutcome',
                         label_values=match_dataset.SCORE_OUTCOMES,
                         model_dir="match_score",
                         train_path=training_utils.create_train_path(type, country),
                         receipt=receipt,
                         history=history,
                         previous_vocab_date=previous_vocab_date,
                         show_outcome=True,
                         history_file=history_file)

