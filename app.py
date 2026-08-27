# ============================================================
# 🐂 RAJESH STOCK ANALYZER PRO V3.2 MASTER
# NSE • Manual 1–15 Stocks
# EMS V3.2 • PRICE VALUE • D/W/M
# EMA 10/20/50/100/200 • CPR • RSI • MACD • SUPERTREND
# Momentum • Breakout Quality • Retest
# ATR Risk • Dynamic Entry • Dynamic Targets
# Signal Change Tracker • Swing + Long
# MOBILE-FIRST • READABLE NUMBERS • NO DUPLICATE CPR
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime

# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="RAJESH STOCK ANALYZER PRO V3.2",
    page_icon="🐂",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CSS — READABILITY LOCK
# ============================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: Arial, sans-serif !important;
}

.stApp {
    background:#050505;
    color:#F5F5F5;
}

.block-container {
    padding-top:.55rem !important;
    padding-left:.55rem !important;
    padding-right:.55rem !important;
    padding-bottom:2rem !important;
}

.app-title {
    font-size:24px !important;
    font-weight:900 !important;
    color:#FFFFFF !important;
    line-height:1.25 !important;
    margin-bottom:3px !important;
}

.app-subtitle {
    font-size:11px !important;
    color:#D0D0D0 !important;
    opacity:1 !important;
    line-height:1.45 !important;
}

.section-title {
    font-size:17px !important;
    font-weight:900 !important;
    color:#FFFFFF !important;
    line-height:1.3 !important;
    margin-top:11px !important;
    margin-bottom:6px !important;
}

.box-grid {
    display:grid;
    grid-template-columns:repeat(6,minmax(0,1fr));
    gap:5px;
    margin-bottom:8px;
}

.key-grid {
    display:grid;
    grid-template-columns:repeat(6,minmax(0,1fr));
    gap:4px;
}

.target-grid {
    display:grid;
    grid-template-columns:repeat(3,minmax(0,1fr));
    gap:5px;
}

.ems-grid {
    display:grid;
    grid-template-columns:repeat(5,minmax(0,1fr));
    gap:4px;
}

.metric-box,
.key-box,
.price-box,
.target-box,
.ems-box {
    border:1px solid #3A3A3A;
    border-radius:8px;
    background:#111111;
    padding:7px 5px;
    text-align:center;
    overflow:hidden;
    box-sizing:border-box;
}

.metric-title,
.key-title,
.price-title,
.target-title,
.ems-title {
    font-size:9px !important;
    font-weight:900 !important;
    color:#D8D8D8 !important;
    opacity:1 !important;
    white-space:nowrap;
    line-height:1.2 !important;
}

.metric-value,
.key-value,
.price-value,
.target-value,
.ems-value {
    font-size:13px !important;
    font-weight:900 !important;
    color:#FFFFFF !important;
    margin-top:3px !important;
    white-space:nowrap;
    line-height:1.25 !important;
}

.key-box {
    min-height:56px;
    display:flex;
    flex-direction:column;
    justify-content:center;
}

.key-value {
    font-size:11px !important;
}

.target-box {
    min-height:58px;
}

.target-value {
    font-size:13px !important;
}

.target-upside {
    font-size:9px !important;
    font-weight:800 !important;
    color:#D8D8D8 !important;
    margin-top:2px;
}

.ems-box {
    min-height:55px;
}

.ems-value {
    font-size:11px !important;
}

.green-box {
    border-color:#218545 !important;
}

.red-box {
    border-color:#A83232 !important;
}

.blue-box {
    border-color:#376AA5 !important;
}

.yellow-box {
    border-color:#9A7B1B !important;
}

.orange-box {
    border-color:#B2671A !important;
}

.key-positive {
    border-color:#218545 !important;
}

.key-negative {
    border-color:#A83232 !important;
}

.key-warning {
    border-color:#9A7B1B !important;
}

.signal {
    font-size:19px !important;
    font-weight:900 !important;
    color:#FFFFFF !important;
    padding:4px 0 !important;
    line-height:1.3 !important;
}

.small-note {
    font-size:10px !important;
    font-weight:700 !important;
    color:#D0D0D0 !important;
}

@media(max-width:900px) {

    .box-grid {
        grid-template-columns:repeat(3,1fr);
    }

    .key-grid {
        grid-template-columns:repeat(3,1fr);
    }

    .ems-grid {
        grid-template-columns:repeat(3,1fr);
    }
}

@media(max-width:500px) {

    .app-title {
        font-size:18px !important;
    }

    .app-subtitle {
        font-size:10px !important;
    }

    .box-grid {
        grid-template-columns:repeat(2,1fr);
        gap:4px;
    }

    .key-grid {
        grid-template-columns:repeat(3,1fr);
        gap:3px;
    }

    .target-grid {
        grid-template-columns:repeat(3,1fr);
        gap:3px;
    }

    .ems-grid {
        grid-template-columns:repeat(3,1fr);
        gap:3px;
    }

    .metric-box,
    .key-box,
    .price-box,
    .target-box,
    .ems-box {
        padding:6px 3px;
    }

    .key-box,
    .target-box,
    .ems-box {
        min-height:51px;
    }

    .key-title,
    .price-title,
    .target-title,
    .ems-title {
        font-size:8px !important;
    }

    .key-value,
    .target-value,
    .ems-value {
        font-size:10px !important;
    }

    .metric-value,
    .price-value {
        font-size:12px !important;
    }
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="app-title">🐂 RAJESH STOCK ANALYZER PRO V3.2 MASTER</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="app-subtitle">'
    'NSE • Manual 1–15 Stocks • EMS V3.2 • PRICE VALUE • D/W/M • '
    'EMA 10/20/50/100/200 • CPR Central Pivot Range • RSI • MACD • '
    'Supertrend • Momentum • Breakout Quality + Retest • ATR Risk • '
    'Dynamic Entry + Targets • Swing + Long'
    '</div>',
    unsafe_allow_html=True
)

# ============================================================
# HELPERS
# ============================================================

def safe_num(value, default=0.0):
    try:
        if value is None:
            return default
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def html_box(title, value, css=""):
    return f"""
    <div class="key-box {css}">
        <div class="key-title">{title}</div>
        <div class="key-value">{value}</div>
    </div>
    """


def price_box(title, value, css=""):
    return f"""
    <div class="price-box {css}">
        <div class="price-title">{title}</div>
        <div class="price-value">{value}</div>
    </div>
    """


def target_box(title, price, upside):
    return f"""
    <div class="target-box">
        <div class="target-title">{title}</div>
        <div class="target-value">₹{price:,.2f}</div>
        <div class="target-upside">{upside:+.1f}%</div>
    </div>
    """


def ems_box(title, value, css=""):
    return f"""
    <div class="ems-box {css}">
        <div class="ems-title">{title}</div>
        <div class="ems-value">{value}</div>
    </div>
    """

# ============================================================
# INDICATORS
# ============================================================

def calculate_indicators(df):

    df = df.copy()

    close = pd.to_numeric(df["Close"], errors="coerce")
    high = pd.to_numeric(df["High"], errors="coerce")
    low = pd.to_numeric(df["Low"], errors="coerce")
    volume = pd.to_numeric(df["Volume"], errors="coerce")

    # EMA
    for p in [10,20,50,100,200]:
        df[f"EMA{p}"] = close.ewm(
            span=p,
            adjust=False
        ).mean()

    # RSI 14
    delta = close.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(
        alpha=1/14,
        adjust=False
    ).mean()

    avg_loss = loss.ewm(
        alpha=1/14,
        adjust=False
    ).mean()

    rs = avg_gain / avg_loss.replace(0,np.nan)

    df["RSI14"] = 100 - (
        100 / (1 + rs)
    )

    df["RSI14"] = df["RSI14"].fillna(50)

    # MACD
    ema12 = close.ewm(
        span=12,
        adjust=False
    ).mean()

    ema26 = close.ewm(
        span=26,
        adjust=False
    ).mean()

    df["MACD"] = ema12 - ema26

    df["MACD_SIGNAL"] = df["MACD"].ewm(
        span=9,
        adjust=False
    ).mean()

    df["MACD_HIST"] = (
        df["MACD"] -
        df["MACD_SIGNAL"]
    )

    # Volume
    df["VOLUME_AVG20"] = volume.rolling(20).mean()

    df["VOLUME_RATIO"] = (
        volume /
        df["VOLUME_AVG20"].replace(0,np.nan)
    )

    df["VOLUME_RATIO"] = df["VOLUME_RATIO"].fillna(0)

    # 52 Week
    df["52W_HIGH"] = close.rolling(252).max()
    df["52W_LOW"] = close.rolling(252).min()

    # CPR
    prev_high = high.shift(1)
    prev_low = low.shift(1)
    prev_close = close.shift(1)

    df["PP"] = (
        prev_high +
        prev_low +
        prev_close
    ) / 3

    df["BC"] = (
        prev_high +
        prev_low
    ) / 2

    df["TC"] = (
        2 * df["PP"] -
        df["BC"]
    )

    df["CPR_LOW"] = df[
        ["BC","TC"]
    ].min(axis=1)

    df["CPR_HIGH"] = df[
        ["BC","TC"]
    ].max(axis=1)

    df["CPR_WIDTH"] = (
        (df["CPR_HIGH"] - df["CPR_LOW"]) /
        df["PP"].replace(0,np.nan)
    ) * 100

    # Support / Resistance
    df["SUPPORT20"] = low.rolling(20).min()
    df["RESISTANCE20"] = high.rolling(20).max()

    # ATR 14
    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()

    true_range = pd.concat(
        [tr1,tr2,tr3],
        axis=1
    ).max(axis=1)

    df["ATR14"] = true_range.rolling(14).mean()

    # Supertrend
    period = 10
    multiplier = 3.0

    atr_st = true_range.rolling(period).mean()

    hl2 = (high + low) / 2

    upper = hl2 + multiplier * atr_st
    lower = hl2 - multiplier * atr_st

    st_line = pd.Series(
        index=df.index,
        dtype=float
    )

    trend = pd.Series(
        index=df.index,
        dtype=int
    )

    if len(df) > 0:
        trend.iloc[0] = 1
        st_line.iloc[0] = lower.iloc[0]

    for i in range(1,len(df)):

        previous_upper = upper.iloc[i-1]
        previous_lower = lower.iloc[i-1]

        if close.iloc[i] > previous_upper:
            trend.iloc[i] = 1

        elif close.iloc[i] < previous_lower:
            trend.iloc[i] = -1

        else:
            trend.iloc[i] = trend.iloc[i-1]

        if trend.iloc[i] == 1:
            st_line.iloc[i] = lower.iloc[i]
        else:
            st_line.iloc[i] = upper.iloc[i]

    df["SUPERTREND_LINE"] = st_line
    df["SUPERTREND_TREND"] = trend

    # Momentum
    df["ROC20"] = close.pct_change(20) * 100

    # Trend slope
    df["EMA20_SLOPE"] = (
        df["EMA20"].pct_change(10) * 100
    )

    return df


# ============================================================
# D/W/M TREND ENGINE
# ============================================================

def one_timeframe_score(data):

    if data is None or len(data) < 60:
        return 50

    last = data.iloc[-1]

    close = safe_num(last["Close"])
    e20 = safe_num(last["EMA20"],close)
    e50 = safe_num(last["EMA50"],close)
    e200 = safe_num(last["EMA200"],close)
    rsi = safe_num(last["RSI14"],50)

    score = 50

    if close > e20:
        score += 15
    else:
        score -= 15

    if e20 > e50:
        score += 15
    else:
        score -= 15

    if close > e200:
        score += 10
    else:
        score -= 10

    if rsi >= 55:
        score += 10
    elif rsi < 40:
        score -= 10

    return max(0,min(100,score))


def timeframe_score(df):

    daily = one_timeframe_score(df)

    weekly = df.resample("W").agg({
        "Open":"first",
        "High":"max",
        "Low":"min",
        "Close":"last",
        "Volume":"sum"
    }).dropna()

    monthly = df.resample("ME").agg({
        "Open":"first",
        "High":"max",
        "Low":"min",
        "Close":"last",
        "Volume":"sum"
    }).dropna()

    weekly = calculate_indicators(weekly)
    monthly = calculate_indicators(monthly)

    weekly_score = one_timeframe_score(weekly)
    monthly_score = one_timeframe_score(monthly)

    master = round(
        daily * .40 +
        weekly_score * .30 +
        monthly_score * .30,
        1
    )

    if master >= 75:
        regime = "🐂 STRONG BULL"
    elif master >= 65:
        regime = "🟢 BULL"
    elif master >= 50:
        regime = "🟡 NEUTRAL"
    elif master >= 35:
        regime = "🟠 BEARISH"
    else:
        regime = "🔴 STRONG BEAR"

    return (
        daily,
        weekly_score,
        monthly_score,
        master,
        regime
    )

# ============================================================
# BREAKOUT QUALITY ENGINE
# ============================================================

def breakout_engine(df):

    last = df.iloc[-1]

    close = safe_num(last["Close"])
    resistance = safe_num(
        last["RESISTANCE20"],
        close
    )

    volume = safe_num(
        last["VOLUME_RATIO"],
        0
    )

    rsi = safe_num(
        last["RSI14"],
        50
    )

    macd = safe_num(last["MACD"])
    macd_signal = safe_num(
        last["MACD_SIGNAL"]
    )

    ema20 = safe_num(
        last["EMA20"],
        close
    )

    st = safe_num(
        last["SUPERTREND_TREND"],
        0
    )

    breakout_level = resistance * 1.003

    breakout = close >= breakout_level

    previous_resistance = safe_num(
        df["RESISTANCE20"].iloc[-2]
        if len(df) > 1 else resistance,
        resistance
    )

    retest_low = previous_resistance * .985
    retest_high = previous_resistance * 1.015

    retest = (
        retest_low <= close <= retest_high
    )

    volume_confirmed = volume >= 2.0

    confirmations = 0

    if breakout:
        confirmations += 1

    if volume_confirmed:
        confirmations += 1

    if retest:
        confirmations += 1

    if close > ema20:
        confirmations += 1

    if rsi >= 55:
        confirmations += 1

    if macd > macd_signal:
        confirmations += 1

    if st == 1:
        confirmations += 1

    if confirmations >= 6:
        quality = "🚀 STRONG"
    elif confirmations >= 4:
        quality = "🟢 GOOD"
    elif confirmations >= 2:
        quality = "🟡 DEVELOPING"
    else:
        quality = "🔴 WEAK"

    if breakout and volume_confirmed and retest:
        status = "🚀 BREAKOUT + RETEST CONFIRMED"
    elif breakout and volume_confirmed:
        status = "🚀 BREAKOUT CONFIRMED"
    elif breakout:
        status = "🟡 BREAKOUT / CONFIRMATION PENDING"
    else:
        status = "🟡 WATCH"

    return {
        "level":breakout_level,
        "breakout":breakout,
        "retest":retest,
        "retest_low":retest_low,
        "retest_high":retest_high,
        "volume_confirmed":volume_confirmed,
        "confirmations":confirmations,
        "quality":quality,
        "status":status
    }

# ============================================================
# TECHNICAL ENGINE
# ============================================================

def technical_engine(df):

    last = df.iloc[-1]

    close = safe_num(last["Close"])

    e10 = safe_num(last["EMA10"],close)
    e20 = safe_num(last["EMA20"],close)
    e50 = safe_num(last["EMA50"],close)
    e100 = safe_num(last["EMA100"],close)
    e200 = safe_num(last["EMA200"],close)

    rsi = safe_num(last["RSI14"],50)

    macd = safe_num(last["MACD"])
    macd_signal = safe_num(
        last["MACD_SIGNAL"]
    )

    volume = safe_num(
        last["VOLUME_RATIO"],
        0
    )

    st = safe_num(
        last["SUPERTREND_TREND"],
        0
    )

    score = 0

    # EMA 40%
    if close > e10:
        score += 8

    if e10 > e20:
        score += 8

    if e20 > e50:
        score += 8

    if e50 > e100:
        score += 8

    if e100 > e200:
        score += 8

    # RSI
    if rsi >= 60:
        score += 15
    elif rsi >= 50:
        score += 10
    elif rsi >= 40:
        score += 5

    # MACD
    if macd > macd_signal:
        score += 15

    # Supertrend
    if st == 1:
        score += 15

    # Volume
    if volume >= 2:
        score += 15
    elif volume >= 1:
        score += 8

    return max(
        0,
        min(100,round(score,1))
    )

# ============================================================
# PRICE VALUE ENGINE
# ============================================================

def price_value_engine(df):

    last = df.iloc[-1]

    cmp = safe_num(last["Close"])

    e20 = safe_num(last["EMA20"],cmp)
    e50 = safe_num(last["EMA50"],cmp)
    e100 = safe_num(last["EMA100"],cmp)
    e200 = safe_num(last["EMA200"],cmp)

    support = safe_num(
        last["SUPPORT20"],
        cmp*.95
    )

    resistance = safe_num(
        last["RESISTANCE20"],
        cmp*1.05
    )

    high52 = safe_num(
        last["52W_HIGH"],
        resistance
    )

    low52 = safe_num(
        last["52W_LOW"],
        support
    )

    reference = (
        e20*.15 +
        e50*.20 +
        e100*.20 +
        e200*.20 +
        resistance*.15 +
        high52*.10
    )

    distance = (
        (cmp-reference)/reference*100
        if reference > 0 else 0
    )

    # Value score
    if distance <= -15:
        value_score = 100
    elif distance <= -8:
        value_score = 90
    elif distance <= -3:
        value_score = 80
    elif distance <= 3:
        value_score = 70
    elif distance <= 8:
        value_score = 50
    elif distance <= 15:
        value_score = 25
    else:
        value_score = 0

    if distance > 15:
        value_status = "🔴 EXPENSIVE"
    elif distance > 8:
        value_status = "🟠 PREMIUM"
    elif distance >= -3:
        value_status = "🟡 FAIR"
    elif distance >= -8:
        value_status = "🟢 ATTRACTIVE"
    else:
        value_status = "🟢 DISCOUNT"

    return {
        "reference":reference,
        "value_score":value_score,
        "distance":distance,
        "value_status":value_status,
        "support":support,
        "resistance":resistance,
        "high52":high52,
        "low52":low52
    }

# ============================================================
# ATR RISK + DYNAMIC TARGET ENGINE
# ============================================================

def risk_target_engine(df, price, breakout):

    last = df.iloc[-1]

    cmp = safe_num(last["Close"])

    atr = safe_num(
        last["ATR14"],
        cmp*.03
    )

    support = price["support"]
    resistance = price["resistance"]
    high52 = price["high52"]

    # ATR protection
    atr_stop = cmp - (1.8 * atr)

    support_stop = support * .97

    stop = min(
        atr_stop,
        support_stop
    )

    # Prevent unrealistic stop
    if stop <= 0 or stop >= cmp:
        stop = cmp - (2 * atr)

    # Dynamic entry
    buy_center = (
        safe_num(last["EMA20"],cmp)*.45 +
        safe_num(last["EMA50"],cmp)*.55
    )

    buy_low = max(
        0,
        min(
            support,
            buy_center*.97
        )
    )

    buy_high = max(
        support,
        buy_center*1.01
    )

    dip_low = max(
        0,
        min(
            safe_num(last["EMA50"],cmp)*.97,
            support*.99
        )
    )

    dip_high = max(
        safe_num(last["EMA50"],cmp)*1.01,
        support*1.02
    )

    breakout_entry = breakout["level"]

    # Dynamic swing targets
    swing1 = max(
        resistance*1.03,
        cmp + 1.5*atr
    )

    swing2 = max(
        resistance*1.08,
        cmp + 2.5*atr
    )

    swing3 = max(
        high52*1.05,
        cmp + 3.5*atr
    )

    # Long targets
    long1 = max(
        high52*1.03,
        cmp*1.15
    )

    long2 = max(
        high52*1.10,
        cmp*1.25
    )

    long3 = max(
        high52*1.20,
        cmp*1.40
    )

    risk_amount = max(
        0,
        cmp-stop
    )

    reward = max(
        0,
        swing1-cmp
    )

    rr = (
        reward/risk_amount
        if risk_amount > 0 else 0
    )

    downside = (
        risk_amount/cmp*100
        if cmp > 0 else 0
    )

    return {
        "atr":atr,
        "stop":stop,
        "buy_low":buy_low,
        "buy_high":buy_high,
        "dip_low":dip_low,
        "dip_high":dip_high,
        "breakout":breakout_entry,
        "swing1":swing1,
        "swing2":swing2,
        "swing3":swing3,
        "long1":long1,
        "long2":long2,
        "long3":long3,
        "rr":rr,
        "downside":downside
    }

# ============================================================
# EMS V3.2
# ============================================================

def ems_engine(df):

    last = df.iloc[-1]

    close = safe_num(last["Close"])

    technical = technical_engine(df)

    # --------------------------------------------------------
    # MOMENTUM
    # --------------------------------------------------------

    rsi = safe_num(last["RSI14"],50)
    roc = safe_num(last["ROC20"],0)

    momentum = 50

    if rsi >= 60:
        momentum += 20
    elif rsi >= 50:
        momentum += 10
    elif rsi < 40:
        momentum -= 20

    if roc > 10:
        momentum += 20
    elif roc > 0:
        momentum += 10
    else:
        momentum -= 10

    momentum = max(
        0,
        min(100,momentum)
    )

    if rsi >= 75:
        momentum_grade = "🔴 EXTREME"
    elif momentum >= 75:
        momentum_grade = "🟢 STRONG"
    elif momentum >= 60:
        momentum_grade = "🟡 IMPROVING"
    else:
        momentum_grade = "🔴 WEAK"

    # --------------------------------------------------------
    # SUPPORT
    # --------------------------------------------------------

    support = safe_num(
        last["SUPPORT20"],
        close*.95
    )

    resistance = safe_num(
        last["RESISTANCE20"],
        close*1.05
    )

    support_score = 50

    if close > support:
        support_score += 20

    if close < resistance:
        support_score += 10

    support_score = max(
        0,
        min(100,support_score)
    )

    # --------------------------------------------------------
    # VOLUME
    # --------------------------------------------------------

    volume_ratio = safe_num(
        last["VOLUME_RATIO"],
        0
    )

    if volume_ratio >= 2:
        volume_score = 100
    elif volume_ratio >= 1.5:
        volume_score = 80
    elif volume_ratio >= 1:
        volume_score = 60
    else:
        volume_score = 30

    # --------------------------------------------------------
    # RELATIVE STRENGTH PROXY
    # --------------------------------------------------------

    relative = 50

    if close > safe_num(last["EMA50"],close):
        relative += 20

    if close > safe_num(last["EMA200"],close):
        relative += 20

    relative = max(
        0,
        min(100,relative)
    )

    # --------------------------------------------------------
    # RISK
    # --------------------------------------------------------

    risk = 20

    if close < safe_num(last["EMA20"],close):
        risk += 20

    if rsi < 40:
        risk += 25

    if safe_num(last["MACD"]) < safe_num(
        last["MACD_SIGNAL"]
    ):
        risk += 20

    if volume_ratio < .7:
        risk += 15

    if rsi >= 75:
        risk += 15

    risk = max(
        0,
        min(100,risk)
    )

    # --------------------------------------------------------
    # CPR
    # --------------------------------------------------------

    cpr_low = safe_num(
        last["CPR_LOW"],
        close
    )

    cpr_high = safe_num(
        last["CPR_HIGH"],
        close
    )

    pp = safe_num(
        last["PP"],
        close
    )

    cpr_width = safe_num(
        last["CPR_WIDTH"],
        0
    )

    if close > cpr_high:
        cpr_score = 100
        cpr_status = "🟢 ABOVE"
    elif close < cpr_low:
        cpr_score = 30
        cpr_status = "🔴 BELOW"
    else:
        cpr_score = 60
        cpr_status = "🟡 INSIDE"

    if cpr_width <= .50:
        cpr_type = "🟢 NARROW"
    elif cpr_width <= 1.00:
        cpr_type = "🟡 NORMAL"
    else:
        cpr_type = "🟠 WIDE"

    # --------------------------------------------------------
    # BREAKOUT
    # --------------------------------------------------------

    breakout = breakout_engine(df)

    breakout_score = round(
        breakout["confirmations"]/7*100,
        1
    )

    # --------------------------------------------------------
    # PRICE VALUE
    # --------------------------------------------------------

    value = price_value_engine(df)

    # --------------------------------------------------------
    # D/W/M
    # --------------------------------------------------------

    daily,weekly,monthly,dwm,regime = (
        timeframe_score(df)
    )

    # --------------------------------------------------------
    # RAW EMS
    # --------------------------------------------------------

    raw = (
        technical*.25 +
        momentum*.12 +
        support_score*.08 +
        volume_score*.08 +
        relative*.08 +
        cpr_score*.08 +
        breakout_score*.05 +
        (100-risk)*.09 +
        value["value_score"]*.10 +
        dwm*.07
    )

    ems = round(
        max(0,min(100,raw)),
        1
    )

    # --------------------------------------------------------
    # ACTION ENGINE
    # --------------------------------------------------------

    if rsi >= 75 and volume_ratio < 1:
        decision = "🟠 WAIT / OVERBOUGHT"

    elif ems >= 75 and technical >= 70:
        decision = "🟢 ADD"

    elif ems >= 65:
        decision = "🟢 HOLD / ADD ON DIP"

    elif ems >= 55:
        decision = "🟡 HOLD / WAIT"

    elif ems >= 45:
        decision = "🟠 REDUCE / WAIT"

    else:
        decision = "🔴 EXIT / NO BUY"

    # --------------------------------------------------------
    # ENTRY MODE
    # --------------------------------------------------------

    if rsi >= 75 and volume_ratio < 1:
        entry_mode = "⚠️ WAIT — OVERBOUGHT"

    elif breakout["breakout"] and breakout["volume_confirmed"]:
        entry_mode = "🚀 BREAKOUT ENTRY"

    elif ems >= 65:
        entry_mode = "🟢 BUY ON DIP"

    elif ems >= 55:
        entry_mode = "🟡 WAIT FOR CONFIRMATION"

    else:
        entry_mode = "🔴 NO BUY"

    return {
        "ems":ems,
        "technical":technical,
        "momentum":momentum,
        "momentum_grade":momentum_grade,
        "support_score":support_score,
        "volume_score":volume_score,
        "relative":relative,
        "risk":risk,
        "cpr_score":cpr_score,
        "cpr_status":cpr_status,
        "cpr_type":cpr_type,
        "cpr_width":cpr_width,
        "pp":pp,
        "breakout_score":breakout_score,
        "breakout":breakout,
        "value":value,
        "daily":daily,
        "weekly":weekly,
        "monthly":monthly,
        "dwm":dwm,
        "regime":regime,
        "decision":decision,
        "entry_mode":entry_mode
    }

# ============================================================
# SIGNAL CHANGE
# ============================================================

def signal_class(ems):

    if ems >= 75:
        return "BUY / ADD"
    elif ems >= 65:
        return "HOLD / ADD ON DIP"
    elif ems >= 55:
        return "HOLD / WAIT"
    elif ems >= 45:
        return "REDUCE / WAIT"
    else:
        return "EXIT / NO BUY"

# ============================================================
# FULL ANALYSIS
# ============================================================

def analyze_stock(symbol):

    ticker = symbol.upper().strip()

    if not ticker.endswith(".NS"):
        ticker += ".NS"

    try:

        df = yf.download(
            ticker,
            period="5y",
            interval="1d",
            auto_adjust=False,
            progress=False
        )

        if df is None or df.empty:
            return None

        if isinstance(df.columns,pd.MultiIndex):
            df.columns = (
                df.columns
                .get_level_values(0)
            )

        required = [
            "Open",
            "High",
            "Low",
            "Close",
            "Volume"
        ]

        if any(
            x not in df.columns
            for x in required
        ):
            return None

        df = df.dropna(
            subset=required
        )

        if len(df) < 210:
            return None

        df = calculate_indicators(df)

        ems = ems_engine(df)

        value = ems["value"]

        breakout = ems["breakout"]

        risk = risk_target_engine(
            df,
            value,
            breakout
        )

        return {
            "df":df,
            "ems":ems,
            "price":value,
            "risk":risk
        }

    except Exception:
        return None

# ============================================================
# SESSION STATE
# ============================================================

if "stocks" not in st.session_state:
    st.session_state.stocks = []

if "results" not in st.session_state:
    st.session_state.results = {}

if "previous_signals" not in st.session_state:
    st.session_state.previous_signals = {}

# ============================================================
# WATCHLIST
# ============================================================

st.markdown(
    '<div class="section-title">➕ ADD STOCK</div>',
    unsafe_allow_html=True
)

stock_input = st.text_input(
    "NSE Symbol",
    placeholder="BSE / RATNAVEER / AIIL",
    label_visibility="collapsed"
)

if stock_input:

    symbol = (
        stock_input
        .upper()
        .replace(".NS","")
        .strip()
    )

    if (
        symbol
        and symbol not in st.session_state.stocks
        and len(st.session_state.stocks) < 15
    ):
        st.session_state.stocks.append(symbol)
        st.rerun()

st.markdown(
    f'<div class="section-title">📋 MY STOCKS — '
    f'{len(st.session_state.stocks)}/15</div>',
    unsafe_allow_html=True
)

if st.session_state.stocks:

    st.markdown(
        " • ".join(st.session_state.stocks),
        unsafe_allow_html=True
    )

    if st.button(
        "🗑️ CLEAR WATCHLIST",
        use_container_width=True
    ):
        st.session_state.stocks = []
        st.session_state.results = {}
        st.rerun()

# ============================================================
# ANALYZE
# ============================================================

if st.button(
    "🔍 ANALYZE ALL",
    use_container_width=True
):

    st.session_state.results = {}

    total = len(
        st.session_state.stocks
    )

    progress = st.progress(0)

    for i,symbol in enumerate(
        st.session_state.stocks
    ):

        result = analyze_stock(symbol)

        if result is not None:

            st.session_state.results[
                symbol
            ] = result

        else:

            st.error(
                f"⚠️ {symbol}: Market data unavailable"
            )

        progress.progress(
            int((i+1)/max(total,1)*100)
        )

    st.success("✅ Analysis completed.")

# ============================================================
# DASHBOARD
# ============================================================

if st.session_state.results:

    results = st.session_state.results

    analyzed = len(results)

    positive = sum(
        1 for r in results.values()
        if r["ems"]["ems"] >= 60
    )

    risk_exit = sum(
        1 for r in results.values()
        if r["ems"]["ems"] < 45
    )

    avg_ems = np.mean([
        r["ems"]["ems"]
        for r in results.values()
    ])

    avg_tech = np.mean([
        r["ems"]["technical"]
        for r in results.values()
    ])

    bull = sum(
        1 for r in results.values()
        if r["ems"]["dwm"] >= 65
    )

    bear = analyzed - bull

    st.markdown("---")

    st.markdown(
        '<div class="section-title">'
        '🚦 SMART SIGNAL DASHBOARD'
        '</div>',
        unsafe_allow_html=True
    )

    dash = f"""
    <div class="box-grid">

        {price_box(
            "ANALYZED",
            f"📊 {analyzed}",
            "blue-box"
        )}

        {price_box(
            "POSITIVE",
            f"🟢 {positive}",
            "green-box"
        )}

        {price_box(
            "RISK / EXIT",
            f"⚠️ {risk_exit}",
            "red-box"
        )}

        {price_box(
            "AVG EMS",
            f"🧠 {avg_ems:.0f}/100",
            "yellow-box"
        )}

        {price_box(
            "AVG TECH",
            f"📈 {avg_tech:.0f}/100",
            "blue-box"
        )}

        {price_box(
            "BULL / BEAR",
            f"🐂 {bull} / 🐻 {bear}",
            "blue-box"
        )}

    </div>
    """

    st.markdown(
        dash,
        unsafe_allow_html=True
    )

# ============================================================
# STOCK RESULTS
# ============================================================

for symbol,result in st.session_state.results.items():

    df = result["df"]
    ems = result["ems"]
    price = result["price"]
    risk = result["risk"]

    last = df.iloc[-1]

    cmp = safe_num(
        last["Close"]
    )

    # --------------------------------------------------------
    # SIGNAL
    # --------------------------------------------------------

    if ems["ems"] >= 75:
        regime = "🐂 BULL"
        signal = "🚦 BUY / ADD"

    elif ems["ems"] >= 65:
        regime = "🟢 POSITIVE"
        signal = "🟢 HOLD / ADD ON DIP"

    elif ems["ems"] >= 55:
        regime = "🟡 NEUTRAL"
        signal = "🟡 HOLD / WAIT"

    elif ems["ems"] >= 45:
        regime = "🟠 WEAK"
        signal = "🟠 REDUCE / WAIT"

    else:
        regime = "🐻 BEAR"
        signal = "🔴 EXIT / NO BUY"

    current_signal = signal_class(
        ems["ems"]
    )

    previous_signal = (
        st.session_state
        .previous_signals
        .get(symbol)
    )

    if previous_signal is None:
        signal_change = "🆕 FIRST ANALYSIS"
    elif previous_signal != current_signal:
        signal_change = (
            f"⚡ {previous_signal} → "
            f"{current_signal}"
        )
    else:
        signal_change = "➡️ SIGNAL UNCHANGED"

    st.session_state.previous_signals[
        symbol
    ] = current_signal

    st.markdown("---")

    st.markdown(
        f"## 🏢 {symbol}"
    )

    st.caption(
        f"{symbol}.NS • NSE • Last available close • "
        f"Analysis: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )

    st.markdown(
        f'<div class="signal">{regime} &nbsp; {signal}</div>',
        unsafe_allow_html=True
    )

    st.info(
        f"🔄 Signal Tracker: {signal_change}"
    )

    # --------------------------------------------------------
    # SMART DASHBOARD
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🚦 SMART SIGNAL DASHBOARD'
        '</div>',
        unsafe_allow_html=True
    )

    summary = f"""
    <div class="box-grid">

        {price_box(
            "CMP / CLOSE",
            f"₹{cmp:,.2f}",
            "blue-box"
        )}

        {price_box(
            "EMS",
            f'{ems["ems"]:.0f}/100',
            "green-box"
            if ems["ems"]>=60
            else "red-box"
        )}

        {price_box(
            "TECH",
            f'{ems["technical"]:.0f}/100',
            "green-box"
            if ems["technical"]>=60
            else "red-box"
        )}

        {price_box(
            "RSI",
            f'{safe_num(last["RSI14"],50):.1f}',
            "green-box"
            if safe_num(last["RSI14"],50)<75
            else "red-box"
        )}

        {price_box(
            "VOLUME",
            f'{safe_num(last["VOLUME_RATIO"],0):.2f}x',
            "green-box"
            if safe_num(last["VOLUME_RATIO"],0)>=1.5
            else "yellow-box"
        )}

        {price_box(
            "DECISION",
            ems["decision"],
            "green-box"
            if ems["ems"]>=65
            else "yellow-box"
        )}

    </div>
    """

    st.markdown(
        summary,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # KEY INDICATORS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '📊 KEY INDICATORS'
        '</div>',
        unsafe_allow_html=True
    )

    e10 = safe_num(last["EMA10"])
    e20 = safe_num(last["EMA20"])
    e50 = safe_num(last["EMA50"])
    e100 = safe_num(last["EMA100"])
    e200 = safe_num(last["EMA200"])

    macd_bull = (
        safe_num(last["MACD"])
        >
        safe_num(last["MACD_SIGNAL"])
    )

    st_bull = (
        safe_num(last["SUPERTREND_TREND"])
        == 1
    )

    volume = safe_num(
        last["VOLUME_RATIO"],
        0
    )

    high52 = safe_num(
        last["52W_HIGH"]
    )

    low52 = safe_num(
        last["52W_LOW"]
    )

    key_html = f"""
    <div class="key-grid">

        {html_box(
            "EMA 10",
            f"₹{e10:,.2f}",
            "key-positive"
            if cmp>e10 else "key-negative"
        )}

        {html_box(
            "EMA 20",
            f"₹{e20:,.2f}",
            "key-positive"
            if cmp>e20 else "key-negative"
        )}

        {html_box(
            "EMA 50",
            f"₹{e50:,.2f}",
            "key-positive"
            if cmp>e50 else "key-negative"
        )}

        {html_box(
            "EMA 100",
            f"₹{e100:,.2f}",
            "key-positive"
            if cmp>e100 else "key-negative"
        )}

        {html_box(
            "EMA 200",
            f"₹{e200:,.2f}",
            "key-positive"
            if cmp>e200 else "key-negative"
        )}

        {html_box(
            "RSI 14",
            f'{safe_num(last["RSI14"],50):.1f}',
            "key-positive"
            if safe_num(last["RSI14"],50)>=50
            else "key-negative"
        )}

        {html_box(
            "MACD",
            "🟢 BULL" if macd_bull else "🔴 BEAR",
            "key-positive"
            if macd_bull else "key-negative"
        )}

        {html_box(
            "SUPERTREND",
            "🟢 BULL" if st_bull else "🔴 BEAR",
            "key-positive"
            if st_bull else "key-negative"
        )}

        {html_box(
            "VOLUME",
            f"{volume:.2f}x",
            "key-positive"
            if volume>=1.5 else "key-warning"
        )}

        {html_box(
            "52W HIGH",
            f"₹{high52:,.2f}"
        )}

        {html_box(
            "52W LOW",
            f"₹{low52:,.2f}"
        )}

        {html_box(
            "PRICE vs CPR",
            ems["cpr_status"],
            "key-positive"
            if ems["cpr_score"]>=80
            else "key-negative"
        )}

        {html_box(
            "CPR WIDTH",
            f'{ems["cpr_width"]:.2f}%',
            "key-warning"
        )}

        {html_box(
            "CPR TYPE",
            ems["cpr_type"],
            "key-warning"
        )}

        {html_box(
            "MOMENTUM",
            ems["momentum_grade"],
            "key-positive"
            if ems["momentum"]>=75
            else "key-warning"
        )}

        {html_box(
            "D/W/M REGIME",
            ems["regime"]
        )}

        {html_box(
            "BREAKOUT",
            ems["breakout"]["quality"],
            "key-positive"
            if ems["breakout"]["confirmations"]>=5
            else "key-warning"
        )}

    </div>
    """

    st.markdown(
        key_html,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # PRICE VALUE
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '💰 PRICE VALUE'
        '</div>',
        unsafe_allow_html=True
    )

    pv = f"""
    <div class="box-grid">

        {price_box(
            "CMP / CLOSE",
            f"₹{cmp:,.2f}",
            "blue-box"
        )}

        {price_box(
            "REFERENCE VALUE",
            f"₹{price['reference']:,.2f}",
            "yellow-box"
        )}

        {price_box(
            "VALUE SCORE",
            f'{price["value_score"]}/100',
            "green-box"
            if price["value_score"]>=70
            else "yellow-box"
        )}

        {price_box(
            "VALUE STATUS",
            price["value_status"],
            "green-box"
            if price["value_score"]>=70
            else "red-box"
        )}

        {price_box(
            "VALUE GAP",
            f'{price["distance"]:+.1f}%',
            "green-box"
            if price["distance"]<=3
            else "red-box"
        )}

        {price_box(
            "RISK : REWARD",
            f'1 : {risk["rr"]:.2f}',
            "blue-box"
        )}

    </div>
    """

    st.markdown(
        pv,
        unsafe_allow_html=True
    )

    if price["distance"] > 8:

        st.warning(
            "⚠️ Price Value: CMP reference value કરતાં "
            "ઉપર છે. Fresh chasing ટાળો."
        )

    elif price["value_score"] >= 80:

        st.success(
            "🟢 Price Value attractive zone."
        )

    # --------------------------------------------------------
    # CPR — SINGLE SECTION ONLY
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '📐 CPR — CENTRAL PIVOT RANGE'
        '</div>',
        unsafe_allow_html=True
    )

    cpr_html = f"""
    <div class="box-grid">

        {price_box(
            "PP / PIVOT",
            f'₹{ems["pp"]:,.2f}',
            "blue-box"
        )}

        {price_box(
            "BC",
            f'₹{safe_num(last["BC"]):,.2f}',
            "blue-box"
        )}

        {price_box(
            "TC",
            f'₹{safe_num(last["TC"]):,.2f}',
            "blue-box"
        )}

        {price_box(
            "CPR LOW",
            f'₹{safe_num(last["CPR_LOW"]):,.2f}',
            "blue-box"
        )}

        {price_box(
            "CPR HIGH",
            f'₹{safe_num(last["CPR_HIGH"]):,.2f}',
            "blue-box"
        )}

        {price_box(
            "CPR WIDTH",
            f'{ems["cpr_width"]:.2f}% • {ems["cpr_type"]}',
            "yellow-box"
        )}

    </div>
    """

    st.markdown(
        cpr_html,
        unsafe_allow_html=True
    )

    st.info(
        f"📐 CPR Position: {ems['cpr_status']} • "
        f"CPR Type: {ems['cpr_type']}"
    )

    # --------------------------------------------------------
    # EMS BREAKDOWN
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🧠 EMS V3.2 BREAKDOWN'
        '</div>',
        unsafe_allow_html=True
    )

    ems_html = f"""
    <div class="ems-grid">

        {ems_box(
            "TECHNICAL",
            f'{ems["technical"]:.0f}/100'
        )}

        {ems_box(
            "MOMENTUM",
            f'{ems["momentum"]:.0f}/100'
        )}

        {ems_box(
            "SUPPORT",
            f'{ems["support_score"]:.0f}/100'
        )}

        {ems_box(
            "VOLUME",
            f'{ems["volume_score"]:.0f}/100'
        )}

        {ems_box(
            "RELATIVE",
            f'{ems["relative"]:.0f}/100'
        )}

        {ems_box(
            "CPR",
            f'{ems["cpr_score"]:.0f}/100'
        )}

        {ems_box(
            "BREAKOUT",
            f'{ems["breakout_score"]:.0f}/100'
        )}

        {ems_box(
            "RISK",
            f'{ems["risk"]:.0f}/100'
        )}

        {ems_box(
            "PRICE VALUE",
            f'{price["value_score"]:.0f}/100'
        )}

        {ems_box(
            "D/W/M",
            f'{ems["dwm"]:.0f}/100'
        )}

        {ems_box(
            "FINAL EMS",
            f'{ems["ems"]:.0f}/100'
        )}

    </div>
    """

    st.markdown(
        ems_html,
        unsafe_allow_html=True
    )

    st.info(
        f'🧠 EMS Decision: {ems["decision"]} • '
        f'Daily {ems["daily"]:.0f} | '
        f'Weekly {ems["weekly"]:.0f} | '
        f'Monthly {ems["monthly"]:.0f} | '
        f'Master {ems["dwm"]:.0f}'
    )

    # --------------------------------------------------------
    # RSI WARNING
    # --------------------------------------------------------

    if safe_num(last["RSI14"],50) >= 75:

        st.error(
            "🔴 RSI EXTREME OVERBOUGHT — "
            "fresh ADD ટાળો; dip અથવા confirmationની રાહ જુઓ."
        )

    elif safe_num(last["RSI14"],50) >= 60:

        st.success(
            "🟢 RSI strong momentum."
        )

    # --------------------------------------------------------
    # PRICE LEVELS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🎯 PRICE LEVELS'
        '</div>',
        unsafe_allow_html=True
    )

    levels = f"""
    <div class="box-grid">

        {price_box(
            "SUPPORT",
            f'₹{price["support"]:,.2f}',
            "blue-box"
        )}

        {price_box(
            "RESISTANCE",
            f'₹{price["resistance"]:,.2f}',
            "blue-box"
        )}

        {price_box(
            "52W HIGH",
            f'₹{price["high52"]:,.2f}',
            "yellow-box"
        )}

        {price_box(
            "52W LOW",
            f'₹{price["low52"]:,.2f}',
            "blue-box"
        )}

        {price_box(
            "ATR 14",
            f'₹{risk["atr"]:,.2f}',
            "yellow-box"
        )}

        {price_box(
            "STOP LOSS",
            f'₹{risk["stop"]:,.2f}',
            "red-box"
        )}

    </div>
    """

    st.markdown(
        levels,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # ENTRY + RISK
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🛡️ ENTRY + RISK'
        '</div>',
        unsafe_allow_html=True
    )

    entry = f"""
    <div class="box-grid">

        {price_box(
            "ENTRY MODE",
            ems["entry_mode"],
            "green-box"
            if "BUY" in ems["entry_mode"]
            else "yellow-box"
        )}

        {price_box(
            "BUY ZONE",
            f'₹{risk["buy_low"]:,.0f} – '
            f'₹{risk["buy_high"]:,.0f}',
            "green-box"
        )}

        {price_box(
            "BUY ON DIP",
            f'₹{risk["dip_low"]:,.0f} – '
            f'₹{risk["dip_high"]:,.0f}',
            "green-box"
        )}

        {price_box(
            "BREAKOUT ENTRY",
            f'₹{risk["breakout"]:,.2f}',
            "blue-box"
        )}

        {price_box(
            "ATR STOP",
            f'₹{risk["stop"]:,.2f}',
            "red-box"
        )}

        {price_box(
            "RISK",
            f'{risk["downside"]:.1f}%',
            "red-box"
        )}

    </div>
    """

    st.markdown(
        entry,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # SWING TARGETS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🎯 DYNAMIC SWING TARGETS'
        '</div>',
        unsafe_allow_html=True
    )

    swing = f"""
    <div class="target-grid">

        {target_box(
            "SWING T1",
            risk["swing1"],
            (risk["swing1"]/cmp-1)*100
        )}

        {target_box(
            "SWING T2",
            risk["swing2"],
            (risk["swing2"]/cmp-1)*100
        )}

        {target_box(
            "SWING T3",
            risk["swing3"],
            (risk["swing3"]/cmp-1)*100
        )}

    </div>
    """

    st.markdown(
        swing,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # LONG TARGETS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🏆 LONG-TERM TARGETS'
        '</div>',
        unsafe_allow_html=True
    )

    long_html = f"""
    <div class="target-grid">

        {target_box(
            "LONG T1",
            risk["long1"],
            (risk["long1"]/cmp-1)*100
        )}

        {target_box(
            "LONG T2",
            risk["long2"],
            (risk["long2"]/cmp-1)*100
        )}

        {target_box(
            "LONG T3",
            risk["long3"],
            (risk["long3"]/cmp-1)*100
        )}

    </div>
    """

    st.markdown(
        long_html,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # BREAKOUT + RETEST
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🚀 BREAKOUT QUALITY + RETEST'
        '</div>',
        unsafe_allow_html=True
    )

    br = ems["breakout"]

    br_html = f"""
    <div class="box-grid">

        {price_box(
            "BREAKOUT LEVEL",
            f'₹{br["level"]:,.2f}',
            "blue-box"
        )}

        {price_box(
            "QUALITY",
            br["quality"],
            "green-box"
            if br["confirmations"]>=5
            else "yellow-box"
        )}

        {price_box(
            "CONFIRMATIONS",
            f'{br["confirmations"]}/7',
            "green-box"
            if br["confirmations"]>=5
            else "yellow-box"
        )}

        {price_box(
            "VOLUME",
            "✅ CONFIRMED"
            if br["volume_confirmed"]
            else "⏳ PENDING",
            "green-box"
            if br["volume_confirmed"]
            else "yellow-box"
        )}

        {price_box(
            "RETEST",
            "✅ YES"
            if br["retest"]
            else "⏳ WAIT",
            "green-box"
            if br["retest"]
            else "yellow-box"
        )}

        {price_box(
            "STATUS",
            br["status"],
            "green-box"
            if br["confirmations"]>=5
            else "yellow-box"
        )}

    </div>
    """

    st.markdown(
        br_html,
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="small-note">'
        f'Retest Zone: ₹{br["retest_low"]:,.2f} – '
        f'₹{br["retest_high"]:,.2f}'
        f'</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # D/W/M
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '📅 D / W / M TREND'
        '</div>',
        unsafe_allow_html=True
    )

    dwm_html = f"""
    <div class="box-grid">

        {price_box(
            "DAILY",
            f'{ems["daily"]:.0f}/100',
            "green-box"
            if ems["daily"]>=65
            else "yellow-box"
        )}

        {price_box(
            "WEEKLY",
            f'{ems["weekly"]:.0f}/100',
            "green-box"
            if ems["weekly"]>=65
            else "yellow-box"
        )}

        {price_box(
            "MONTHLY",
            f'{ems["monthly"]:.0f}/100',
            "green-box"
            if ems["monthly"]>=65
            else "yellow-box"
        )}

        {price_box(
            "MASTER",
            f'{ems["dwm"]:.0f}/100',
            "blue-box"
        )}

        {price_box(
            "REGIME",
            ems["regime"],
            "green-box"
            if ems["dwm"]>=65
            else "yellow-box"
        )}

        {price_box(
            "ACTION",
            ems["decision"],
            "green-box"
            if ems["ems"]>=65
            else "yellow-box"
        )}

    </div>
    """

    st.markdown(
        dwm_html,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # CHART
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '📈 PRICE + EMA 10/20/50/100/200'
        '</div>',
        unsafe_allow_html=True
    )

    chart_df = df[
        [
            "Close",
            "EMA10",
            "EMA20",
            "EMA50",
            "EMA100",
            "EMA200"
        ]
    ].tail(180).copy()

    chart_df.index = pd.to_datetime(
        chart_df.index
    )

    chart_df = chart_df.apply(
        pd.to_numeric,
        errors="coerce"
    ).dropna(how="all")

    st.line_chart(
        chart_df,
        use_container_width=True
    )

    # --------------------------------------------------------
    # WHY
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🧠 WHY THIS SIGNAL?'
        '</div>',
        unsafe_allow_html=True
    )

    if cmp > e10 > e20 > e50 > e100 > e200:

        st.success(
            "✅ Full EMA bullish alignment: "
            "10 > 20 > 50 > 100 > 200"
        )

    elif cmp < e10 < e20 < e50 < e100 < e200:

        st.error(
            "🔴 Full EMA bearish alignment: "
            "10 < 20 < 50 < 100 < 200"
        )

    else:

        st.warning(
            "🟡 EMA structure mixed"
        )

    if safe_num(last["RSI14"],50) >= 75:
        st.error(
            "🔴 RSI extreme overbought"
        )

    elif safe_num(last["RSI14"],50) >= 60:
        st.write(
            "🟢 RSI strong"
        )

    elif safe_num(last["RSI14"],50) >= 50:
        st.write(
            "🟢 RSI positive"
        )

    else:
        st.write(
            "🔴 RSI weak"
        )

    if macd_bull:
        st.write(
            "🟢 MACD bullish"
        )
    else:
        st.write(
            "🔴 MACD bearish"
        )

    if st_bull:
        st.write(
            "🟢 Supertrend bullish"
        )
    else:
        st.write(
            "🔴 Supertrend bearish"
        )

    if volume >= 2:
        st.write(
            "🚀 Volume breakout confirmation"
        )
    elif volume >= 1:
        st.write(
            "🟡 Volume improving"
        )
    else:
        st.write(
            "🔴 Volume weak"
        )

    if ems["cpr_type"] == "🟢 NARROW":
        st.write(
            "🟢 Narrow CPR — breakout potential"
        )
    elif ems["cpr_type"] == "🟠 WIDE":
        st.write(
            "🟠 Wide CPR — range is relatively broad"
        )

    if price["value_score"] >= 80:
        st.write(
            "🟢 Price Value attractive"
        )
    elif price["distance"] > 8:
        st.write(
            "🔴 Price Value: CMP above reference value"
        )
    else:
        st.write(
            "🟡 Price Value: neutral"
        )

    if br["confirmations"] >= 5:
        st.write(
            "🚀 Breakout quality strong"
        )
    else:
        st.write(
            "🟡 Breakout confirmation incomplete"
        )

    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    st.caption(
        "🐂 RAJESH STOCK ANALYZER PRO V3.2 MASTER • "
        "NSE Manual Analyzer • EMS V3.2 • "
        "CPR = Central Pivot Range • "
        "ATR Risk • Dynamic Entry + Targets • "
        "Research & decision-support tool • Not financial advice."
    )
