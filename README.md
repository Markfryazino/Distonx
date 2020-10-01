# Distonx

This is an attempt to build some kind of autonomous cryptocurrency trading bot that uses supervised and reinforcement learning for decision making. Trading is done on Binance cryptocurrency market via its API and [11 pairs](https://github.com/Markfryazino/Distonx/blob/master/settings/pairs.txt) are traded simultaneously.

At the current moment, the project is closed despite the fact some of its parts remain unfinished. The components we've implemented include:
1. [The system](stonks/DataCatcher) for mining dataset from Binance. The dataset contains such data as the top 20 levels of orderbook and various features that aggregate prices, volumes and trading intensity.
2. [The emulator](stonks/paper_testing) of the market and environment for paper testing. Models can be evaluated both in real-time or on historical data. Also, we've implemented a TF-Agents environment for reinforcement learning.
3. [A prototype model](stonks/modeling) that uses independent neural networks predicting the movement of the rate for each pair.

Apart from that, in [this directory](research) you can see all the code we used for research. For example, notebook [dqn-learn](research/dqn-learn.ipynb) shows our attempt to apply reinforcement learning (unfortunately, unsuccessful) and [feature_try](research/feature_try.ipynb) contains some code we used for feature engineering.
