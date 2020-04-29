import stonks.auxiliary.data_preprocessing as dp
from tf_agents.specs import array_spec
from tf_agents.environments import py_environment
import numpy as np
from ..DataCatcher import DB
from sklearn.preprocessing import StandardScaler
import datetime
import joblib
import pandas as pd


class LearningEnvironment(py_environment.PyEnvironment):
    def __init__(self, emulator, logger=None, start_time=1581434096, test_time=3600,
                 indent=3600, period=1., reset=True):
        super().__init__()
        self.db = DB()
        self.emulator = emulator
        self.logger = logger
        self.indent = indent
        self.period = period
        self.start_time = start_time
        self.test_time = test_time
        self.current_data = {}
        self.memory = {}
        self.data = {}
        self.somes = {}
        self.times = {}
        self.current_time = start_time
        with open('settings/pairs.txt') as file:
            self.pairs = [a[:-1] for a in file.readlines()]

        for pair in self.pairs:
            self.memory[pair] = self.db.fetch_pandas(start=start_time - indent,
                                                     end=start_time + test_time, pair_names={pair})
            self.times[pair] = self.memory[pair]['time']
            self.times[pair].index = self.times[pair].apply(datetime.datetime.fromtimestamp)
            data = dp.basic_clean(self.memory[pair])
            copy = data.copy()
            some = dp.make_x(copy)
            self.times[pair] = self.times[pair][some.index]
            self.somes[pair] = some

        common_index = self.times[self.pairs[0]].index
        for pair in self.pairs:
            common_index = common_index.intersection(self.times[pair].index)
        self.time = self.times[self.pairs[0]][common_index]

        for pair in self.pairs:
            some = self.somes[pair]
            if reset:
                scaler = StandardScaler()
                ok_cols = list(some.columns)
                scaler.fit(some)
                joblib.dump(ok_cols, 'settings/Env_settings/' + pair + '_columns.joblib')
                joblib.dump(scaler, 'settings/Env_settings/' + pair + '_scaler.joblib')
            else:
                scaler = joblib.load('settings/Env_settings/' + pair + '_scaler.joblib')
                ok_cols = joblib.load('settings/Env_settings/' + pair + '_columns.joblib')
                some = some[ok_cols]

            some = some.loc[common_index]
            self.data[pair] = scaler.transform(some)

        time = self.time.reset_index(drop=True)
        current = pd.Series(range(start_time, start_time + test_time))
        timeta = pd.DataFrame(time, columns=['time'])
        timeta['index'] = timeta.index
        curta = pd.DataFrame(current, columns=['time'])
        merged = curta.merge(timeta, how='outer', sort=True)
        merged.ffill(inplace=True)
        final = curta.join(merged.set_index('time'), on='time')
        final = final.set_index('time')
        final['index'] = final['index'].apply(int)
        self.time_to_id = final

        del self.times, self.somes

        self._action_spec = array_spec.BoundedArraySpec(shape=(), dtype=np.int32, minimum=0, maximum=12,
                                                        name='action')
        self._observation_spec = array_spec.ArraySpec(shape=(indent, 11 * 109 + 11), dtype=np.float64,
                                                      name='observation')
        self._episode_ended = False

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _reset(self):
        self._episode_ended = False
        self.current_time = self.start_time

    def get_current(self):
        idx = self.time_to_id[self.current_time]
        return {pair: self.data[pair].iloc[idx] for pair in self.pairs}

    def _step(self, action):
        if self._episode_ended:
            return self.reset()

        current = self.get_current()
        query = []


