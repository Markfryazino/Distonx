# Distonx

This is an attempt to build a some kind of autonomous cryptocurrency trading bot that uses supervised and reinforcement learning for decision making. Trading is done on Binance cryptocurrency market via its API and [11 pairs](https://github.com/Markfryazino/Distonx/blob/master/settings/pairs.txt) are traded simultaneously.

The implemented model uses a separate neural network predicting the movement of the rate for each pair. The training data was collected by ourselves and covers about a month.

Currently in progress is building an environment for reinforcement learning model based on a Deep Q-Network.
