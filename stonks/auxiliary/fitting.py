from ..DataCatcher.database_saver import db
import pandas as pd
import logging


def fit_model(model, start_time, end_time, pair_name=''):
    dbase = db()
    names = dbase.get_columns_names()
    data = dbase.get_data_from_DB(start_time, end_time, pair_name)
    logging.debug('fetched data')
    data = pd.DataFrame(data=data, columns=names)
    model.fit(data)
