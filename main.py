import yfinance as yf
import pandas as pd
import numpy as np

data = yf.download(
    "VOO",
    start="2010-01-01",
    auto_adjust=True
)

data = data.droplevel(level=1, axis=1)

data["sma200"] = (
    data["Close"]
    .rolling(200)
    .mean()
)

data["mom60"] = (
    data["Close"]
    .pct_change(60)
)


data["signal"] = np.where(
    (data["Close"] > data["sma200"])
    &
    (data["mom60"] > 0),
    1,
    0
)

data["ret"] = data["Close"].pct_change()

data["vol"] = (
    data["ret"]
    .rolling(20)
    .std()
)

data["vol_weight"] = (
    0.02 /
    data["vol"]
)

data["vol_weight"] = (
    data["vol_weight"]
    .clip(upper=1)
)


data["position"] = (
    data["signal"]
    .shift(1)
    *
    data["vol_weight"]
    .shift(1)
)

data["trade"] = (
    data["position"]
    .diff()
    .abs()
)

cost_rate = 0.001

data["cost"] = (
    data["trade"]
    *
    cost_rate
)

data["strategy_ret"] = (
    data["position"]
    *
    data["ret"]
    -
    data["cost"]
)

data["equity"] = (
    1 +
    data["strategy_ret"]
).cumprod()

sharpe = (
    data["strategy_ret"].mean()
    /
    data["strategy_ret"].std()
) * np.sqrt(252)

data["peak"] = (
    data["equity"]
    .cummax()
)

data["drawdown"] = (
    data["equity"]
    /
    data["peak"]
    - 1
)

max_dd = (
    data["drawdown"]
    .min()
)

import matplotlib.pyplot as plt

data["equity"].plot()

plt.show()


print(data.tail())
print(sharpe )