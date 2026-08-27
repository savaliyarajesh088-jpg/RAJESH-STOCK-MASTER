# ============================================================
# 🐂 RAJESH STOCK ANALYZER PRO V3.3 MASTER
# NSE ONLY • MANUAL 1–15 STOCKS
# EMS V3.3 • EXITMANTRA STYLE DECISION ENGINE
# BULL / PIG / BEAR • ADD / HOLD / REPLACE / EXIT
# SWING SCORE • LONG SCORE • D/W/M
# EMA 10/20/50/100/200 • RSI 14 • MACD 12/26/9
# SUPERTREND 10/3 • CPR • VOLUME • 52W
# BREAKOUT + RETEST • ATR RISK
# DYNAMIC ENTRY • SL • SWING TARGETS • LONG TARGETS
# MOBILE-FIRST • SINGLE CPR • PRICE VALUE
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
    page_title="RAJESH STOCK ANALYZER PRO V3.3",
    page_icon="🐂",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CSS
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
    padding:.55rem !important;
    max-width:1500px !important;
}

.app-title {
    font-size:24px;
    font-weight:900;
    color:#FFFFFF;
    line-height:1.2;
}

.app-subtitle {
    font-size:11px;
    color:#D0D0D0;
    line-height:1.5;
}

.section-title {
    font-size:17px;
    font-weight:900;
    color:#FFFFFF;
    margin-top:12px;
    margin-bottom:6px;
}

.grid6 {
    display:grid;
    grid-template-columns:repeat(6,1fr);
    gap:5px;
    margin-bottom:7px;
}

.grid5 {
    display:grid;
    grid-template-columns:repeat(5,1fr);
    gap:4px;
    margin-bottom:7px;
}

.grid3 {
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:5px;
    margin-bottom:7px;
}

.box {
    border:1px solid #3A3A3A;
    background:#111111;
    border-radius:8px;
    padding:7px 4px;
    text-align:center;
    overflow:hidden;
}

.title {
    font-size:9px;
    font-weight:900;
    color:#D8D8D8;
    white-space:nowrap;
}

.value {
    font-size:13px;
    font-weight:900;
    color:#FFFFFF;
    margin-top:3px;
    white-space:nowrap;
}

.green {border-color:#218545;}
.red {border-color:#A83232;}
.blue {border-color:#376AA5;}
.yellow {border-color:#9A7B1B;}
.orange {border-color:#B2671A;}

.big-signal {
    font-size:21px;
    font-weight:900;
    padding:5px 0;
}

.small {
    font-size:10px;
    font-weight:700;
    color:#D0D0D0;
}

@media(max-width:900px) {
    .grid6 {grid-template-columns:repeat(3,1fr);}
    .grid5 {grid-template-columns:repeat(3,1fr);}
}

@media(max-width:500px) {

    .app-title {font-size:18px;}
    .app-subtitle {font-size:10px;}

    .grid6 {
        grid-template-columns:repeat(2,1fr);
        gap:4px;
    }

    .grid5 {
        grid-template-columns:repeat(3,1fr);
        gap:3px;
    }

    .grid3 {
        gap:3px;
    }

    .box {
        padding:6px 3px;
    }

    .title {
        font-size:8px;
    }

    .value {
        font-size:11px;
    }

    .big-signal {
        font-size:18px;
    }
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="app-title">🐂 RAJESH STOCK ANALYZER PRO V3.3 MASTER</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="app-subtitle">'
    'NSE ONLY • EMS V3.3 • EXITMANTRA STYLE • '
    'BULL / PIG / BEAR • ADD / HOLD / REPLACE / EXIT • '
    'SWING SCORE + LONG SCORE • D/W/M • '
    'EMA 10/20/50/100/200 • RSI • MACD • SUPERTREND • CPR • '
    'BREAKOUT + RETEST • ATR RISK • DYNAMIC TARGETS'
    '</div>',
    unsafe_allow_html=True
)

# ============================================================
# HELPERS
# ============================================================

def safe_num(value, default=0.0):
    try:
        if value is None or pd.isna(value):
            return default
        return float(value)
    except:
        return default


def box(title, value, css=""):
    return f"""
    <div class="box {css}">
        <div class="title">{title}</div>
        <div class="value">{value}</div>
    </div>
    """


def target_box(title, price, upside):
    return f"""
    <div class="box">
        <div class="title">{title}</div>
        <div class="value">₹{price:,.2f}</div>
        <div class="small">{upside:+.1f}%</div>
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
        100 / (1 + rs)
    )

    df["RSI14"] = df["RSI14"].fillna(50)

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

    df["VOLUME_AVG20"] = volume.rolling(20).mean()

    df["VOLUME_RATIO"] = (
        volume /
        df["VOLUME_AVG20"].replace(0,np.nan)
    ).fillna(0)

    # --------------------------------------------------------
    # 52 WEEK
    # --------------------------------------------------------

    df["52W_HIGH"] = close.rolling(252).max()
    df["52W_LOW"] = close.rolling(252).min()

    # --------------------------------------------------------
    # CPR
    # SINGLE SOURCE
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
        (
            df["CPR_HIGH"] -
            df["CPR_LOW"]
        )
        /
        df["PP"].replace(0,np.nan)
    ) * 100

    # --------------------------------------------------------
    # SUPPORT / RESISTANCE
    # --------------------------------------------------------

    df["SUPPORT20"] = low.rolling(20).min()
    df["RESISTANCE20"] = high.rolling(20).max()

    # --------------------------------------------------------
    # ATR
    # --------------------------------------------------------

    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()

    true_range = pd.concat(
        [tr1,tr2,tr3],
        axis=1
    ).max(axis=1)

    df["TR"] = true_range

    df["ATR14"] = true_range.rolling(14).mean()

    # --------------------------------------------------------
    # SUPERTREND 10 / 3
    # --------------------------------------------------------

    period = 10
    multiplier = 3

    atr_st = true_range.rolling(
        period
    ).mean()

    hl2 = (
        high + low
    ) / 2

    upper = (
        hl2 +
        multiplier * atr_st
    )

    lower = (
        hl2 -
        multiplier * atr_st
    )

    trend = pd.Series(
        index=df.index,
        dtype=float
    )

    st_line = pd.Series(
        index=df.index,
        dtype=float
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

    df["SUPERTREND_TREND"] = trend
    df["SUPERTREND_LINE"] = st_line

    # --------------------------------------------------------
    # MOMENTUM
    # --------------------------------------------------------

    df["ROC20"] = (
        close.pct_change(20) * 100
    )

    df["EMA20_SLOPE"] = (
        df["EMA20"].pct_change(10) * 100
    )

    return df

# ============================================================
# TIMEFRAME ENGINE
# ============================================================

def timeframe_score(data):

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

    return max(
        0,
        min(100,score)
    )


def dwm_engine(df):

    daily = timeframe_score(df)

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

    weekly = calculate_indicators(
        weekly
    )

    monthly = calculate_indicators(
        monthly
    )

    weekly_score = timeframe_score(
        weekly
    )

    monthly_score = timeframe_score(
        monthly
    )

    master = round(
        daily*.40 +
        weekly_score*.30 +
        monthly_score*.30,
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
    signal = safe_num(
        last["MACD_SIGNAL"]
    )

    volume = safe_num(
        last["VOLUME_RATIO"]
    )

    st = safe_num(
        last["SUPERTREND_TREND"]
    )

    score = 0

    # EMA alignment = 40%
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
    if macd > signal:
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
# MOMENTUM ENGINE
# ============================================================

def momentum_engine(df):

    last = df.iloc[-1]

    rsi = safe_num(
        last["RSI14"],
        50
    )

    roc = safe_num(
        last["ROC20"],
        0
    )

    slope = safe_num(
        last["EMA20_SLOPE"],
        0
    )

    score = 50

    if rsi >= 60:
        score += 20

    elif rsi >= 50:
        score += 10

    elif rsi < 40:
        score -= 20

    if roc > 10:
        score += 15

    elif roc > 0:
        score += 8

    else:
        score -= 10

    if slope > 2:
        score += 15

    elif slope > 0:
        score += 8

    else:
        score -= 8

    score = max(
        0,
        min(100,score)
    )

    if score >= 75:
        grade = "🟢 STRONG"

    elif score >= 60:
        grade = "🟡 IMPROVING"

    elif score >= 45:
        grade = "🟠 WEAK"

    else:
        grade = "🔴 VERY WEAK"

    return score,grade

# ============================================================
# BREAKOUT + RETEST
# ============================================================

def breakout_engine(df):

    last = df.iloc[-1]

    close = safe_num(last["Close"])

    resistance = safe_num(
        last["RESISTANCE20"],
        close
    )

    volume = safe_num(
        last["VOLUME_RATIO"]
    )

    rsi = safe_num(
        last["RSI14"],
        50
    )

    macd = safe_num(
        last["MACD"]
    )

    macd_signal = safe_num(
        last["MACD_SIGNAL"]
    )

    ema20 = safe_num(
        last["EMA20"],
        close
    )

    st = safe_num(
        last["SUPERTREND_TREND"]
    )

    level = resistance * 1.003

    breakout = close >= level

    previous_resistance = resistance

    if len(df) > 1:
        previous_resistance = safe_num(
            df["RESISTANCE20"].iloc[-2],
            resistance
        )

    retest_low = (
        previous_resistance * .985
    )

    retest_high = (
        previous_resistance * 1.015
    )

    retest = (
        retest_low <= close <= retest_high
    )

    volume_confirmed = (
        volume >= 2
    )

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

    score = round(
        confirmations / 7 * 100,
        1
    )

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
        status = "🟡 BREAKOUT PENDING"

    else:
        status = "🟡 WATCH"

    return {
        "level":level,
        "breakout":breakout,
        "retest":retest,
        "retest_low":retest_low,
        "retest_high":retest_high,
        "volume_confirmed":volume_confirmed,
        "confirmations":confirmations,
        "score":score,
        "quality":quality,
        "status":status
    }

# ============================================================
# PRICE VALUE
# ============================================================

def price_value_engine(df):

    last = df.iloc[-1]

    cmp = safe_num(
        last["Close"]
    )

    e20 = safe_num(
        last["EMA20"],
        cmp
    )

    e50 = safe_num(
        last["EMA50"],
        cmp
    )

    e100 = safe_num(
        last["EMA100"],
        cmp
    )

    e200 = safe_num(
        last["EMA200"],
        cmp
    )

    resistance = safe_num(
        last["RESISTANCE20"],
        cmp*1.05
    )

    high52 = safe_num(
        last["52W_HIGH"],
        resistance
    )

    support = safe_num(
        last["SUPPORT20"],
        cmp*.95
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

    gap = (
        (cmp-reference) /
        reference * 100
        if reference > 0
        else 0
    )

    if gap <= -15:
        score = 100

    elif gap <= -8:
        score = 90

    elif gap <= -3:
        score = 80

    elif gap <= 3:
        score = 70

    elif gap <= 8:
        score = 50

    elif gap <= 15:
        score = 25

    else:
        score = 0

    if gap > 15:
        status = "🔴 EXPENSIVE"

    elif gap > 8:
        status = "🟠 PREMIUM"

    elif gap >= -3:
        status = "🟡 FAIR"

    elif gap >= -8:
        status = "🟢 ATTRACTIVE"

    else:
        status = "🟢 DISCOUNT"

    return {
        "reference":reference,
        "gap":gap,
        "score":score,
        "status":status,
        "support":support,
        "resistance":resistance,
        "high52":high52,
        "low52":low52
    }

# ============================================================
# CPR ENGINE
# ============================================================

def cpr_engine(df):

    last = df.iloc[-1]

    close = safe_num(
        last["Close"]
    )

    low = safe_num(
        last["CPR_LOW"],
        close
    )

    high = safe_num(
        last["CPR_HIGH"],
        close
    )

    pp = safe_num(
        last["PP"],
        close
    )

    width = safe_num(
        last["CPR_WIDTH"]
    )

    if close > high:
        status = "🟢 ABOVE"
        score = 100

    elif close < low:
        status = "🔴 BELOW"
        score = 30

    else:
        status = "🟡 INSIDE"
        score = 60

    if width <= .50:
        cpr_type = "🟢 NARROW"

    elif width <= 1:
        cpr_type = "🟡 NORMAL"

    else:
        cpr_type = "🟠 WIDE"

    return {
        "pp":pp,
        "bc":safe_num(last["BC"]),
        "tc":safe_num(last["TC"]),
        "low":low,
        "high":high,
        "width":width,
        "status":status,
        "type":cpr_type,
        "score":score
    }

# ============================================================
# EXITMANTRA 3-PILLAR ENGINE
# ============================================================

def exitmantra_engine(
    technical,
    momentum,
    above_exit,
    ath_profit,
    outperformance,
    risk,
    ems
):

    # --------------------------------------------------------
    # 3 PILLARS
    # --------------------------------------------------------

    pillar_count = (
        int(ath_profit) +
        int(outperformance) +
        int(above_exit)
    )

    # --------------------------------------------------------
    # EXITMANTRA STYLE ZONE
    # --------------------------------------------------------

    if (
        pillar_count == 3
        and ems >= 70
        and risk < 55
    ):
        zone = "🐂 BULL"

    elif (
        pillar_count >= 2
        and ems >= 55
    ):
        zone = "🐂 BULL"

    elif (
        pillar_count == 1
        and ems >= 45
    ):
        zone = "🐷 PIG"

    elif (
        pillar_count == 0
        and ems >= 45
    ):
        zone = "🐷 PIG"

    else:
        zone = "🐻 BEAR"

    # --------------------------------------------------------
    # ACTION
    # --------------------------------------------------------

    if zone == "🐂 BULL":

        if (
            pillar_count == 3
            and ems >= 70
        ):
            action = "🟢 ADD"

        else:
            action = "🟢 HOLD"

    elif zone == "🐷 PIG":

        if (
            ems >= 60
            and technical >= 55
        ):
            action = "🟡 HOLD"

        else:
            action = "🟠 REPLACE"

    else:

        if (
            ems < 40
            or pillar_count == 0
        ):
            action = "🔴 EXIT"

        else:
            action = "🟠 REPLACE"

    # --------------------------------------------------------
    # RATING
    # --------------------------------------------------------

    if action == "🟢 ADD":
        rating = "ADD"

    elif action == "🟢 HOLD":
        rating = "HOLD"

    elif action == "🟡 HOLD":
        rating = "HOLD"

    elif action == "🟠 REPLACE":
        rating = "REPLACE"

    else:
        rating = "EXIT"

    return {
        "zone":zone,
        "action":action,
        "rating":rating,
        "pillars":pillar_count
    }

# ============================================================
# RISK + TARGET ENGINE
# ============================================================

def risk_target_engine(
    df,
    price,
    breakout
):

    last = df.iloc[-1]

    cmp = safe_num(
        last["Close"]
    )

    atr = safe_num(
        last["ATR14"],
        cmp*.03
    )

    support = price["support"]
    resistance = price["resistance"]
    high52 = price["high52"]

    # --------------------------------------------------------
    # STOP
    # --------------------------------------------------------

    atr_stop = (
        cmp -
        1.8 * atr
    )

    support_stop = (
        support * .97
    )

    stop = min(
        atr_stop,
        support_stop
    )

    if (
        stop <= 0
        or stop >= cmp
    ):
        stop = cmp - 2*atr

    # --------------------------------------------------------
    # BUY ZONE
    # --------------------------------------------------------

    e20 = safe_num(
        last["EMA20"],
        cmp
    )

    e50 = safe_num(
        last["EMA50"],
        cmp
    )

    center = (
        e20*.45 +
        e50*.55
    )

    buy_low = max(
        0,
        min(
            support,
            center*.97
        )
    )

    buy_high = max(
        support,
        center*1.01
    )

    dip_low = max(
        0,
        min(
            e50*.97,
            support*.99
        )
    )

    dip_high = max(
        e50*1.01,
        support*1.02
    )

    # --------------------------------------------------------
    # BREAKOUT ENTRY
    # --------------------------------------------------------

    breakout_entry = breakout["level"]

    # --------------------------------------------------------
    # SWING TARGETS
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # LONG TARGETS
    # --------------------------------------------------------

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
        if risk_amount > 0
        else 0
    )

    downside = (
        risk_amount/cmp*100
        if cmp > 0
        else 0
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
# EMS V3.3 MASTER
# ============================================================

def ems_engine(df):

    last = df.iloc[-1]

    close = safe_num(
        last["Close"]
    )

    technical = technical_engine(
        df
    )

    momentum, momentum_grade = (
        momentum_engine(df)
    )

    cpr = cpr_engine(df)

    breakout = breakout_engine(
        df
    )

    value = price_value_engine(
        df
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
        support_score += 25

    if close < resistance:
        support_score += 15

    support_score = max(
        0,
        min(100,support_score)
    )

    # --------------------------------------------------------
    # VOLUME
    # --------------------------------------------------------

    volume_ratio = safe_num(
        last["VOLUME_RATIO"]
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
    # RELATIVE STRENGTH
    # --------------------------------------------------------

    relative = 50

    if close > safe_num(
        last["EMA50"],
        close
    ):
        relative += 20

    if close > safe_num(
        last["EMA200"],
        close
    ):
        relative += 20

    relative = min(
        100,
        relative
    )

    # --------------------------------------------------------
    # RISK
    # --------------------------------------------------------

    rsi = safe_num(
        last["RSI14"],
        50
    )

    risk = 20

    if close < safe_num(
        last["EMA20"],
        close
    ):
        risk += 20

    if rsi < 40:
        risk += 25

    if safe_num(
        last["MACD"]
    ) < safe_num(
        last["MACD_SIGNAL"]
    ):
        risk += 20

    if volume_ratio < .7:
        risk += 15

    if rsi >= 75:
        risk += 15

    risk = min(
        100,
        risk
    )

    # --------------------------------------------------------
    # D/W/M
    # --------------------------------------------------------

    daily,weekly,monthly,dwm,regime = (
        dwm_engine(df)
    )

    # --------------------------------------------------------
    # PILLARS
    #
    # ATH PROFIT:
    # Current price >= 52W high * 0.90
    #
    # OUTPERFORMANCE:
    # Momentum + relative strength
    #
    # ABOVE EXIT PRICE:
    # Current price above calculated technical exit line
    # --------------------------------------------------------

    high52 = value["high52"]

    ath_profit = (
        close >= high52*.90
    )

    outperformance = (
        momentum >= 60
        and relative >= 70
    )

    # Dynamic Exit Price
    exit_price = min(
        safe_num(last["EMA50"],close),
        support
    )

    above_exit = (
        close > exit_price
    )

    # --------------------------------------------------------
    # PRELIMINARY EMS
    # --------------------------------------------------------

    raw = (
        technical*.25 +
        momentum*.12 +
        support_score*.08 +
        volume_score*.08 +
        relative*.08 +
        cpr["score"]*.08 +
        breakout["score"]*.05 +
        (100-risk)*.09 +
        value["score"]*.10 +
        dwm*.07
    )

    ems = round(
        max(
            0,
            min(100,raw)
        ),
        1
    )

    # --------------------------------------------------------
    # EXITMANTRA
    # --------------------------------------------------------

    exitm = exitmantra_engine(
        technical=technical,
        momentum=momentum,
        above_exit=above_exit,
        ath_profit=ath_profit,
        outperformance=outperformance,
        risk=risk,
        ems=ems
    )

    # --------------------------------------------------------
    # SWING SCORE
    # --------------------------------------------------------

    swing_score = round(
        technical*.30 +
        momentum*.25 +
        breakout["score"]*.20 +
        cpr["score"]*.10 +
        volume_score*.05 +
        (100-risk)*.10,
        1
    )

    # --------------------------------------------------------
    # LONG SCORE
    # --------------------------------------------------------

    long_score = round(
        technical*.25 +
        dwm*.25 +
        relative*.15 +
        value["score"]*.15 +
        (100-risk)*.10 +
        momentum*.10,
        1
    )

    # --------------------------------------------------------
    # SWING ACTION
    # --------------------------------------------------------

    if swing_score >= 75:
        swing_action = "🚀 SWING BUY"

    elif swing_score >= 65:
        swing_action = "🟢 SWING HOLD"

    elif swing_score >= 55:
        swing_action = "🟡 SWING WAIT"

    elif swing_score >= 45:
        swing_action = "🟠 SWING REDUCE"

    else:
        swing_action = "🔴 SWING EXIT"

    # --------------------------------------------------------
    # LONG ACTION
    # --------------------------------------------------------

    if long_score >= 75:
        long_action = "🏆 LONG ADD"

    elif long_score >= 65:
        long_action = "🟢 LONG HOLD"

    elif long_score >= 55:
        long_action = "🟡 LONG WATCH"

    elif long_score >= 45:
        long_action = "🟠 LONG REDUCE"

    else:
        long_action = "🔴 LONG EXIT"

    return {
        "ems":ems,
        "technical":technical,
        "momentum":momentum,
        "momentum_grade":momentum_grade,
        "support_score":support_score,
        "volume_score":volume_score,
        "relative":relative,
        "risk":risk,
        "cpr":cpr,
        "breakout":breakout,
        "value":value,
        "daily":daily,
        "weekly":weekly,
        "monthly":monthly,
        "dwm":dwm,
        "regime":regime,
        "ath_profit":ath_profit,
        "outperformance":outperformance,
        "above_exit":above_exit,
        "exit_price":exit_price,
        "exitmantra":exitm,
        "swing_score":swing_score,
        "swing_action":swing_action,
        "long_score":long_score,
        "long_action":long_action
    }

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

        df = calculate_indicators(
            df
        )

        ems = ems_engine(
            df
        )

        risk = risk_target_engine(
            df,
            ems["value"],
            ems["breakout"]
        )

        return {
            "df":df,
            "ems":ems,
            "risk":risk
        }

    except Exception:
        return None

# ============================================================
# SESSION
# ============================================================

if "stocks" not in st.session_state:
    st.session_state.stocks = []

if "results" not in st.session_state:
    st.session_state.results = {}

if "previous_signals" not in st.session_state:
    st.session_state.previous_signals = {}

# ============================================================
# STOCK INPUT
# ============================================================

st.markdown(
    '<div class="section-title">➕ ADD STOCK</div>',
    unsafe_allow_html=True
)

stock_input = st.text_input(
    "NSE Symbol",
    placeholder="BSE / AIIL / RATNAVEER / SHRIRAMFIN",
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
        st.session_state.stocks.append(
            symbol
        )
        st.rerun()

st.markdown(
    f'<div class="section-title">'
    f'📋 MY STOCKS — '
    f'{len(st.session_state.stocks)}/15'
    f'</div>',
    unsafe_allow_html=True
)

if st.session_state.stocks:

    st.write(
        " • ".join(
            st.session_state.stocks
        )
    )

    if st.button(
        "🗑️ CLEAR WATCHLIST",
        use_container_width=True
    ):

        st.session_state.stocks = []
        st.session_state.results = {}

        st.rerun()

# ============================================================
# ANALYZE BUTTON
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

        result = analyze_stock(
            symbol
        )

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

    st.success(
        "✅ V3.3 Analysis completed."
    )

# ============================================================
# DASHBOARD
# ============================================================

if st.session_state.results:

    results = (
        st.session_state.results
    )

    analyzed = len(results)

    adds = sum(
        1
        for r in results.values()
        if r["ems"]["exitmantra"]["rating"] == "ADD"
    )

    holds = sum(
        1
        for r in results.values()
        if r["ems"]["exitmantra"]["rating"] == "HOLD"
    )

    replaces = sum(
        1
        for r in results.values()
        if r["ems"]["exitmantra"]["rating"] == "REPLACE"
    )

    exits = sum(
        1
        for r in results.values()
        if r["ems"]["exitmantra"]["rating"] == "EXIT"
    )

    avg_ems = np.mean([
        r["ems"]["ems"]
        for r in results.values()
    ])

    st.markdown("---")

    st.markdown(
        '<div class="section-title">'
        '🚦 EMS V3.3 MASTER DASHBOARD'
        '</div>',
        unsafe_allow_html=True
    )

    html = f"""
    <div class="grid6">

        {box(
            "ANALYZED",
            analyzed,
            "blue"
        )}

        {box(
            "ADD",
            f"🟢 {adds}",
            "green"
        )}

        {box(
            "HOLD",
            f"🟡 {holds}",
            "yellow"
        )}

        {box(
            "REPLACE",
            f"🟠 {replaces}",
            "orange"
        )}

        {box(
            "EXIT",
            f"🔴 {exits}",
            "red"
        )}

        {box(
            "AVG EMS",
            f"{avg_ems:.0f}/100",
            "blue"
        )}

    </div>
    """

    st.markdown(
        html,
        unsafe_allow_html=True
    )

# ============================================================
# STOCK RESULTS
# ============================================================

for symbol,result in (
    st.session_state.results.items()
):

    df = result["df"]
    ems = result["ems"]
    price = ems["value"]
    risk = result["risk"]

    last = df.iloc[-1]

    cmp = safe_num(
        last["Close"]
    )

    exitm = ems["exitmantra"]

    # --------------------------------------------------------
    # MAIN SIGNAL
    # --------------------------------------------------------

    if exitm["rating"] == "ADD":
        signal_css = "green"

    elif exitm["rating"] == "HOLD":
        signal_css = "yellow"

    elif exitm["rating"] == "REPLACE":
        signal_css = "orange"

    else:
        signal_css = "red"

    st.markdown("---")

    st.markdown(
        f"## 🏢 {symbol}"
    )

    st.caption(
        f"{symbol}.NS • NSE • "
        f"Last available close • "
        f"{datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )

    st.markdown(
        f'<div class="big-signal">'
        f'{exitm["zone"]} &nbsp; '
        f'{exitm["action"]}'
        f'</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # EXITMANTRA MASTER RESULT
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🎯 EXITMANTRA-STYLE MASTER RESULT'
        '</div>',
        unsafe_allow_html=True
    )

    master_html = f"""
    <div class="grid5">

        {box(
            "ZONE",
            exitm["zone"],
            signal_css
        )}

        {box(
            "RATING",
            exitm["rating"],
            signal_css
        )}

        {box(
            "EMS",
            f'{ems["ems"]:.0f}/100',
            "green"
            if ems["ems"]>=65
            else "yellow"
        )}

        {box(
            "PILLARS",
            f'{exitm["pillars"]}/3',
            "blue"
        )}

        {box(
            "EXIT PRICE",
            f'₹{ems["exit_price"]:,.2f}',
            "red"
        )}

    </div>
    """

    st.markdown(
        master_html,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # THREE PILLARS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🏛️ 3-PILLAR DECISION'
        '</div>',
        unsafe_allow_html=True
    )

    pillar_html = f"""
    <div class="grid3">

        {box(
            "ATH PROFIT",
            "YES" if ems["ath_profit"] else "NO",
            "green"
            if ems["ath_profit"]
            else "red"
        )}

        {box(
            "OUTPERFORMANCE",
            "YES" if ems["outperformance"] else "NO",
            "green"
            if ems["outperformance"]
            else "red"
        )}

        {box(
            "ABOVE EXIT PRICE",
            "YES" if ems["above_exit"] else "NO",
            "green"
            if ems["above_exit"]
            else "red"
        )}

    </div>
    """

    st.markdown(
        pillar_html,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # SWING + LONG
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '📈 STRATEGY SCORES'
        '</div>',
        unsafe_allow_html=True
    )

    strategy_html = f"""
    <div class="grid5">

        {box(
            "SWING SCORE",
            f'{ems["swing_score"]:.0f}/100',
            "green"
            if ems["swing_score"]>=65
            else "yellow"
        )}

        {box(
            "SWING ACTION",
            ems["swing_action"],
            "green"
            if ems["swing_score"]>=65
            else "yellow"
        )}

        {box(
            "LONG SCORE",
            f'{ems["long_score"]:.0f}/100',
            "blue"
        )}

        {box(
            "LONG ACTION",
            ems["long_action"],
            "blue"
        )}

        {box(
            "D/W/M",
            f'{ems["dwm"]:.0f}/100',
            "blue"
        )}

    </div>
    """

    st.markdown(
        strategy_html,
        unsafe_allow_html=True
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
    <div class="grid6">

        {box(
            "CMP",
            f"₹{cmp:,.2f}",
            "blue"
        )}

        {box(
            "EMS",
            f'{ems["ems"]:.0f}/100',
            "green"
            if ems["ems"]>=65
            else "yellow"
        )}

        {box(
            "TECH",
            f'{ems["technical"]:.0f}/100',
            "green"
            if ems["technical"]>=60
            else "red"
        )}

        {box(
            "RSI",
            f'{safe_num(last["RSI14"],50):.1f}',
            "green"
            if safe_num(last["RSI14"],50)<75
            else "red"
        )}

        {box(
            "VOLUME",
            f'{safe_num(last["VOLUME_RATIO"]):.2f}x',
            "green"
            if safe_num(last["VOLUME_RATIO"])>=1.5
            else "yellow"
        )}

        {box(
            "RISK",
            f'{ems["risk"]:.0f}/100',
            "red"
            if ems["risk"]>=55
            else "green"
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

    e10 = safe_num(
        last["EMA10"]
    )

    e20 = safe_num(
        last["EMA20"]
    )

    e50 = safe_num(
        last["EMA50"]
    )

    e100 = safe_num(
        last["EMA100"]
    )

    e200 = safe_num(
        last["EMA200"]
    )

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

    key_html = f"""
    <div class="grid5">

        {box(
            "EMA 10",
            f"₹{e10:,.2f}",
            "green" if cmp>e10 else "red"
        )}

        {box(
            "EMA 20",
            f"₹{e20:,.2f}",
            "green" if cmp>e20 else "red"
        )}

        {box(
            "EMA 50",
            f"₹{e50:,.2f}",
            "green" if cmp>e50 else "red"
        )}

        {box(
            "EMA 100",
            f"₹{e100:,.2f}",
            "green" if cmp>e100 else "red"
        )}

        {box(
            "EMA 200",
            f"₹{e200:,.2f}",
            "green" if cmp>e200 else "red"
        )}

        {box(
            "RSI 14",
            f'{safe_num(last["RSI14"],50):.1f}'
        )}

        {box(
            "MACD",
            "🟢 BULL" if macd_bull else "🔴 BEAR"
        )}

        {box(
            "SUPERTREND",
            "🟢 BULL" if st_bull else "🔴 BEAR"
        )}

        {box(
            "MOMENTUM",
            ems["momentum_grade"]
        )}

        {box(
            "D/W/M",
            ems["regime"]
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
    <div class="grid5">

        {box(
            "CMP",
            f"₹{cmp:,.2f}",
            "blue"
        )}

        {box(
            "REFERENCE",
            f'₹{price["reference"]:,.2f}',
            "yellow"
        )}

        {box(
            "VALUE SCORE",
            f'{price["score"]}/100',
            "green"
            if price["score"]>=70
            else "yellow"
        )}

        {box(
            "VALUE STATUS",
            price["status"]
        )}

        {box(
            "VALUE GAP",
            f'{price["gap"]:+.1f}%'
        )}

    </div>
    """

    st.markdown(
        pv,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # CPR — ONLY ONE SECTION
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '📐 CPR — CENTRAL PIVOT RANGE'
        '</div>',
        unsafe_allow_html=True
    )

    cpr = ems["cpr"]

    cpr_html = f"""
    <div class="grid6">

        {box(
            "PP",
            f'₹{cpr["pp"]:,.2f}',
            "blue"
        )}

        {box(
            "BC",
            f'₹{cpr["bc"]:,.2f}',
            "blue"
        )}

        {box(
            "TC",
            f'₹{cpr["tc"]:,.2f}',
            "blue"
        )}

        {box(
            "CPR LOW",
            f'₹{cpr["low"]:,.2f}',
            "blue"
        )}

        {box(
            "CPR HIGH",
            f'₹{cpr["high"]:,.2f}',
            "blue"
        )}

        {box(
            "CPR",
            f'{cpr["status"]} • {cpr["type"]}',
            "yellow"
        )}

    </div>
    """

    st.markdown(
        cpr_html,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # EMS BREAKDOWN
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🧠 EMS V3.3 BREAKDOWN'
        '</div>',
        unsafe_allow_html=True
    )

    ems_html = f"""
    <div class="grid5">

        {box(
            "TECHNICAL",
            f'{ems["technical"]:.0f}/100'
        )}

        {box(
            "MOMENTUM",
            f'{ems["momentum"]:.0f}/100'
        )}

        {box(
            "SUPPORT",
            f'{ems["support_score"]:.0f}/100'
        )}

        {box(
            "VOLUME",
            f'{ems["volume_score"]:.0f}/100'
        )}

        {box(
            "RELATIVE",
            f'{ems["relative"]:.0f}/100'
        )}

        {box(
            "CPR",
            f'{cpr["score"]:.0f}/100'
        )}

        {box(
            "BREAKOUT",
            f'{ems["breakout"]["score"]:.0f}/100'
        )}

        {box(
            "RISK",
            f'{ems["risk"]:.0f}/100'
        )}

        {box(
            "VALUE",
            f'{price["score"]:.0f}/100'
        )}

        {box(
            "FINAL EMS",
            f'{ems["ems"]:.0f}/100',
            "green"
            if ems["ems"]>=65
            else "yellow"
        )}

    </div>
    """

    st.markdown(
        ems_html,
        unsafe_allow_html=True
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
    <div class="grid6">

        {box(
            "SUPPORT",
            f'₹{price["support"]:,.2f}',
            "blue"
        )}

        {box(
            "RESISTANCE",
            f'₹{price["resistance"]:,.2f}',
            "blue"
        )}

        {box(
            "52W HIGH",
            f'₹{price["high52"]:,.2f}',
            "yellow"
        )}

        {box(
            "52W LOW",
            f'₹{price["low52"]:,.2f}',
            "blue"
        )}

        {box(
            "ATR 14",
            f'₹{risk["atr"]:,.2f}',
            "yellow"
        )}

        {box(
            "STOP LOSS",
            f'₹{risk["stop"]:,.2f}',
            "red"
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

    entry = f"""
    <div class="grid6">

        {box(
            "BUY ZONE",
            f'₹{risk["buy_low"]:,.0f} – ₹{risk["buy_high"]:,.0f}',
            "green"
        )}

        {box(
            "BUY ON DIP",
            f'₹{risk["dip_low"]:,.0f} – ₹{risk["dip_high"]:,.0f}',
            "green"
        )}

        {box(
            "BREAKOUT ENTRY",
            f'₹{risk["breakout"]:,.2f}',
            "blue"
        )}

        {box(
            "ATR STOP",
            f'₹{risk["stop"]:,.2f}',
            "red"
        )}

        {box(
            "RISK",
            f'{risk["downside"]:.1f}%',
            "red"
        )}

        {box(
            "R:R",
            f'1 : {risk["rr"]:.2f}',
            "blue"
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

    swing_html = f"""
    <div class="grid3">

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
        swing_html,
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
    <div class="grid3">

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
    # BREAKOUT
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🚀 BREAKOUT QUALITY + RETEST'
        '</div>',
        unsafe_allow_html=True
    )

    br = ems["breakout"]

    br_html = f"""
    <div class="grid6">

        {box(
            "BREAKOUT",
            f'₹{br["level"]:,.2f}',
            "blue"
        )}

        {box(
            "QUALITY",
            br["quality"]
        )}

        {box(
            "CONFIRMATIONS",
            f'{br["confirmations"]}/7'
        )}

        {box(
            "VOLUME",
            "✅ CONFIRMED"
            if br["volume_confirmed"]
            else "⏳ PENDING"
        )}

        {box(
            "RETEST",
            "✅ YES"
            if br["retest"]
            else "⏳ WAIT"
        )}

        {box(
            "STATUS",
            br["status"]
        )}

    </div>
    """

    st.markdown(
        br_html,
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="small">'
        f'Retest Zone: ₹{br["retest_low"]:,.2f}'
        f' – ₹{br["retest_high"]:,.2f}'
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
    <div class="grid5">

        {box(
            "DAILY",
            f'{ems["daily"]:.0f}/100'
        )}

        {box(
            "WEEKLY",
            f'{ems["weekly"]:.0f}/100'
        )}

        {box(
            "MONTHLY",
            f'{ems["monthly"]:.0f}/100'
        )}

        {box(
            "MASTER",
            f'{ems["dwm"]:.0f}/100',
            "blue"
        )}

        {box(
            "REGIME",
            ems["regime"]
        )}

    </div>
    """

    st.markdown(
        dwm_html,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # SIGNAL TRACKER
    # --------------------------------------------------------

    current_signal = (
        exitm["rating"]
    )

    previous_signal = (
        st.session_state
        .previous_signals
        .get(symbol)
    )

    if previous_signal is None:

        tracker = "🆕 FIRST ANALYSIS"

    elif previous_signal != current_signal:

        tracker = (
            f"⚡ {previous_signal} → "
            f"{current_signal}"
        )

    else:

        tracker = "➡️ SIGNAL UNCHANGED"

    st.session_state.previous_signals[
        symbol
    ] = current_signal

    st.info(
        f"🔄 Signal Tracker: {tracker}"
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
    ).dropna(how="all")

    st.line_chart(
        chart_df,
        use_container_width=True
    )

    # --------------------------------------------------------
    # WHY SIGNAL
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🧠 WHY THIS SIGNAL?'
        '</div>',
        unsafe_allow_html=True
    )

    if cmp > e10 > e20 > e50 > e100 > e200:

        st.success(
            "✅ Full EMA bullish alignment."
        )

    elif cmp < e10 < e20 < e50 < e100 < e200:

        st.error(
            "🔴 Full EMA bearish alignment."
        )

    else:

        st.warning(
            "🟡 EMA structure mixed."
        )

    if safe_num(last["RSI14"],50) >= 75:

        st.error(
            "🔴 RSI extreme overbought."
        )

    elif safe_num(last["RSI14"],50) >= 60:

        st.write(
            "🟢 RSI strong."
        )

    elif safe_num(last["RSI14"],50) >= 50:

        st.write(
            "🟢 RSI positive."
        )

    else:

        st.write(
            "🔴 RSI weak."
        )

    st.write(
        "🟢 MACD bullish"
        if macd_bull
        else
        "🔴 MACD bearish"
    )

    st.write(
        "🟢 Supertrend bullish"
        if st_bull
        else
        "🔴 Supertrend bearish"
    )

    if safe_num(
        last["VOLUME_RATIO"]
    ) >= 2:

        st.write(
            "🚀 Volume breakout confirmation."
        )

    elif safe_num(
        last["VOLUME_RATIO"]
    ) >= 1:

        st.write(
            "🟡 Volume improving."
        )

    else:

        st.write(
            "🔴 Volume weak."
        )

    st.write(
        f'📐 CPR: {cpr["status"]} • '
        f'{cpr["type"]}'
    )

    st.write(
        f'🏛️ 3-Pillar: '
        f'{exitm["pillars"]}/3'
    )

    st.write(
        f'🎯 Exit Price: '
        f'₹{ems["exit_price"]:,.2f}'
    )

    st.write(
        f'📈 Swing Score: '
        f'{ems["swing_score"]:.0f}/100'
    )

    st.write(
        f'🏆 Long Score: '
        f'{ems["long_score"]:.0f}/100'
    )

    # --------------------------------------------------------
    # FINAL DECISION
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🏁 FINAL DECISION'
        '</div>',
        unsafe_allow_html=True
    )

    st.success(
        f'{exitm["zone"]} • '
        f'{exitm["action"]} • '
        f'EMS {ems["ems"]:.0f}/100 • '
        f'Swing {ems["swing_score"]:.0f} • '
        f'Long {ems["long_score"]:.0f}'
    )

# ============================================================
# FOOTER
# ============================================================

st.caption(
    "🐂 RAJESH STOCK ANALYZER PRO V3.3 MASTER • "
    "NSE ONLY • EMS V3.3 • ExitMantra-style 3-Pillar Logic • "
    "Bull/Pig/Bear • ADD/HOLD/REPLACE/EXIT • "
    "Swing + Long • CPR Single Source • "
    "Research & decision-support tool • Not financial advice."
)
