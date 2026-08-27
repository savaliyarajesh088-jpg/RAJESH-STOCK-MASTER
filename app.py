# ============================================================
# 🐂 RAJESH STOCK ANALYZER PRO V3.0 MASTER
# NSE • Manual 1–15 Stocks
# EMS V3.1 • PRICE VALUE • D/W/M
# EMA 10/20/50/100/200 • CPR CENTRAL PIVOT RANGE
# RSI • MACD • SUPERTREND • MOMENTUM
# BREAKOUT + RETEST • SWING + LONG • RISK
# MOBILE FIRST • BRIGHT VALUES • STABLE CARDS
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
    page_title="RAJESH STOCK ANALYZER PRO V3.0",
    page_icon="🐂",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CSS — STABLE / BRIGHT / MOBILE FIRST
# ============================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: Arial, sans-serif !important;
}

.stApp {
    background:#050505 !important;
}

.main {
    background:#050505 !important;
}

.block-container {
    padding-top:.55rem !important;
    padding-left:.55rem !important;
    padding-right:.55rem !important;
    padding-bottom:2rem !important;
    max-width:1500px !important;
}

/* ---------------- TITLE ---------------- */

.app-title {
    font-size:23px;
    font-weight:900;
    color:#ffffff !important;
    margin-bottom:2px;
}

.app-subtitle {
    font-size:11px;
    color:#cfcfcf !important;
    opacity:1 !important;
    margin-bottom:10px;
}

/* ---------------- GRID ---------------- */

.box-grid {
    display:grid;
    grid-template-columns:repeat(6,minmax(0,1fr));
    gap:5px;
    margin-bottom:8px;
    width:100%;
}

.key-grid {
    display:grid;
    grid-template-columns:repeat(6,minmax(0,1fr));
    gap:4px;
    width:100%;
}

.target-grid {
    display:grid;
    grid-template-columns:repeat(3,minmax(0,1fr));
    gap:4px;
    width:100%;
}

.ems-grid {
    display:grid;
    grid-template-columns:repeat(5,minmax(0,1fr));
    gap:4px;
    width:100%;
}

/* ---------------- BOX BASE ---------------- */

.metric-box,
.key-box,
.price-box,
.target-box,
.ems-box {
    box-sizing:border-box;
    border:1px solid #383838;
    border-radius:8px;
    background:#111111;
    padding:7px 4px;
    text-align:center;
    overflow:hidden;
    min-width:0;
}

/* ---------------- LABEL ---------------- */

.metric-title,
.key-title,
.price-title,
.target-title,
.ems-title {
    display:block;
    font-size:9px;
    font-weight:700;
    color:#d0d0d0 !important;
    opacity:1 !important;
    white-space:nowrap;
    overflow:hidden;
    text-overflow:ellipsis;
}

/* ---------------- VALUES — ALWAYS BRIGHT ---------------- */

.metric-value,
.key-value,
.price-value,
.target-value,
.ems-value {
    display:block;
    font-size:13px;
    font-weight:900;
    color:#ffffff !important;
    opacity:1 !important;
    margin-top:3px;
    white-space:nowrap;
    overflow:hidden;
    text-overflow:ellipsis;
}

.key-value {
    font-size:11px;
}

.target-value {
    font-size:13px;
}

.ems-value {
    font-size:12px;
}

.target-upside {
    font-size:10px;
    color:#dddddd !important;
    opacity:1 !important;
    margin-top:2px;
}

/* ---------------- STATUS COLORS ---------------- */

.green-box {
    border-color:#176b36 !important;
}

.red-box {
    border-color:#7b2020 !important;
}

.blue-box {
    border-color:#244e86 !important;
}

.yellow-box {
    border-color:#80651a !important;
}

.orange-box {
    border-color:#9a5a12 !important;
}

.key-positive {
    border-color:#176b36 !important;
}

.key-negative {
    border-color:#7b2020 !important;
}

.key-warning {
    border-color:#80651a !important;
}

/* ---------------- SIGNAL ---------------- */

.signal {
    font-size:19px;
    font-weight:900;
    color:#ffffff !important;
    opacity:1 !important;
    padding:4px 0;
}

/* ---------------- SECTION ---------------- */

.section-title {
    font-size:16px;
    font-weight:900;
    color:#ffffff !important;
    margin-top:10px;
    margin-bottom:5px;
}

/* ---------------- INFO / WARNING ---------------- */

.stAlert {
    color:#ffffff !important;
}

/* ---------------- MOBILE ---------------- */

@media(max-width:900px) {

    .box-grid {
        grid-template-columns:repeat(3,minmax(0,1fr));
    }

    .key-grid {
        grid-template-columns:repeat(3,minmax(0,1fr));
    }

    .target-grid {
        grid-template-columns:repeat(3,minmax(0,1fr));
    }

    .ems-grid {
        grid-template-columns:repeat(3,minmax(0,1fr));
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
        font-size:10px;
    }

    .box-grid {
        grid-template-columns:repeat(2,minmax(0,1fr));
        gap:4px;
    }

    .key-grid {
        grid-template-columns:repeat(3,minmax(0,1fr));
        gap:3px;
    }

    .target-grid {
        grid-template-columns:repeat(3,minmax(0,1fr));
        gap:3px;
    }

    .ems-grid {
        grid-template-columns:repeat(3,minmax(0,1fr));
        gap:3px;
    }

    .metric-box,
    .key-box,
    .price-box,
    .target-box,
    .ems-box {
        padding:6px 3px;
        border-radius:7px;
    }

    .metric-title,
    .key-title,
    .price-title,
    .target-title,
    .ems-title {
        font-size:8px;
    }

    .metric-value {
        font-size:12px;
    }

    .key-value,
    .ems-value {
        font-size:10px;
    }

    .target-value {
        font-size:11px;
    }

    .target-upside {
        font-size:9px;
    }

    .signal {
        font-size:17px;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="app-title">🐂 RAJESH STOCK ANALYZER PRO V3.0 MASTER</div>',
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


def clean_symbol(symbol):

    symbol = str(symbol).upper().strip()

    if symbol.endswith(".NS"):
        symbol = symbol[:-3]

    return symbol


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

    # Flatten possible yfinance columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    close = pd.to_numeric(df["Close"], errors="coerce")
    high = pd.to_numeric(df["High"], errors="coerce")
    low = pd.to_numeric(df["Low"], errors="coerce")
    volume = pd.to_numeric(df["Volume"], errors="coerce")

    df["Close"] = close
    df["High"] = high
    df["Low"] = low
    df["Volume"] = volume

    # --------------------------------------------------------
    # EMA
    # --------------------------------------------------------

    for p in [10,20,50,100,200]:

        df[f"EMA{p}"] = close.ewm(
            span=p,
            adjust=False,
            min_periods=p
        ).mean()

    # --------------------------------------------------------
    # RSI 14
    # --------------------------------------------------------

    delta = close.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(
        alpha=1/14,
        adjust=False,
        min_periods=14
    ).mean()

    avg_loss = loss.ewm(
        alpha=1/14,
        adjust=False,
        min_periods=14
    ).mean()

    rs = avg_gain / avg_loss.replace(0,np.nan)

    df["RSI14"] = 100 - (
        100 / (1 + rs)
    )

    # --------------------------------------------------------
    # MACD 12 / 26 / 9
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
        volume.rolling(
            20,
            min_periods=20
        ).mean()
    )

    df["VOLUME_RATIO"] = (
        volume /
        df["VOLUME_AVG20"].replace(0,np.nan)
    )

    # --------------------------------------------------------
    # 52 WEEK
    # --------------------------------------------------------

    df["52W_HIGH"] = (
        close.rolling(
            252,
            min_periods=60
        ).max()
    )

    df["52W_LOW"] = (
        close.rolling(
            252,
            min_periods=60
        ).min()
    )

    # --------------------------------------------------------
    # CPR — CENTRAL PIVOT RANGE
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

    df["SUPPORT20"] = (
        low.rolling(
            20,
            min_periods=10
        ).min()
    )

    df["RESISTANCE20"] = (
        high.rolling(
            20,
            min_periods=10
        ).max()
    )

    # --------------------------------------------------------
    # SUPERTREND 10 / 3
    # --------------------------------------------------------

    period = 10
    multiplier = 3.0

    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()

    tr = pd.concat(
        [tr1,tr2,tr3],
        axis=1
    ).max(axis=1)

    atr = tr.rolling(
        period,
        min_periods=period
    ).mean()

    hl2 = (
        high +
        low
    ) / 2

    basic_upper = (
        hl2 +
        multiplier * atr
    )

    basic_lower = (
        hl2 -
        multiplier * atr
    )

    final_upper = basic_upper.copy()
    final_lower = basic_lower.copy()

    trend = pd.Series(
        1,
        index=df.index,
        dtype=int
    )

    for i in range(1,len(df)):

        if (
            pd.isna(basic_upper.iloc[i]) or
            pd.isna(basic_lower.iloc[i])
        ):
            trend.iloc[i] = trend.iloc[i-1]
            continue

        prev_fu = final_upper.iloc[i-1]
        prev_fl = final_lower.iloc[i-1]

        if (
            pd.isna(prev_fu) or
            basic_upper.iloc[i] < prev_fu or
            close.iloc[i-1] > prev_fu
        ):
            final_upper.iloc[i] = basic_upper.iloc[i]
        else:
            final_upper.iloc[i] = prev_fu

        if (
            pd.isna(prev_fl) or
            basic_lower.iloc[i] > prev_fl or
            close.iloc[i-1] < prev_fl
        ):
            final_lower.iloc[i] = basic_lower.iloc[i]
        else:
            final_lower.iloc[i] = prev_fl

        if trend.iloc[i-1] == -1:

            if close.iloc[i] > final_upper.iloc[i]:
                trend.iloc[i] = 1
            else:
                trend.iloc[i] = -1

        else:

            if close.iloc[i] < final_lower.iloc[i]:
                trend.iloc[i] = -1
            else:
                trend.iloc[i] = 1

    st_line = pd.Series(
        np.nan,
        index=df.index
    )

    for i in range(len(df)):

        if trend.iloc[i] == 1:
            st_line.iloc[i] = final_lower.iloc[i]
        else:
            st_line.iloc[i] = final_upper.iloc[i]

    df["SUPERTREND_LINE"] = st_line
    df["SUPERTREND_TREND"] = trend

    # --------------------------------------------------------
    # MOMENTUM
    # --------------------------------------------------------

    df["ROC20"] = (
        close.pct_change(20) * 100
    )

    return df


# ============================================================
# D / W / M
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

        if rsi >= 55:
            score += 10

        elif rsi < 40:
            score -= 10

        return max(
            0,
            min(100,score)
        )

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

    if len(weekly) > 0:
        weekly = calculate_indicators(weekly)

    if len(monthly) > 0:
        monthly = calculate_indicators(monthly)

    weekly_score = one_score(weekly)
    monthly_score = one_score(monthly)

    master = round(
        daily * .40 +
        weekly_score * .30 +
        monthly_score * .30,
        1
    )

    return (
        daily,
        weekly_score,
        monthly_score,
        master
    )


# ============================================================
# BREAKOUT + RETEST
# ============================================================

def breakout_engine(df):

    last = df.iloc[-1]

    close = safe_num(
        last["Close"]
    )

    resistance = safe_num(
        last["RESISTANCE20"],
        close
    )

    volume = safe_num(
        last["VOLUME_RATIO"],
        0
    )

    breakout_level = (
        resistance * 1.003
    )

    breakout = (
        close >= breakout_level
    )

    previous_resistance = safe_num(
        df["RESISTANCE20"].iloc[-2]
        if len(df) > 1
        else resistance,
        resistance
    )

    retest_zone_low = (
        previous_resistance * .985
    )

    retest_zone_high = (
        previous_resistance * 1.015
    )

    retest = (
        breakout and
        retest_zone_low <= close <= retest_zone_high
    )

    volume_confirmed = (
        volume >= 2.0
    )

    confirmations = 0

    if breakout:
        confirmations += 1

    if volume_confirmed:
        confirmations += 1

    if retest:
        confirmations += 1

    if close > safe_num(
        last["EMA20"]
    ):
        confirmations += 1

    if safe_num(
        last["RSI14"],
        50
    ) >= 55:
        confirmations += 1

    if safe_num(
        last["MACD"]
    ) > safe_num(
        last["MACD_SIGNAL"]
    ):
        confirmations += 1

    if safe_num(
        last["SUPERTREND_TREND"]
    ) == 1:
        confirmations += 1

    if (
        breakout and
        volume_confirmed and
        retest
    ):
        status = (
            "🚀 BREAKOUT + RETEST CONFIRMED"
        )

    elif (
        breakout and
        volume_confirmed
    ):
        status = (
            "🚀 BREAKOUT CONFIRMED"
        )

    elif breakout:
        status = (
            "🟡 BREAKOUT / VOLUME PENDING"
        )

    else:
        status = "🟡 WATCH"

    return {
        "level":breakout_level,
        "breakout":breakout,
        "retest":retest,
        "volume_confirmed":volume_confirmed,
        "confirmations":confirmations,
        "status":status,
        "retest_low":retest_zone_low,
        "retest_high":retest_zone_high
    }


# ============================================================
# TECHNICAL ENGINE
# ============================================================

def technical_engine(df):

    last = df.iloc[-1]

    close = safe_num(
        last["Close"]
    )

    e10 = safe_num(last["EMA10"])
    e20 = safe_num(last["EMA20"])
    e50 = safe_num(last["EMA50"])
    e100 = safe_num(last["EMA100"])
    e200 = safe_num(last["EMA200"])

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

    volume = safe_num(
        last["VOLUME_RATIO"],
        0
    )

    st = safe_num(
        last["SUPERTREND_TREND"],
        0
    )

    score = 0

    # --------------------------------------------------------
    # EMA
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # RSI
    # --------------------------------------------------------

    if rsi >= 60:
        score += 15

    elif rsi >= 50:
        score += 10

    elif rsi >= 40:
        score += 5

    # --------------------------------------------------------
    # MACD
    # --------------------------------------------------------

    if macd > macd_signal:
        score += 15

    # --------------------------------------------------------
    # SUPERTREND
    # --------------------------------------------------------

    if st == 1:
        score += 15

    # --------------------------------------------------------
    # VOLUME
    # --------------------------------------------------------

    if volume >= 2:
        score += 15

    elif volume >= 1:
        score += 8

    return max(
        0,
        min(100,round(score,1))
    )


# ============================================================
# EMS V3.1
# ============================================================

def ems_engine(df):

    last = df.iloc[-1]

    close = safe_num(
        last["Close"]
    )

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

    if rsi >= 70:
        momentum += 5

    elif rsi >= 60:
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

    if close > safe_num(
        last["EMA50"]
    ):
        relative += 20

    if close > safe_num(
        last["EMA200"]
    ):
        relative += 20

    relative = max(
        0,
        min(100,relative)
    )

    # --------------------------------------------------------
    # RISK DETERIORATION
    # --------------------------------------------------------

    risk = 20

    if close < safe_num(
        last["EMA20"]
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

    # Extreme overbought
    if rsi >= 80:
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
        breakout["confirmations"] /
        7 * 100,
        1
    )

    # --------------------------------------------------------
    # PRICE VALUE — NORMALIZED
    # --------------------------------------------------------

    e20 = safe_num(
        last["EMA20"],
        close
    )

    e50 = safe_num(
        last["EMA50"],
        close
    )

    e100 = safe_num(
        last["EMA100"],
        close
    )

    e200 = safe_num(
        last["EMA200"],
        close
    )

    reference = (
        e20*.15 +
        e50*.20 +
        e100*.20 +
        e200*.20 +
        resistance*.15 +
        safe_num(
            last["52W_HIGH"],
            resistance
        )*.10
    )

    price_ratio = (
        reference / close
        if close > 0
        else 1
    )

    # Price value score
    if price_ratio >= 1.10:
        price_value_score = 100

    elif price_ratio >= 1.03:
        price_value_score = 85

    elif price_ratio >= .97:
        price_value_score = 70

    elif price_ratio >= .90:
        price_value_score = 45

    else:
        price_value_score = 0

    # --------------------------------------------------------
    # FINAL EMS
    # --------------------------------------------------------

    raw = (
        technical * .25 +
        momentum * .12 +
        support_score * .08 +
        volume_score * .08 +
        relative * .08 +
        cpr_score * .08 +
        breakout_score * .05 +
        (100-risk) * .08 +
        price_value_score * .18
    )

    ems = round(
        max(0,min(100,raw)),
        1
    )

    # --------------------------------------------------------
    # DECISION
    # --------------------------------------------------------

    if rsi >= 80:

        decision = "🟠 WAIT / OVERBOUGHT"

    elif (
        ems >= 75 and
        technical >= 70 and
        price_value_score >= 70
    ):

        decision = "🟢 ADD"

    elif ems >= 60:

        decision = "🟢 HOLD"

    elif ems >= 45:

        decision = "🟠 REDUCE"

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
        "cpr_type":cpr_type,
        "cpr_width":cpr_width,
        "pp":pp,
        "breakout_score":breakout_score,
        "breakout":breakout,
        "price_value_score":price_value_score,
        "reference":reference,
        "decision":decision
    }


# ============================================================
# PRICE VALUE ENGINE
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

    breakout = (
        resistance*1.003
    )

    swing1 = resistance*1.03

    swing2 = max(
        resistance*1.08,
        high52*.95
    )

    swing3 = max(
        high52*1.05,
        swing2*1.03
    )

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

    upside = (
        (reference/cmp)-1
    )*100 if cmp else 0

    downside = (
        (cmp-stop_loss)/cmp
    )*100 if cmp else 0

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
# DATA DOWNLOAD
# ============================================================

def download_stock(ticker):

    try:

        df = yf.download(
            ticker,
            period="5y",
            interval="1d",
            auto_adjust=False,
            progress=False,
            threads=False
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

        for col in required:

            if col not in df.columns:
                return None

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

        df = df.dropna(
            subset=required
        )

        if len(df) < 210:
            return None

        return df

    except Exception:
        return None


# ============================================================
# ANALYZE STOCK
# ============================================================

def analyze_stock(symbol):

    symbol = clean_symbol(symbol)

    ticker = (
        symbol + ".NS"
    )

    df = download_stock(ticker)

    if df is None:
        return None

    try:

        df = calculate_indicators(df)

        # Remove rows where core indicators unavailable
        valid = df.dropna(
            subset=[
                "EMA20",
                "EMA50",
                "EMA200",
                "RSI14"
            ]
        )

        if valid.empty:
            return None

        # Keep complete dataset for chart
        df = df.loc[
            df.index >= valid.index[0]
        ].copy()

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

st.markdown("### ➕ ADD STOCK")

stock_input = st.text_input(
    "NSE Symbol",
    placeholder="BSE / RATNAVEER / AIIL",
    key="stock_input"
)

col_add, col_clear = st.columns(2)

with col_add:

    if st.button(
        "➕ ADD",
        use_container_width=True
    ):

        symbol = clean_symbol(
            stock_input
        )

        if not symbol:

            st.warning(
                "⚠️ NSE Symbol નાખો."
            )

        elif symbol in st.session_state.stocks:

            st.warning(
                "⚠️ Stock already added."
            )

        elif len(
            st.session_state.stocks
        ) >= 15:

            st.warning(
                "⚠️ Maximum 15 stocks."
            )

        else:

            st.session_state.stocks.append(
                symbol
            )

            st.rerun()


with col_clear:

    if st.button(
        "🗑️ CLEAR ALL",
        use_container_width=True
    ):

        st.session_state.stocks = []
        st.session_state.results = {}

        st.rerun()


# ============================================================
# WATCHLIST
# ============================================================

st.markdown(
    f"### 📋 MY STOCKS — "
    f"{len(st.session_state.stocks)}/15"
)

if st.session_state.stocks:

    st.markdown(
        " • ".join(
            st.session_state.stocks
        )
    )


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

    if total == 0:

        st.warning(
            "⚠️ પહેલા stock add કરો."
        )

    else:

        progress = st.progress(0)

        status_box = st.empty()

        for i,symbol in enumerate(
            st.session_state.stocks
        ):

            status_box.write(
                f"🔄 Analyzing {symbol}..."
            )

            result = analyze_stock(
                symbol
            )

            if result is not None:

                st.session_state.results[
                    symbol
                ] = result

            else:

                st.error(
                    f"⚠️ {symbol}: "
                    f"Market data unavailable"
                )

            progress.progress(
                int(
                    (i+1) /
                    total *
                    100
                )
            )

        status_box.success(
            "✅ Analysis completed."
        )


# ============================================================
# DASHBOARD
# ============================================================

if st.session_state.results:

    results = (
        st.session_state.results
    )

    analyzed = len(results)

    positive = sum(
        1
        for r in results.values()
        if r["ems"]["ems"] >= 60
    )

    risk_exit = sum(
        1
        for r in results.values()
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
        1
        for r in results.values()
        if r["ems"]["technical"] >= 70
    )

    bear = analyzed - bull

    st.markdown("---")

    st.markdown(
        "### 🚦 SMART SIGNAL DASHBOARD"
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

for symbol,result in (
    st.session_state.results.items()
):

    df = result["df"]

    ems = result["ems"]

    price = result["price"]

    last = df.iloc[-1]

    # IMPORTANT:
    # CMP/CLOSE always from SAME latest row
    cmp = safe_num(
        last["Close"]
    )

    # --------------------------------------------------------
    # SIGNAL
    # --------------------------------------------------------

    if ems["ems"] >= 75 and safe_num(
        last["RSI14"],50
    ) < 80:

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

    if safe_num(
        last["RSI14"],50
    ) >= 80:

        regime = "🟡 NEUTRAL"
        signal = "🟠 OVERBOUGHT / WAIT"

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.markdown("---")

    st.markdown(
        f"## 🏢 {symbol}"
    )

    st.caption(
        f"{symbol}.NS • NSE • "
        f"Last available close • "
        f"Analysis: "
        f"{datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )

    st.markdown(
        f'<div class="signal">'
        f'{regime} &nbsp; {signal}'
        f'</div>',
        unsafe_allow_html=True
    )

    # ========================================================
    # SUMMARY
    # ========================================================

    st.markdown(
        "### 🚦 SMART SIGNAL DASHBOARD"
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
            if safe_num(last["RSI14"],50)>=50
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
            if ems["ems"]>=60 and safe_num(last["RSI14"],50)<80
            else "orange-box"
        )}

    </div>
    """

    st.markdown(
        summary,
        unsafe_allow_html=True
    )

    # ========================================================
    # KEY INDICATORS
    # ========================================================

    st.markdown(
        "### 📊 KEY INDICATORS"
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
            "CPR",
            f'₹{safe_num(last["CPR_LOW"]):,.2f} – '
            f'₹{safe_num(last["CPR_HIGH"]):,.2f}',
            "key-warning"
        )}

        {html_box(
            "PP / PIVOT",
            f'₹{safe_num(last["PP"]):,.2f}'
        )}

        {html_box(
            "BC",
            f'₹{safe_num(last["BC"]):,.2f}'
        )}

        {html_box(
            "TC",
            f'₹{safe_num(last["TC"]):,.2f}'
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
            else "key-warning"
        )}

        {html_box(
            "CPR WIDTH",
            f'{ems["cpr_width"]:.2f}%'
        )}

        {html_box(
            "CPR TYPE",
            ems["cpr_type"]
        )}

    </div>
    """

    st.markdown(
        key_html,
        unsafe_allow_html=True
    )

    # ========================================================
    # PRICE VALUE
    # ========================================================

    st.markdown(
        "### 💰 PRICE VALUE"
    )

    pv_html = f"""
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
            "UPSIDE",
            f"{price['upside']:+.1f}%",
            "green-box"
            if price["upside"]>0
            else "red-box"
        )}

        {price_box(
            "DOWNSIDE RISK",
            f"{price['downside']:.1f}%",
            "red-box"
        )}

        {price_box(
            "RISK : REWARD",
            f"1 : {price['rr']:.2f}",
            "blue-box"
        )}

        {price_box(
            "EXIT PRICE",
            f"₹{price['exit']:,.2f}",
            "red-box"
        )}

    </div>
    """

    st.markdown(
        pv_html,
        unsafe_allow_html=True
    )

    if ems["price_value_score"] == 0:

        st.warning(
            "⚠️ PRICE VALUE WARNING: "
            "CMP reference value કરતાં નોંધપાત્ર ઉપર છે."
        )

    elif ems["price_value_score"] >= 70:

        st.success(
            "🟢 PRICE VALUE: "
            "CMP reference valueની નજીક/નીચે છે."
        )

    # ========================================================
    # CPR
    # ========================================================

    st.markdown(
        "### 📐 CPR — CENTRAL PIVOT RANGE"
    )

    cpr_html = f"""
    <div class="key-grid">

        {html_box(
            "PP / PIVOT",
            f'₹{safe_num(last["PP"]):,.2f}'
        )}

        {html_box(
            "BC",
            f'₹{safe_num(last["BC"]):,.2f}'
        )}

        {html_box(
            "TC",
            f'₹{safe_num(last["TC"]):,.2f}'
        )}

        {html_box(
            "CPR LOW",
            f'₹{safe_num(last["CPR_LOW"]):,.2f}'
        )}

        {html_box(
            "CPR HIGH",
            f'₹{safe_num(last["CPR_HIGH"]):,.2f}'
        )}

        {html_box(
            "CPR WIDTH",
            f'{ems["cpr_width"]:.2f}%'
        )}

        {html_box(
            "CPR TYPE",
            ems["cpr_type"]
        )}

        {html_box(
            "PRICE",
            ems["cpr_status"]
        )}

    </div>
    """

    st.markdown(
        cpr_html,
        unsafe_allow_html=True
    )

    # ========================================================
    # EMS BREAKDOWN
    # ========================================================

    st.markdown(
        "### 🧠 EMS V3.1 BREAKDOWN"
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
            f'{ems["price_value_score"]:.0f}/100'
        )}

        {ems_box(
            "D/W/M",
            f'{result["dwm"]:.0f}/100'
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
        f'🧠 EMS Decision: '
        f'{ems["decision"]} • '
        f'Daily {result["daily"]:.0f} | '
        f'Weekly {result["weekly"]:.0f} | '
        f'Monthly {result["monthly"]:.0f} | '
        f'Master {result["dwm"]:.0f}'
    )

    # ========================================================
    # OVERBOUGHT WARNING
    # ========================================================

    if safe_num(
        last["RSI14"],
        50
    ) >= 80:

        st.error(
            "🔴 RSI EXTREME OVERBOUGHT — "
            "fresh ADD ટાળો; confirmation / dipની રાહ જુઓ."
        )

    # ========================================================
    # PRICE LEVELS
    # ========================================================

    st.markdown(
        "### 🎯 PRICE LEVELS"
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

    # ========================================================
    # ENTRY + RISK
    # ========================================================

    st.markdown(
        "### 🛡️ ENTRY + RISK"
    )

    if (
        ems["ems"] < 45 or
        safe_num(last["RSI14"],50) >= 80
    ):

        entry = f"""
        <div class="box-grid">

            {price_box(
                "STATUS",
                "⚠️ WAIT",
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

    # ========================================================
    # SWING TARGETS
    # ========================================================

    st.markdown(
        "### 🎯 SWING TARGETS"
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

    # ========================================================
    # LONG TARGETS
    # ========================================================

    st.markdown(
        "### 🏆 LONG-TERM TARGETS"
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

    # ========================================================
    # BREAKOUT + RETEST
    # ========================================================

    st.markdown(
        "### 🚀 BREAKOUT + RETEST"
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

    # ========================================================
    # D / W / M
    # ========================================================

    st.markdown(
        "### 📅 D / W / M TREND"
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

    # ========================================================
    # CHART
    # ========================================================

    st.markdown(
        "### 📈 PRICE + EMA 10/20/50/100/200"
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

    chart_df = chart_df.dropna(
        how="all"
    )

    st.line_chart(
        chart_df,
        use_container_width=True
    )

    # ========================================================
    # WHY SIGNAL
    # ========================================================

    st.markdown(
        "### 🧠 WHY THIS SIGNAL?"
    )

    if (
        cmp >
        e10 >
        e20 >
        e50 >
        e100 >
        e200
    ):

        st.success(
            "✅ Full EMA bullish alignment: "
            "10 > 20 > 50 > 100 > 200"
        )

    elif (
        cmp <
        e10 <
        e20 <
        e50 <
        e100 <
        e200
    ):

        st.error(
            "🔴 Full EMA bearish alignment: "
            "10 < 20 < 50 < 100 < 200"
        )

    else:

        st.warning(
            "🟡 EMA structure mixed"
        )

    current_rsi = safe_num(
        last["RSI14"],
        50
    )

    if current_rsi >= 80:

        st.write(
            "🔴 RSI extreme overbought"
        )

    elif current_rsi >= 60:

        st.write(
            "🟢 RSI strong"
        )

    elif current_rsi >= 50:

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

    if ems["cpr_width"] <= .50:

        st.write(
            "🟢 Narrow CPR — breakout setup can be important"
        )

    elif ems["cpr_width"] <= 1.00:

        st.write(
            "🟡 Normal CPR range"
        )

    else:

        st.write(
            "🟠 Wide CPR — range is relatively broad"
        )

    if ems["price_value_score"] < 50:

        st.write(
            "🔴 Price Value: CMP significantly above reference value"
        )

    else:

        st.write(
            "🟢 Price Value: valuation zone acceptable"
        )

    # ========================================================
    # FOOTER
    # ========================================================

    st.caption(
        "🐂 RAJESH STOCK ANALYZER PRO V3.0 MASTER • "
        "NSE Manual Analyzer • EMS V3.1 • "
        "CPR = Central Pivot Range • "
        "Research & decision-support tool • "
        "Not financial advice."
    )
