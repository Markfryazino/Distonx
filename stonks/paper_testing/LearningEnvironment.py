import stonks.auxiliary.data_preprocessing as dp
from tf_agents.specs import array_spec
from tf_agents.environments import py_environment
import tf_agents.trajectories.time_step as ts
import numpy as np
from ..DataCatcher import DB
from sklearn.preprocessing import StandardScaler
import datetime
import joblib
import time
import pandas as pd


class LearningEnvironment(py_environment.PyEnvironment):
    def __init__(self, emulator, balance, logger=None, start_time=1581434096, test_time=12 * 3600,
                 indent=3600, period=1., reset=True, string_start='', orderbook_depth=5,
                 action_ratio=0.25,
                 return_type='delta'):
        super().__init__()
        self.action_ratio = action_ratio
        self.db = DB()
        self.emulator = emulator
        self.logger = logger
        self.indent = indent
        self.return_type = return_type
        self.period = period
        self.start_time = start_time
        self.test_time = test_time
        self.current_data = {}
        self.memory = {}
        self.data = {}
        self.somes = {}
        self.times = {}
        self.current_time = start_time
        self.agent_balance = balance.copy()
        self.start_balance = balance.copy()
        self.max_balance = balance.copy()
        self.orderbook_depth = orderbook_depth

        assert len(balance) == 6, 'А почему баланс всего из 6 валют?'

        with open(string_start + 'settings/pairs.txt') as file:
            self.pairs = [a[:-1] for a in file.readlines()]
        with open(string_start + 'settings/cryptos.txt') as file:
            self.assets = [a[:-1] for a in file.readlines()]

        n = self.orderbook_depth

        memory_columns = [f'depth_ask_price_{i + 1}' for i in range(n)] + \
                         [f'depth_bid_price_{i + 1}' for i in range(n)] + \
                         [f'depth_ask_quantity_{i + 1}' for i in range(n)] + \
                         [f'depth_bid_quantity_{i + 1}' for i in range(n)]
        self.memory_columns = {val: idx for idx, val in enumerate(memory_columns)}

        for pair in self.pairs:
            self.memory[pair] = self.db.fetch_pandas(start=start_time - indent,
                                                     end=start_time + test_time, pair_names={pair})
            self.times[pair] = self.memory[pair]['time'].copy()
            self.times[pair].index = self.times[pair].apply(datetime.datetime.fromtimestamp)
            self.memory[pair].index = self.memory[pair]['time'].apply(datetime.datetime.fromtimestamp)
            data = dp.basic_clean(self.memory[pair].copy())
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
                joblib.dump(ok_cols, string_start + 'settings/Env_settings/' + pair + '_columns.joblib')
                joblib.dump(scaler, string_start + 'settings/Env_settings/' + pair + '_scaler.joblib')
            else:
                scaler = joblib.load(string_start + 'settings/Env_settings/' + pair + '_scaler.joblib')
                ok_cols = joblib.load(string_start + 'settings/Env_settings/' + pair + '_columns.joblib')
                some = some[ok_cols]

            some = some.loc[common_index]
            self.memory[pair] = self.memory[pair].loc[common_index][memory_columns].values
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

        self._action_spec = array_spec.BoundedArraySpec(shape=(), dtype=np.int32, minimum=0, maximum=22,
                                                        name='action')
        self._observation_spec = array_spec.ArraySpec(shape=(11 * 109 + 6,), dtype=np.float64,
                                                      name='observation')
        self._episode_ended = False

        init_handle = self.emulator.handle([], self.agent_balance, self.form_orderbook())
        self.history = [(self.current_time, init_handle['new_usdt'])]

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _reset(self):
        self._episode_ended = False
        self.current_time = self.start_time
        self.agent_balance = self.start_balance.copy()
        self.max_balance = self.start_balance.copy()
        self.history = [self.history[0]]
        return ts.restart(self.form_observation())

    def get_current(self):
        idx = self.time_to_id.loc[self.current_time]
        return {pair: self.data[pair][idx] for pair in self.pairs}

    def form_observation(self):
        cur_data = self.get_current()
        npbalance = np.array([self.agent_balance[asset] for asset in self.assets])
        return np.hstack([cur_data[pair].T.reshape(109,) for pair in self.pairs] + [npbalance])

    def form_orderbook(self):

        orderbook = {pair: {'bids': [], 'asks': []} for pair in self.pairs}
        idx = self.time_to_id.loc[self.current_time]

        for pair in self.pairs:
            mem = self.memory[pair][idx]
            for i in range(self.orderbook_depth):
                for side in ('bid', 'ask'):
                    price = float(mem[0][self.memory_columns[f'depth_{side}_price_{i + 1}']])
                    quantity = float(mem[0][self.memory_columns[f'depth_{side}_quantity_{i + 1}']])
                    orderbook[pair][side + 's'].append([price, quantity + 5e6])

        return orderbook

    def _step(self, action):

        if self._episode_ended:
            return self.reset()

        query = []
        if action != 22:
            pair = self.pairs[action // 2]
            sell_base = action % 2
            if sell_base:
                query.append((pair, 'sell base', self.max_balance[pair[:3]] * self.action_ratio))
            else:
                query.append((pair, 'sell quote', self.max_balance[pair[3:]] * self.action_ratio))

        orderbook = self.form_orderbook()

        result = self.emulator.handle(query, self.agent_balance, orderbook)
        if self.logger is not None:
            self.logger.step({'query': query, 'emulator_response': result})

        for key, val in result['delta_balance'].items():
            self.agent_balance[key] += val
            if val > 0:
                self.max_balance[key] = self.agent_balance[key]
        if self.return_type == 'delta':
            reward = result['new_usdt'] - self.history[-1][1]
        else:
            reward = result['new_usdt']
        self.history.append((self.current_time, result['new_usdt']))

        self.current_time += self.period
        if self.current_time >= self.start_time + self.test_time - self.period:
            self._episode_ended = True

        observation = self.form_observation()

        if self._episode_ended:
            return ts.termination(observation, reward)
        else:
            return ts.transition(observation, reward)
