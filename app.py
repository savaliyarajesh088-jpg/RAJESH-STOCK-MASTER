# ============================================================
# 🐂 RAJESH STOCK ANALYZER PRO V3.1 MASTER
# NSE • Manual 1–15 Stocks
# EMS V3.1 • PRICE VALUE • D/W/M
# EMA 10/20/50/100/200
# CPR • RSI • MACD • SUPERTREND
# MOMENTUM • BREAKOUT + RETEST
# SWING + LONG • RISK MANAGEMENT
# MOBILE FIRST • READABILITY FIX
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
    page_title="RAJESH STOCK ANALYZER PRO V3.1",
    page_icon="🐂",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# MASTER CSS
# ============================================================

st.markdown("""
<style>

/* ---------- GLOBAL ---------- */

html, body, [class*="css"] {
    font-family: Arial, sans-serif !important;
}

.stApp {
    background:#050505 !important;
    color:#FFFFFF !important;
}

.main {
    background:#050505 !important;
}

.block-container {
    padding-top:.55rem !important;
    padding-left:.55rem !important;
    padding-right:.55rem !important;
    padding-bottom:2rem !important;
}

/* ---------- FORCE TEXT VISIBILITY ---------- */

h1, h2, h3, h4, h5, h6,
p, span, div, label {
    color:#FFFFFF;
}

.app-title {
    color:#FFFFFF !important;
    font-size:23px;
    font-weight:900;
    line-height:1.2;
    margin-bottom:3px;
}

.app-subtitle {
    color:#D0D0D0 !important;
    font-size:11px;
    font-weight:700;
    opacity:1 !important;
    margin-bottom:10px;
}

.section-title {
    color:#FFFFFF !important;
    font-size:16px;
    font-weight:900;
    margin-top:10px;
    margin-bottom:6px;
}

/* ---------- BOX SYSTEM ---------- */

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
    margin-bottom:8px;
}

.target-grid {
    display:grid;
    grid-template-columns:repeat(3,minmax(0,1fr));
    gap:4px;
    margin-bottom:8px;
}

.ems-grid {
    display:grid;
    grid-template-columns:repeat(5,minmax(0,1fr));
    gap:4px;
    margin-bottom:8px;
}

/* ---------- BOXES ---------- */

.metric-box,
.key-box,
.price-box,
.target-box,
.ems-box {
    border:1px solid #3D3D3D;
    border-radius:7px;
    background:#111111 !important;
    padding:7px 4px;
    text-align:center;
    overflow:hidden;
    box-sizing:border-box;
}

.metric-title,
.key-title,
.price-title,
.target-title,
.ems-title {
    color:#E8E8E8 !important;
    font-size:9px;
    font-weight:900;
    opacity:1 !important;
    white-space:nowrap;
    line-height:1.2;
}

.metric-value,
.key-value,
.price-value,
.target-value,
.ems-value {
    color:#FFFFFF !important;
    font-size:13px;
    font-weight:900;
    margin-top:3px;
    opacity:1 !important;
    white-space:nowrap;
    line-height:1.2;
}

.key-box {
    min-height:55px;
    display:flex;
    flex-direction:column;
    justify-content:center;
}

.key-value {
    font-size:11px;
}

.target-box {
    min-height:58px;
    padding:6px 3px;
}

.target-value {
    font-size:13px;
}

.target-upside {
    color:#FFFFFF !important;
    font-size:10px;
    font-weight:800;
    opacity:1 !important;
    margin-top:2px;
}

.ems-box {
    min-height:54px;
}

.ems-value {
    font-size:11px;
}

/* ---------- SIGNAL BORDERS ---------- */

.green-box,
.key-positive {
    border-color:#19A957 !important;
}

.red-box,
.key-negative {
    border-color:#E03A3A !important;
}

.blue-box {
    border-color:#367BD6 !important;
}

.yellow-box,
.key-warning {
    border-color:#D6A91A !important;
}

.orange-box {
    border-color:#E47C16 !important;
}

/* ---------- SIGNAL ---------- */

.signal {
    color:#FFFFFF !important;
    font-size:19px;
    font-weight:900;
    padding:4px 0;
    opacity:1 !important;
}

/* ---------- ALERTS ---------- */

.notice {
    border:1px solid #555;
    border-radius:7px;
    padding:8px;
    margin:6px 0;
    background:#101010;
    color:#FFFFFF !important;
    font-weight:800;
    font-size:12px;
}

.notice-red {
    border-color:#B72B2B;
}

.notice-yellow {
    border-color:#B68A16;
}

.notice-green {
    border-color:#178944;
}

.notice-blue {
    border-color:#2865A8;
}

/* ---------- MOBILE ---------- */

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

    .block-container {
        padding-left:.35rem !important;
        padding-right:.35rem !important;
    }

    .app-title {
        font-size:18px;
    }

    .app-subtitle {
        font-size:9px;
    }

    .box-grid {
        grid-template-columns:repeat(2,1fr);
        gap:3px;
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

    .key-box,
    .target-box,
    .ems-box {
        min-height:50px;
    }

    .key-title,
    .price-title,
    .target-title,
    .ems-title {
        font-size:8px;
    }

    .key-value,
    .target-value,
    .ems-value {
        font-size:10px;
    }

    .price-value {
        font-size:11px;
    }

    .metric-value {
        font-size:11px;
    }

    .signal {
        font-size:16px;
    }
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="app-title">🐂 RAJESH STOCK ANALYZER PRO V3.1 MASTER</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="app-subtitle">'
    'NSE • Manual 1–15 Stocks • EMS V3.1 • PRICE VALUE • D/W/M • '
    'EMA 10/20/50/100/200 • CPR Central Pivot Range • RSI • MACD • '
    'Supertrend • Momentum • Breakout + Retest • Swing + Long • Risk'
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


def notice(text, css="notice-blue"):
    st.markdown(
        f'<div class="notice {css}">{text}</div>',
        unsafe_allow_html=True
    )

# ============================================================
# INDICATORS
# ============================================================

def calculate_indicators(df):

    df = df.copy()

    close = df["Close"]
    high = df["High"]
    low = df["Low"]

    # --------------------------------------------------------
    # EMA
    # --------------------------------------------------------

    for p in [10,20,50,100,200]:
        df[f"EMA{p}"] = close.ewm(
            span=p,
            adjust=False
        ).mean()

    # --------------------------------------------------------
    # RSI 14
    # --------------------------------------------------------

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
        100/(1+rs)
    )

    # --------------------------------------------------------
    # MACD
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # VOLUME
    # --------------------------------------------------------

    df["VOLUME_AVG20"] = (
        df["Volume"].rolling(20).mean()
    )

    df["VOLUME_RATIO"] = (
        df["Volume"] /
        df["VOLUME_AVG20"].replace(0,np.nan)
    )

    # --------------------------------------------------------
    # 52 WEEK
    # --------------------------------------------------------

    df["52W_HIGH"] = (
        close.rolling(252).max()
    )

    df["52W_LOW"] = (
        close.rolling(252).min()
    )

    # --------------------------------------------------------
    # CPR
    # --------------------------------------------------------

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
        (df["CPR_HIGH"] -
         df["CPR_LOW"]) /
        df["PP"] * 100
    )

    # --------------------------------------------------------
    # SUPPORT / RESISTANCE
    # --------------------------------------------------------

    df["SUPPORT20"] = (
        low.rolling(20).min()
    )

    df["RESISTANCE20"] = (
        high.rolling(20).max()
    )

    # --------------------------------------------------------
    # SUPERTREND
    # --------------------------------------------------------

    period = 10
    multiplier = 3.0

    tr1 = high-low
    tr2 = (high-close.shift()).abs()
    tr3 = (low-close.shift()).abs()

    tr = pd.concat(
        [tr1,tr2,tr3],
        axis=1
    ).max(axis=1)

    atr = tr.rolling(period).mean()

    hl2 = (high+low)/2

    upper = hl2 + multiplier*atr
    lower = hl2 - multiplier*atr

    st_line = pd.Series(
        index=df.index,
        dtype=float
    )

    trend = pd.Series(
        index=df.index,
        dtype=int
    )

    trend.iloc[0] = 1
    st_line.iloc[0] = lower.iloc[0]

    for i in range(1,len(df)):

        if close.iloc[i] > upper.iloc[i-1]:
            trend.iloc[i] = 1

        elif close.iloc[i] < lower.iloc[i-1]:
            trend.iloc[i] = -1

        else:
            trend.iloc[i] = trend.iloc[i-1]

        if trend.iloc[i] == 1:
            st_line.iloc[i] = lower.iloc[i]
        else:
            st_line.iloc[i] = upper.iloc[i]

    df["SUPERTREND_LINE"] = st_line
    df["SUPERTREND_TREND"] = trend

    # --------------------------------------------------------
    # MOMENTUM
    # --------------------------------------------------------

    df["ROC20"] = (
        close.pct_change(20)*100
    )

    return df

# ============================================================
# D/W/M
# ============================================================

def timeframe_score(df):

    def one_score(data):

        if len(data) < 60:
            return 50

        last = data.iloc[-1]

        c = safe_num(last["Close"])
        e20 = safe_num(last["EMA20"])
        e50 = safe_num(last["EMA50"])

        score = 50

        if c > e20:
            score += 15
        else:
            score -= 15

        if e20 > e50:
            score += 15
        else:
            score -= 15

        rsi = safe_num(
            last["RSI14"],
            50
        )

        if 55 <= rsi < 70:
            score += 10
        elif rsi >= 70:
            score += 5
        elif rsi < 40:
            score -= 10

        return max(0,min(100,score))

    daily = one_score(df)

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

    weekly_score = one_score(weekly)
    monthly_score = one_score(monthly)

    master = round(
        daily*.40 +
        weekly_score*.30 +
        monthly_score*.30,
        1
    )

    return (
        daily,
        weekly_score,
        monthly_score,
        master
    )

# ============================================================
# BREAKOUT ENGINE
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

    breakout_level = resistance*1.003

    breakout = close >= breakout_level

    previous_resistance = safe_num(
        df["RESISTANCE20"].iloc[-2]
        if len(df)>1
        else resistance,
        resistance
    )

    retest_low = previous_resistance*.985
    retest_high = previous_resistance*1.015

    retest = (
        breakout and
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

    if close > safe_num(last["EMA20"]):
        confirmations += 1

    if safe_num(last["RSI14"],50) >= 55:
        confirmations += 1

    if safe_num(last["MACD"]) > safe_num(
        last["MACD_SIGNAL"]
    ):
        confirmations += 1

    if safe_num(
        last["SUPERTREND_TREND"]
    ) == 1:
        confirmations += 1

    if breakout and volume_confirmed and retest:
        status = "🚀 CONFIRMED"

    elif breakout and volume_confirmed:
        status = "🚀 BREAKOUT"

    elif breakout:
        status = "🟡 VOLUME PENDING"

    else:
        status = "🟡 WATCH"

    return {
        "level":breakout_level,
        "breakout":breakout,
        "retest":retest,
        "volume_confirmed":volume_confirmed,
        "confirmations":confirmations,
        "retest_low":retest_low,
        "retest_high":retest_high,
        "status":status
    }

# ============================================================
# TECHNICAL ENGINE
# ============================================================

def technical_engine(df):

    last = df.iloc[-1]

    close = safe_num(last["Close"])

    e10 = safe_num(last["EMA10"])
    e20 = safe_num(last["EMA20"])
    e50 = safe_num(last["EMA50"])
    e100 = safe_num(last["EMA100"])
    e200 = safe_num(last["EMA200"])

    rsi = safe_num(
        last["RSI14"],
        50
    )

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
    if 60 <= rsi < 70:
        score += 15
    elif 50 <= rsi < 60:
        score += 10
    elif rsi >= 70:
        score += 8
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
# PRICE VALUE
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

    # Value score
    premium = (
        (cmp/reference)-1
    )*100 if reference > 0 else 0

    if premium <= -10:
        value_score = 100
    elif premium <= 0:
        value_score = 80
    elif premium <= 10:
        value_score = 60
    elif premium <= 20:
        value_score = 30
    else:
        value_score = 0

    exit_price = min(
        e50,
        support*1.02
    )

    stop_loss = support*.97

    buy_center = (
        e20*.40 +
        e50*.60
    )

    buy_low = min(
        support,
        buy_center*.97
    )

    buy_high = max(
        support,
        buy_center*1.01
    )

    dip_low = min(
        e50*.97,
        support*.99
    )

    dip_high = max(
        e50*1.01,
        support*1.02
    )

    breakout = resistance*1.003

    swing1 = max(
        resistance*1.03,
        cmp*1.03
    )

    swing2 = max(
        resistance*1.08,
        swing1*1.05
    )

    swing3 = max(
        high52*1.05,
        swing2*1.05
    )

    # Validation
    swing2 = max(swing2,swing1*1.01)
    swing3 = max(swing3,swing2*1.01)

    long1 = max(
        high52*1.03,
        cmp*1.15
    )

    long2 = max(
        high52*1.10,
        long1*1.08
    )

    long3 = max(
        high52*1.20,
        long2*1.10
    )

    upside = (
        (reference/cmp)-1
    )*100

    downside = (
        (cmp-stop_loss)/cmp
    )*100

    reward = max(
        0,
        swing1-cmp
    )

    risk = max(
        0,
        cmp-stop_loss
    )

    rr = (
        reward/risk
        if risk > 0
        else 0
    )

    return {
        "reference":reference,
        "value_score":value_score,
        "premium":premium,
        "exit":exit_price,
        "stop":stop_loss,
        "buy_low":buy_low,
        "buy_high":buy_high,
        "dip_low":dip_low,
        "dip_high":dip_high,
        "breakout":breakout,
        "support":support,
        "resistance":resistance,
        "high52":high52,
        "low52":low52,
        "swing1":swing1,
        "swing2":swing2,
        "swing3":swing3,
        "long1":long1,
        "long2":long2,
        "long3":long3,
        "upside":upside,
        "downside":downside,
        "rr":rr
    }

# ============================================================
# EMS V3.1
# ============================================================

def ems_engine(df):

    last = df.iloc[-1]

    close = safe_num(last["Close"])

    technical = technical_engine(df)

    # --------------------------------------------------------
    # MOMENTUM
    # --------------------------------------------------------

    rsi = safe_num(
        last["RSI14"],
        50
    )

    roc = safe_num(
        last["ROC20"],
        0
    )

    momentum = 50

    if 60 <= rsi < 70:
        momentum += 20
    elif rsi >= 70:
        momentum += 10
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
    # RELATIVE
    # --------------------------------------------------------

    relative = 50

    if close > safe_num(last["EMA50"]):
        relative += 20

    if close > safe_num(last["EMA200"]):
        relative += 20

    relative = max(
        0,
        min(100,relative)
    )

    # --------------------------------------------------------
    # RISK
    # --------------------------------------------------------

    risk = 20

    if close < safe_num(last["EMA20"]):
        risk += 20

    if rsi < 40:
        risk += 25

    if rsi >= 75:
        risk += 15

    if safe_num(last["MACD"]) < safe_num(
        last["MACD_SIGNAL"]
    ):
        risk += 20

    if volume_ratio < .7:
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

    if cpr_width <= 0.5:
        cpr_type = "🟢 NARROW"
    elif cpr_width <= 1.0:
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

    price = price_value_engine(df)

    value_score = price["value_score"]

    # --------------------------------------------------------
    # FINAL EMS
    # --------------------------------------------------------

    raw = (
        technical*.25 +
        momentum*.12 +
        support_score*.10 +
        volume_score*.08 +
        relative*.08 +
        cpr_score*.08 +
        breakout_score*.05 +
        (100-risk)*.10 +
        value_score*.14
    )

    ems = round(
        max(0,min(100,raw)),
        1
    )

    # --------------------------------------------------------
    # DECISION GUARD
    # --------------------------------------------------------

    if rsi >= 80:
        if breakout["breakout"] and breakout["volume_confirmed"]:
            decision = "🟡 WAIT / CONFIRM"
        else:
            decision = "🟠 WAIT / OVERBOUGHT"

    elif ems >= 75 and technical >= 70:
        decision = "🟢 ADD"

    elif ems >= 60:
        decision = "🟢 HOLD"

    elif ems >= 45:
        decision = "🟠 REDUCE / WAIT"

    else:
        decision = "🔴 EXIT / NO BUY"

    return {
        "ems":ems,
        "technical":technical,
        "momentum":momentum,
        "support_score":support_score,
        "volume_score":volume_score,
        "relative":relative,
        "risk":risk,
        "cpr_score":cpr_score,
        "cpr_status":cpr_status,
        "cpr_width":cpr_width,
        "cpr_type":cpr_type,
        "breakout_score":breakout_score,
        "breakout":breakout,
        "value_score":value_score,
        "decision":decision
    }

# ============================================================
# DATA ANALYSIS
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

        if isinstance(
            df.columns,
            pd.MultiIndex
        ):
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

        missing = [
            x for x in required
            if x not in df.columns
        ]

        if missing:
            return None

        df = df.dropna(
            subset=required
        )

        if len(df) < 210:
            return None

        df = calculate_indicators(df)

        ems = ems_engine(df)

        price = price_value_engine(df)

        d,w,m,master = timeframe_score(df)

        return {
            "df":df,
            "ems":ems,
            "price":price,
            "daily":d,
            "weekly":w,
            "monthly":m,
            "dwm":master
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

# ============================================================
# ADD STOCK
# ============================================================

st.markdown(
    '<div class="section-title">➕ ADD STOCK</div>',
    unsafe_allow_html=True
)

stock_input = st.text_input(
    "NSE Symbol",
    placeholder="BSE / RATNAVEER / AIIL"
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

st.markdown(
    f'<div class="section-title">'
    f'📋 MY STOCKS — {len(st.session_state.stocks)}/15'
    f'</div>',
    unsafe_allow_html=True
)

if st.session_state.stocks:
    st.markdown(
        f'<div class="notice notice-blue">'
        f'{" • ".join(st.session_state.stocks)}'
        f'</div>',
        unsafe_allow_html=True
    )

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
            int(
                (i+1) /
                max(total,1) *
                100
            )
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
        if r["ems"]["technical"] >= 70
    )

    bear = analyzed-bull

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

    last = df.iloc[-1]

    cmp = safe_num(
        last["Close"]
    )

    rsi = safe_num(
        last["RSI14"],
        50
    )

    volume = safe_num(
        last["VOLUME_RATIO"],
        0
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
        safe_num(
            last["SUPERTREND_TREND"]
        ) == 1
    )

    # --------------------------------------------------------
    # SIGNAL
    # --------------------------------------------------------

    if rsi >= 80:
        regime = "🟡 NEUTRAL"
        signal = "🟠 OVERBOUGHT / WAIT"

    elif ems["ems"] >= 75:
        regime = "🐂 BULL"
        signal = "🚦 BUY / ADD"

    elif ems["ems"] >= 60:
        regime = "🟢 POSITIVE"
        signal = "🟢 HOLD"

    elif ems["ems"] >= 45:
        regime = "🟡 NEUTRAL"
        signal = "🟠 REDUCE / WAIT"

    else:
        regime = "🐻 BEAR"
        signal = "🔴 EXIT / NO BUY"

    st.markdown("---")

    st.markdown(
        f"## 🏢 {symbol}"
    )

    st.caption(
        f"{symbol}.NS • NSE • Last available close • "
        f"Analysis: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )

    st.markdown(
        f'<div class="signal">'
        f'{regime} &nbsp; {signal}'
        f'</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # OVERBOUGHT WARNING
    # --------------------------------------------------------

    if rsi >= 80:

        notice(
            "🔴 RSI EXTREME OVERBOUGHT — fresh ADD ટાળો; "
            "confirmation અથવા dipની રાહ જુઓ.",
            "notice-red"
        )

    elif rsi >= 70:

        notice(
            "🟡 RSI OVERBOUGHT — fresh entryમાં confirmation જરૂરી.",
            "notice-yellow"
        )

    # --------------------------------------------------------
    # SUMMARY
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
            f'{rsi:.1f}',
            "red-box"
            if rsi>=70
            else "green-box"
        )}

        {price_box(
            "VOLUME",
            f'{volume:.2f}x',
            "green-box"
            if volume>=1.5
            else "yellow-box"
        )}

        {price_box(
            "DECISION",
            ems["decision"],
            "green-box"
            if ems["ems"]>=60 and rsi<80
            else "orange-box"
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
            f"{rsi:.1f}",
            "key-negative"
            if rsi>=70
            else "key-positive"
        )}

        {html_box(
            "MACD",
            "🟢 BULL"
            if macd_bull
            else "🔴 BEAR",
            "key-positive"
            if macd_bull
            else "key-negative"
        )}

        {html_box(
            "SUPERTREND",
            "🟢 BULL"
            if st_bull
            else "🔴 BEAR",
            "key-positive"
            if st_bull
            else "key-negative"
        )}

        {html_box(
            "VOLUME",
            f"{volume:.2f}x",
            "key-positive"
            if volume>=1.5
            else "key-warning"
        )}

        {html_box(
            "52W HIGH",
            f"₹{safe_num(last['52W_HIGH']):,.2f}"
        )}

        {html_box(
            "52W LOW",
            f"₹{safe_num(last['52W_LOW']):,.2f}"
        )}

        {html_box(
            "PRICE vs CPR",
            ems["cpr_status"],
            "key-positive"
            if ems["cpr_score"]>=80
            else "key-warning"
        )}

        {html_box(
            "CPR WIDTH",
            f'{ems["cpr_width"]:.2f}%',
            "key-warning"
            if ems["cpr_width"]>1
            else "key-positive"
        )}

        {html_box(
            "CPR TYPE",
            ems["cpr_type"]
        )}

        {html_box(
            "BREAKOUT",
            ems["breakout"]["status"],
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
            if price["value_score"]>=60
            else "red-box"
        )}

        {price_box(
            "UPSIDE",
            f'{price["upside"]:+.1f}%',
            "green-box"
            if price["upside"]>0
            else "red-box"
        )}

        {price_box(
            "DOWNSIDE RISK",
            f'{price["downside"]:.1f}%',
            "red-box"
        )}

        {price_box(
            "RISK : REWARD",
            f'1 : {price["rr"]:.2f}',
            "blue-box"
        )}

    </div>
    """

    st.markdown(
        pv,
        unsafe_allow_html=True
    )

    if price["value_score"] <= 30:

        notice(
            "⚠️ PRICE VALUE WARNING: CMP reference value કરતાં "
            "નોંધપાત્ર ઉપર છે.",
            "notice-red"
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
            f'₹{safe_num(last["PP"]):,.2f}',
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
            f'{ems["cpr_width"]:.2f}%',
            "yellow-box"
        )}

    </div>
    """

    st.markdown(
        cpr_html,
        unsafe_allow_html=True
    )

    notice(
        f'📐 CPR TYPE: {ems["cpr_type"]} • '
        f'PRICE: {ems["cpr_status"]}',
        "notice-blue"
    )

    # --------------------------------------------------------
    # EMS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🧠 EMS V3.1 BREAKDOWN'
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
            f'{ems["value_score"]:.0f}/100'
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
        f'Daily {result["daily"]:.0f} | '
        f'Weekly {result["weekly"]:.0f} | '
        f'Monthly {result["monthly"]:.0f} | '
        f'Master {result["dwm"]:.0f}'
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
            "STOP LOSS",
            f'₹{price["stop"]:,.2f}',
            "red-box"
        )}

        {price_box(
            "BREAKOUT",
            f'₹{price["breakout"]:,.2f}',
            "blue-box"
        )}

    </div>
    """

    st.markdown(
        levels,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # ENTRY
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🛡️ ENTRY + RISK'
        '</div>',
        unsafe_allow_html=True
    )

    if rsi >= 80:

        entry = f"""
        <div class="box-grid">

            {price_box(
                "STATUS",
                "⚠️ WAIT — OVERBOUGHT",
                "orange-box"
            )}

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
                "STOP LOSS",
                f'₹{price["stop"]:,.2f}',
                "red-box"
            )}

        </div>
        """

    elif ems["ems"] < 45:

        entry = f"""
        <div class="box-grid">

            {price_box(
                "STATUS",
                "🚫 NO BUY",
                "red-box"
            )}

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
                "STOP LOSS",
                f'₹{price["stop"]:,.2f}',
                "red-box"
            )}

        </div>
        """

    else:

        entry = f"""
        <div class="box-grid">

            {price_box(
                "BUY ZONE",
                f'₹{price["buy_low"]:,.0f} – '
                f'₹{price["buy_high"]:,.0f}',
                "green-box"
            )}

            {price_box(
                "BUY ON DIP",
                f'₹{price["dip_low"]:,.0f} – '
                f'₹{price["dip_high"]:,.0f}',
                "green-box"
            )}

            {price_box(
                "BREAKOUT ENTRY",
                f'₹{price["breakout"]:,.2f}',
                "blue-box"
            )}

            {price_box(
                "STOP LOSS",
                f'₹{price["stop"]:,.2f}',
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
        '🎯 SWING TARGETS'
        '</div>',
        unsafe_allow_html=True
    )

    swing = f"""
    <div class="target-grid">

        {target_box(
            "SWING T1",
            price["swing1"],
            (price["swing1"]/cmp-1)*100
        )}

        {target_box(
            "SWING T2",
            price["swing2"],
            (price["swing2"]/cmp-1)*100
        )}

        {target_box(
            "SWING T3",
            price["swing3"],
            (price["swing3"]/cmp-1)*100
        )}

    </div>
    """

    st.markdown(
        swing,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # LONG
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
            price["long1"],
            (price["long1"]/cmp-1)*100
        )}

        {target_box(
            "LONG T2",
            price["long2"],
            (price["long2"]/cmp-1)*100
        )}

        {target_box(
            "LONG T3",
            price["long3"],
            (price["long3"]/cmp-1)*100
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
        '🚀 BREAKOUT + RETEST'
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
            "RETEST ZONE",
            f'₹{br["retest_low"]:,.2f} – '
            f'₹{br["retest_high"]:,.2f}',
            "blue-box"
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
            f'{result["daily"]:.0f}/100',
            "green-box"
            if result["daily"]>=65
            else "yellow-box"
        )}

        {price_box(
            "WEEKLY",
            f'{result["weekly"]:.0f}/100',
            "green-box"
            if result["weekly"]>=65
            else "yellow-box"
        )}

        {price_box(
            "MONTHLY",
            f'{result["monthly"]:.0f}/100',
            "green-box"
            if result["monthly"]>=65
            else "yellow-box"
        )}

        {price_box(
            "MASTER",
            f'{result["dwm"]:.0f}/100',
            "blue-box"
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

    chart_df = chart_df.apply(
        pd.to_numeric,
        errors="coerce"
    ).dropna()

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

    if rsi >= 80:
        st.write("🔴 RSI extreme overbought")

    elif rsi >= 70:
        st.write("🟠 RSI overbought")

    elif rsi >= 60:
        st.write("🟢 RSI strong")

    elif rsi >= 50:
        st.write("🟢 RSI positive")

    else:
        st.write("🔴 RSI weak")

    if macd_bull:
        st.write("🟢 MACD bullish")
    else:
        st.write("🔴 MACD bearish")

    if st_bull:
        st.write("🟢 Supertrend bullish")
    else:
        st.write("🔴 Supertrend bearish")

    if volume >= 2:
        st.write("🚀 Volume breakout confirmation")
    elif volume >= 1:
        st.write("🟡 Volume improving")
    else:
        st.write("🔴 Volume weak")

    if price["value_score"] >= 60:
        st.write("🟢 Price Value acceptable")
    else:
        st.write("🔴 Price Value: CMP above reference")

    if ems["cpr_width"] <= .5:
        st.write("🟢 Narrow CPR — breakout potential")
    elif ems["cpr_width"] <= 1:
        st.write("🟡 Normal CPR")
    else:
        st.write("🟠 Wide CPR — range relatively broad")

    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    st.caption(
        "🐂 RAJESH STOCK ANALYZER PRO V3.1 MASTER • "
        "NSE Manual Analyzer • EMS V3.1 • "
        "CPR = Central Pivot Range • "
        "Research & decision-support tool • Not financial advice."
    )
