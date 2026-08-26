# ============================================================
# 🐂 RAJESH STOCK ANALYZER PRO V2.6
# NSE • Manual 1–15 Stocks
# EMS V3 • D/W/M
# EMA 10/20/50/100/200 • CPR
# RSI • MACD • Supertrend • Volume
# Breakout + Retest • Swing + Long
# MOBILE FIRST • SAFE DATA • CRASH PROTECTED
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="RAJESH STOCK ANALYZER PRO V2.6",
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
    font-family: Arial, sans-serif;
}

.main {
    background:#050505;
}

.block-container {
    padding-top:.6rem;
    padding-left:.65rem;
    padding-right:.65rem;
}

/* HEADER */

.app-title {
    font-size:23px;
    font-weight:900;
    margin-bottom:2px;
}

.app-subtitle {
    font-size:11px;
    opacity:.72;
    margin-bottom:10px;
}

/* GRID */

.box-grid {
    display:grid;
    grid-template-columns:repeat(6,minmax(0,1fr));
    gap:5px;
    margin-bottom:8px;
}

/* ALL BOXES */

.metric-box,
.key-box,
.price-box,
.target-box,
.decision-box {
    border:1px solid #303030;
    border-radius:7px;
    background:#0e0e0e;
    padding:6px 4px;
    text-align:center;
    overflow:hidden;
}

.metric-title,
.key-title,
.price-title,
.target-title,
.decision-title {
    font-size:9px;
    font-weight:800;
    opacity:.72;
    white-space:nowrap;
}

.metric-value,
.key-value,
.price-value,
.target-value,
.decision-value {
    font-size:13px;
    font-weight:900;
    margin-top:2px;
    white-space:nowrap;
}

.key-grid {
    display:grid;
    grid-template-columns:repeat(6,minmax(0,1fr));
    gap:4px;
    margin-bottom:8px;
}

.key-box {
    min-height:52px;
    display:flex;
    flex-direction:column;
    justify-content:center;
}

.key-value {
    font-size:11px;
}

.target-grid {
    display:grid;
    grid-template-columns:repeat(3,minmax(0,1fr));
    gap:4px;
    margin-bottom:8px;
}

.target-box {
    min-height:50px;
    padding:5px 3px;
}

.target-value {
    font-size:12px;
}

.target-upside {
    font-size:9px;
    margin-top:1px;
    opacity:.8;
}

/* EMS COMPONENTS */

.ems-grid {
    display:grid;
    grid-template-columns:repeat(5,minmax(0,1fr));
    gap:4px;
}

.ems-box {
    border:1px solid #303030;
    border-radius:7px;
    background:#0d0d0d;
    padding:6px 3px;
    text-align:center;
}

.ems-value {
    font-size:12px;
    font-weight:900;
}

/* COLORS */

.green-box,
.key-positive {
    border-color:#176b36;
}

.blue-box {
    border-color:#244e86;
}

.red-box,
.key-negative {
    border-color:#7b2020;
}

.yellow-box,
.key-warning {
    border-color:#80651a;
}

.orange-box {
    border-color:#8a4c17;
}

/* SIGNAL */

.signal {
    font-size:19px;
    font-weight:900;
    padding:3px 0;
}

/* DECISION */

.decision-grid {
    display:grid;
    grid-template-columns:repeat(5,minmax(0,1fr));
    gap:4px;
}

.decision-box {
    min-height:52px;
}

/* MOBILE */

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

    .decision-grid {
        grid-template-columns:repeat(3,1fr);
    }
}

@media(max-width:500px) {

    .app-title {
        font-size:18px;
    }

    .box-grid {
        grid-template-columns:repeat(2,1fr);
        gap:4px;
    }

    .key-grid {
        grid-template-columns:repeat(3,1fr);
        gap:3px;
    }

    .key-box {
        min-height:49px;
    }

    .key-value {
        font-size:10px;
    }

    .metric-value {
        font-size:12px;
    }

    .target-grid {
        grid-template-columns:repeat(3,1fr);
    }

    .target-value {
        font-size:10px;
    }

    .target-title {
        font-size:8px;
    }

    .ems-grid {
        grid-template-columns:repeat(3,1fr);
    }

    .decision-grid {
        grid-template-columns:repeat(2,1fr);
    }

}

</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="app-title">🐂 RAJESH STOCK ANALYZER PRO V2.6</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="app-subtitle">'
    'NSE • Manual 1–15 Stocks • EMS V3 • D/W/M • '
    'EMA 10/20/50/100/200 • CPR • RSI • MACD • Supertrend • '
    'Momentum • Breakout + Retest • Swing + Long'
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

        if isinstance(value, pd.Series):
            if len(value) == 0:
                return default
            value = value.iloc[-1]

        if pd.isna(value):
            return default

        return float(value)

    except Exception:
        return default


def render_html(html):
    st.markdown(html, unsafe_allow_html=True)


def pct_change(a, b):

    a = safe_num(a)
    b = safe_num(b)

    if b == 0:
        return 0.0

    return ((a - b) / b) * 100


# ============================================================
# TECHNICAL INDICATORS
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

    for period in [10, 20, 50, 100, 200]:

        df[f"EMA{period}"] = close.ewm(
            span=period,
            adjust=False,
            min_periods=period
        ).mean()

    # --------------------------------------------------------
    # RSI 14
    # --------------------------------------------------------

    delta = close.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)

    df["RSI14"] = 100 - (
        100 / (1 + rs)
    )

    # --------------------------------------------------------
    # MACD 12/26/9
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
        df["MACD"] - df["MACD_SIGNAL"]
    )

    # --------------------------------------------------------
    # ATR 10
    # --------------------------------------------------------

    prev_close = close.shift(1)

    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()

    true_range = pd.concat(
        [tr1, tr2, tr3],
        axis=1
    ).max(axis=1)

    df["ATR10"] = true_range.rolling(10).mean()

    # --------------------------------------------------------
    # SUPERTREND 10 / 3
    # --------------------------------------------------------

    multiplier = 3.0

    hl2 = (high + low) / 2

    basic_upper = (
        hl2 + multiplier * df["ATR10"]
    )

    basic_lower = (
        hl2 - multiplier * df["ATR10"]
    )

    final_upper = basic_upper.copy()
    final_lower = basic_lower.copy()

    for i in range(1, len(df)):

        prev_i = i - 1

        if (
            basic_upper.iloc[i]
            < final_upper.iloc[prev_i]
            or close.iloc[prev_i]
            > final_upper.iloc[prev_i]
        ):
            final_upper.iloc[i] = basic_upper.iloc[i]
        else:
            final_upper.iloc[i] = final_upper.iloc[prev_i]

        if (
            basic_lower.iloc[i]
            > final_lower.iloc[prev_i]
            or close.iloc[prev_i]
            < final_lower.iloc[prev_i]
        ):
            final_lower.iloc[i] = basic_lower.iloc[i]
        else:
            final_lower.iloc[i] = final_lower.iloc[prev_i]

    supertrend = pd.Series(
        index=df.index,
        dtype=float
    )

    direction = pd.Series(
        index=df.index,
        dtype=int
    )

    direction.iloc[0] = 1
    supertrend.iloc[0] = final_lower.iloc[0]

    for i in range(1, len(df)):

        if (
            direction.iloc[i - 1] == 1
            and close.iloc[i] < final_lower.iloc[i]
        ):
            direction.iloc[i] = -1

        elif (
            direction.iloc[i - 1] == -1
            and close.iloc[i] > final_upper.iloc[i]
        ):
            direction.iloc[i] = 1

        else:
            direction.iloc[i] = direction.iloc[i - 1]

        if direction.iloc[i] == 1:
            supertrend.iloc[i] = final_lower.iloc[i]
        else:
            supertrend.iloc[i] = final_upper.iloc[i]

    df["SUPERTREND"] = supertrend
    df["SUPERTREND_DIRECTION"] = direction

    # --------------------------------------------------------
    # VOLUME
    # --------------------------------------------------------

    df["VOLUME_AVG20"] = volume.rolling(20).mean()

    df["VOLUME_RATIO"] = (
        volume /
        df["VOLUME_AVG20"].replace(0, np.nan)
    )

    # --------------------------------------------------------
    # 52 WEEK HIGH / LOW
    # --------------------------------------------------------

    df["52W_HIGH"] = close.rolling(252).max()
    df["52W_LOW"] = close.rolling(252).min()

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
        ["BC", "TC"]
    ].min(axis=1)

    df["CPR_HIGH"] = df[
        ["BC", "TC"]
    ].max(axis=1)

    # --------------------------------------------------------
    # 20 DAY SUPPORT / RESISTANCE
    # --------------------------------------------------------

    df["SUPPORT20"] = low.rolling(20).min()
    df["RESISTANCE20"] = high.rolling(20).max()

    # --------------------------------------------------------
    # BREAKOUT
    # --------------------------------------------------------

    df["BREAKOUT_LEVEL"] = (
        df["RESISTANCE20"].shift(1)
    )

    df["BREAKOUT_ABOVE"] = (
        close > df["BREAKOUT_LEVEL"]
    )

    return df


# ============================================================
# EMA TREND SCORE
# ============================================================

def ema_score(last):

    close = safe_num(last.get("Close"))

    e10 = safe_num(last.get("EMA10"))
    e20 = safe_num(last.get("EMA20"))
    e50 = safe_num(last.get("EMA50"))
    e100 = safe_num(last.get("EMA100"))
    e200 = safe_num(last.get("EMA200"))

    score = 0

    if close > e10:
        score += 10

    if e10 > e20:
        score += 10

    if e20 > e50:
        score += 10

    if e50 > e100:
        score += 10

    if e100 > e200:
        score += 10

    return score


# ============================================================
# SIGNAL ENGINE / EMS V3
# ============================================================

def signal_engine(df):

    last = df.iloc[-1]

    close = safe_num(last["Close"])

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

    st_direction = safe_num(
        last["SUPERTREND_DIRECTION"],
        0
    )

    support = safe_num(
        last["SUPPORT20"],
        close * .95
    )

    resistance = safe_num(
        last["RESISTANCE20"],
        close * 1.05
    )

    # --------------------------------------------------------
    # TREND SCORE 0-25
    # --------------------------------------------------------

    e_score = ema_score(last)

    trend_score = e_score / 2

    # --------------------------------------------------------
    # MOMENTUM SCORE 0-20
    # --------------------------------------------------------

    momentum_score = 0

    if rsi >= 60:
        momentum_score += 12

    elif rsi >= 50:
        momentum_score += 8

    elif rsi >= 40:
        momentum_score += 4

    if macd > macd_signal:
        momentum_score += 8

    # --------------------------------------------------------
    # SUPERTREND 0-15
    # --------------------------------------------------------

    supertrend_score = 15 if st_direction > 0 else 0

    # --------------------------------------------------------
    # VOLUME 0-10
    # --------------------------------------------------------

    volume_score = 0

    if volume >= 2:
        volume_score = 10

    elif volume >= 1.5:
        volume_score = 7

    elif volume >= 1:
        volume_score = 4

    # --------------------------------------------------------
    # BREAKOUT 0-15
    # --------------------------------------------------------

    breakout_level = safe_num(
        last["BREAKOUT_LEVEL"],
        resistance
    )

    breakout_score = 0

    if close > breakout_level:

        if volume >= 2:
            breakout_score = 15
        else:
            breakout_score = 8

    # --------------------------------------------------------
    # SUPPORT / RISK 0-15
    # --------------------------------------------------------

    risk_score = 0

    if close > support:
        risk_score += 8

    if close > safe_num(last["EMA200"], close):
        risk_score += 7

    # --------------------------------------------------------
    # EMS TOTAL
    # --------------------------------------------------------

    ems = (
        trend_score +
        momentum_score +
        supertrend_score +
        volume_score +
        breakout_score +
        risk_score
    )

    ems = int(
        max(0, min(100, round(ems)))
    )

    # --------------------------------------------------------
    # TECH SCORE
    # --------------------------------------------------------

    tech = int(
        max(
            0,
            min(
                100,
                round(
                    (
                        trend_score * 2.0 +
                        momentum_score * 2.0 +
                        supertrend_score * 1.5 +
                        volume_score
                    )
                )
            )
        )
    )

    # --------------------------------------------------------
    # REGIME
    # --------------------------------------------------------

    if ems >= 70:
        regime = "🐂 BULL"

    elif ems >= 50:
        regime = "🟡 NEUTRAL"

    else:
        regime = "🐻 BEAR"

    # --------------------------------------------------------
    # DECISION
    # --------------------------------------------------------

    if ems >= 75 and tech >= 70:
        decision = "🟢 ADD"
        signal = "🚦 BUY"

    elif ems >= 60:
        decision = "🟡 HOLD"
        signal = "🟡 HOLD"

    elif ems >= 45:
        decision = "🟡 WAIT"
        signal = "⏳ WAIT"

    elif ems >= 30:
        decision = "🟠 REDUCE"
        signal = "⚠️ REDUCE"

    else:
        decision = "🔴 EXIT"
        signal = "🚦 SELL / EXIT"

    return {
        "ems": ems,
        "tech": tech,
        "trend_score": int(round(trend_score)),
        "momentum_score": momentum_score,
        "supertrend_score": supertrend_score,
        "volume_score": volume_score,
        "breakout_score": breakout_score,
        "risk_score": risk_score,
        "regime": regime,
        "signal": signal,
        "decision": decision,
        "ema_bull": (
            close >
            safe_num(last["EMA10"]) >
            safe_num(last["EMA20"]) >
            safe_num(last["EMA50"]) >
            safe_num(last["EMA100"]) >
            safe_num(last["EMA200"])
        ),
        "ema_bear": (
            close <
            safe_num(last["EMA10"]) <
            safe_num(last["EMA20"]) <
            safe_num(last["EMA50"]) <
            safe_num(last["EMA100"]) <
            safe_num(last["EMA200"])
        ),
        "breakout_level": breakout_level
    }


# ============================================================
# KEY INDICATOR BOX
# ============================================================

def key_box(title, value, css=""):

    return f"""
    <div class="key-box {css}">
        <div class="key-title">{title}</div>
        <div class="key-value">{value}</div>
    </div>
    """


def render_key_indicators(df):

    last = df.iloc[-1]

    e10 = safe_num(last["EMA10"])
    e20 = safe_num(last["EMA20"])
    e50 = safe_num(last["EMA50"])
    e100 = safe_num(last["EMA100"])
    e200 = safe_num(last["EMA200"])

    cpr_low = safe_num(last["CPR_LOW"])
    cpr_high = safe_num(last["CPR_HIGH"])

    rsi = safe_num(last["RSI14"], 50)

    macd = safe_num(last["MACD"])
    macd_signal = safe_num(last["MACD_SIGNAL"])

    volume = safe_num(last["VOLUME_RATIO"])

    high52 = safe_num(last["52W_HIGH"])
    low52 = safe_num(last["52W_LOW"])

    close = safe_num(last["Close"])

    st_dir = safe_num(
        last["SUPERTREND_DIRECTION"]
    )

    breakout = safe_num(
        last["BREAKOUT_LEVEL"],
        close
    )

    # EMA colors individually

    def ema_css(current, previous):

        if current > previous:
            return "key-positive"

        return "key-negative"

    html = f"""
    <div class="key-grid">

        {key_box(
            "EMA 10",
            f"₹{e10:,.2f}",
            ema_css(e10, e20)
        )}

        {key_box(
            "EMA 20",
            f"₹{e20:,.2f}",
            ema_css(e20, e50)
        )}

        {key_box(
            "EMA 50",
            f"₹{e50:,.2f}",
            ema_css(e50, e100)
        )}

        {key_box(
            "EMA 100",
            f"₹{e100:,.2f}",
            ema_css(e100, e200)
        )}

        {key_box(
            "EMA 200",
            f"₹{e200:,.2f}",
            "key-positive"
            if close > e200
            else "key-negative"
        )}

        {key_box(
            "CPR",
            f"₹{cpr_low:,.0f} – ₹{cpr_high:,.0f}",
            "key-positive"
            if close > cpr_high
            else (
                "key-negative"
                if close < cpr_low
                else "key-warning"
            )
        )}

        {key_box(
            "RSI 14",
            f"{rsi:.1f}",
            "key-positive"
            if rsi >= 50
            else "key-negative"
        )}

        {key_box(
            "MACD",
            "🟢 BULL"
            if macd > macd_signal
            else "🔴 BEAR",
            "key-positive"
            if macd > macd_signal
            else "key-negative"
        )}

        {key_box(
            "SUPERTREND",
            "🟢 BULL"
            if st_dir > 0
            else "🔴 BEAR",
            "key-positive"
            if st_dir > 0
            else "key-negative"
        )}

        {key_box(
            "VOLUME",
            f"{volume:.2f}x",
            "key-positive"
            if volume >= 1.5
            else "key-warning"
        )}

        {key_box(
            "52W HIGH",
            f"₹{high52:,.0f}",
            ""
        )}

        {key_box(
            "52W LOW",
            f"₹{low52:,.0f}",
            ""
        )}

        {key_box(
            "BREAKOUT",
            f"₹{breakout:,.2f}",
            "key-positive"
            if close > breakout
            else "key-warning"
        )}

        {key_box(
            "PRICE vs CPR",
            "🟢 ABOVE"
            if close > cpr_high
            else (
                "🔴 BELOW"
                if close < cpr_low
                else "🟡 INSIDE"
            ),
            "key-positive"
            if close > cpr_high
            else (
                "key-negative"
                if close < cpr_low
                else "key-warning"
            )
        )}

    </div>
    """

    render_html(html)


# ============================================================
# PRICE LEVELS
# ============================================================

def render_price_levels(df):

    last = df.iloc[-1]

    cmp = safe_num(last["Close"])

    support = safe_num(
        last["SUPPORT20"],
        cmp * .95
    )

    resistance = safe_num(
        last["RESISTANCE20"],
        cmp * 1.05
    )

    high52 = safe_num(
        last["52W_HIGH"],
        resistance
    )

    low52 = safe_num(
        last["52W_LOW"],
        support
    )

    html = f"""
    <div class="box-grid">

        <div class="price-box blue-box">
            <div class="price-title">SUPPORT</div>
            <div class="price-value">
                ₹{support:,.2f}
            </div>
        </div>

        <div class="price-box blue-box">
            <div class="price-title">RESISTANCE</div>
            <div class="price-value">
                ₹{resistance:,.2f}
            </div>
        </div>

        <div class="price-box yellow-box">
            <div class="price-title">52W HIGH</div>
            <div class="price-value">
                ₹{high52:,.2f}
            </div>
        </div>

        <div class="price-box blue-box">
            <div class="price-title">52W LOW</div>
            <div class="price-value">
                ₹{low52:,.2f}
            </div>
        </div>

    </div>
    """

    render_html(html)

    return support, resistance


# ============================================================
# ENTRY / RISK
# ============================================================

def render_entry_risk(df, signal):

    last = df.iloc[-1]

    cmp = safe_num(last["Close"])

    support = safe_num(
        last["SUPPORT20"],
        cmp * .95
    )

    resistance = safe_num(
        last["RESISTANCE20"],
        cmp * 1.05
    )

    ema50 = safe_num(
        last["EMA50"],
        cmp
    )

    ema200 = safe_num(
        last["EMA200"],
        cmp
    )

    breakout = safe_num(
        signal["breakout_level"],
        resistance
    )

    stop_loss = min(
        support * .97,
        ema200 * .97
    )

    # --------------------------------------------------------
    # BEAR
    # --------------------------------------------------------

    if signal["regime"] == "🐻 BEAR":

        html = f"""
        <div class="box-grid">

            <div class="price-box red-box">
                <div class="price-title">STATUS</div>
                <div class="price-value">
                    🚫 NO BUY
                </div>
            </div>

            <div class="price-box blue-box">
                <div class="price-title">SUPPORT</div>
                <div class="price-value">
                    ₹{support:,.2f}
                </div>
            </div>

            <div class="price-box blue-box">
                <div class="price-title">RESISTANCE</div>
                <div class="price-value">
                    ₹{resistance:,.2f}
                </div>
            </div>

            <div class="price-box red-box">
                <div class="price-title">STOP LOSS</div>
                <div class="price-value">
                    ₹{stop_loss:,.2f}
                </div>
            </div>

            <div class="price-box blue-box">
                <div class="price-title">BREAKOUT</div>
                <div class="price-value">
                    ₹{breakout:,.2f}
                </div>
            </div>

        </div>
        """

        render_html(html)

        return

    # --------------------------------------------------------
    # NON-BEAR
    # --------------------------------------------------------

    buy_low = min(
        support,
        ema50
    )

    buy_high = max(
        support,
        ema50
    )

    breakout_entry = breakout * 1.003

    html = f"""
    <div class="box-grid">

        <div class="price-box green-box">
            <div class="price-title">
                🟢 BUY ZONE
            </div>
            <div class="price-value">
                ₹{buy_low:,.0f} – ₹{buy_high:,.0f}
            </div>
        </div>

        <div class="price-box green-box">
            <div class="price-title">
                🟢 BUY ON DIP
            </div>
            <div class="price-value">
                ₹{support:,.0f} – ₹{ema50:,.0f}
            </div>
        </div>

        <div class="price-box blue-box">
            <div class="price-title">
                🚀 BREAKOUT
            </div>
            <div class="price-value">
                ₹{breakout_entry:,.2f}
            </div>
        </div>

        <div class="price-box red-box">
            <div class="price-title">
                STOP LOSS
            </div>
            <div class="price-value">
                ₹{stop_loss:,.2f}
            </div>
        </div>

    </div>
    """

    render_html(html)


# ============================================================
# TARGET BOX
# ============================================================

def target_box(title, price, upside):

    return f"""
    <div class="target-box">
        <div class="target-title">{title}</div>
        <div class="target-value">
            ₹{price:,.2f}
        </div>
        <div class="target-upside">
            {upside:+.1f}%
        </div>
    </div>
    """


def render_targets(cmp):

    swing1 = cmp * 1.04
    swing2 = cmp * 1.09
    swing3 = cmp * 1.16

    long1 = cmp * 1.15
    long2 = cmp * 1.25
    long3 = cmp * 1.40

    st.markdown("### 🎯 SWING TARGETS")

    render_html(f"""
    <div class="target-grid">

        {target_box(
            "SWING T1",
            swing1,
            4
        )}

        {target_box(
            "SWING T2",
            swing2,
            9
        )}

        {target_box(
            "SWING T3",
            swing3,
            16
        )}

    </div>
    """)

    st.markdown("### 🏆 LONG-TERM TARGETS")

    render_html(f"""
    <div class="target-grid">

        {target_box(
            "LONG T1",
            long1,
            15
        )}

        {target_box(
            "LONG T2",
            long2,
            25
        )}

        {target_box(
            "LONG T3",
            long3,
            40
        )}

    </div>
    """)


# ============================================================
# EMS BREAKDOWN
# ============================================================

def render_ems(signal):

    st.markdown("### 🧠 EMS V3 BREAKDOWN")

    html = f"""
    <div class="ems-grid">

        <div class="ems-box">
            <div class="key-title">TREND</div>
            <div class="ems-value">
                {signal["trend_score"]}/25
            </div>
        </div>

        <div class="ems-box">
            <div class="key-title">MOMENTUM</div>
            <div class="ems-value">
                {signal["momentum_score"]}/20
            </div>
        </div>

        <div class="ems-box">
            <div class="key-title">SUPERTREND</div>
            <div class="ems-value">
                {signal["supertrend_score"]}/15
            </div>
        </div>

        <div class="ems-box">
            <div class="key-title">VOLUME</div>
            <div class="ems-value">
                {signal["volume_score"]}/10
            </div>
        </div>

        <div class="ems-box">
            <div class="key-title">BREAKOUT</div>
            <div class="ems-value">
                {signal["breakout_score"]}/15
            </div>
        </div>

        <div class="ems-box">
            <div class="key-title">RISK / SUPPORT</div>
            <div class="ems-value">
                {signal["risk_score"]}/15
            </div>
        </div>

        <div class="ems-box">
            <div class="key-title">TOTAL EMS</div>
            <div class="ems-value">
                {signal["ems"]}/100
            </div>
        </div>

    </div>
    """

    render_html(html)


# ============================================================
# BREAKOUT / RETEST
# ============================================================

def render_breakout(df, signal):

    last = df.iloc[-1]

    close = safe_num(last["Close"])

    breakout = safe_num(
        signal["breakout_level"],
        close
    )

    volume = safe_num(
        last["VOLUME_RATIO"]
    )

    ema20 = safe_num(
        last["EMA20"],
        close
    )

    confirmations = 0

    if close > breakout:
        confirmations += 1

    if volume >= 1.5:
        confirmations += 1

    if close > ema20:
        confirmations += 1

    if safe_num(last["RSI14"],50) >= 50:
        confirmations += 1

    if safe_num(last["MACD"]) > safe_num(last["MACD_SIGNAL"]):
        confirmations += 1

    if safe_num(last["SUPERTREND_DIRECTION"]) > 0:
        confirmations += 1

    if confirmations >= 5:
        status = "🚀 CONFIRMED"
        css = "green-box"

    elif confirmations >= 3:
        status = "🟡 WATCH"
        css = "yellow-box"

    else:
        status = "🔴 FAILED / WEAK"
        css = "red-box"

    retest_low = breakout * .985
    retest_high = breakout * 1.01

    st.markdown("### 🚀 BREAKOUT + RETEST")

    render_html(f"""
    <div class="box-grid">

        <div class="price-box {css}">
            <div class="price-title">STATUS</div>
            <div class="price-value">
                {status}
            </div>
        </div>

        <div class="price-box blue-box">
            <div class="price-title">
                BREAKOUT LEVEL
            </div>
            <div class="price-value">
                ₹{breakout:,.2f}
            </div>
        </div>

        <div class="price-box yellow-box">
            <div class="price-title">
                RETEST ZONE
            </div>
            <div class="price-value">
                ₹{retest_low:,.0f} – ₹{retest_high:,.0f}
            </div>
        </div>

        <div class="price-box blue-box">
            <div class="price-title">
                CONFIRMATIONS
            </div>
            <div class="price-value">
                {confirmations}/6
            </div>
        </div>

    </div>
    """)


# ============================================================
# WHY SIGNAL
# ============================================================

def render_why(df, signal):

    last = df.iloc[-1]

    st.markdown("### 🧠 WHY THIS SIGNAL?")

    if signal["ema_bull"]:
        st.success(
            "🟢 EMA 10 > 20 > 50 > 100 > 200"
        )

    elif signal["ema_bear"]:
        st.error(
            "🔴 EMA 10 < 20 < 50 < 100 < 200"
        )

    else:
        st.warning(
            "🟡 EMA structure mixed"
        )

    rsi = safe_num(
        last["RSI14"],
        50
    )

    if rsi >= 60:
        st.write("🟢 RSI strong")

    elif rsi >= 50:
        st.write("🟢 RSI positive")

    elif rsi >= 40:
        st.write("🟡 RSI neutral / weak")

    else:
        st.write("🔴 RSI weak")

    if safe_num(last["MACD"]) > safe_num(last["MACD_SIGNAL"]):
        st.write("🟢 MACD bullish")
    else:
        st.write("🔴 MACD bearish")

    if safe_num(last["SUPERTREND_DIRECTION"]) > 0:
        st.write("🟢 Supertrend bullish")
    else:
        st.write("🔴 Supertrend bearish")

    volume = safe_num(
        last["VOLUME_RATIO"]
    )

    if volume >= 2:
        st.write("🚀 Volume breakout confirmed")

    elif volume >= 1.5:
        st.write("🟢 Volume improving")

    else:
        st.write("🟡 Volume confirmation pending")


# ============================================================
# STOCK DOWNLOAD
# ============================================================

def download_stock(symbol):

    ticker = symbol.upper().strip()

    if ticker.endswith(".NS"):
        ticker = ticker
    else:
        ticker = ticker + ".NS"

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

        # MultiIndex protection

        if isinstance(df.columns, pd.MultiIndex):

            try:
                df.columns = df.columns.get_level_values(0)

            except Exception:
                df.columns = [
                    c[0]
                    if isinstance(c, tuple)
                    else c
                    for c in df.columns
                ]

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

        df = df[required].copy()

        for col in required:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

        df = df.dropna(
            subset=[
                "Open",
                "High",
                "Low",
                "Close"
            ]
        )

        if len(df) < 220:
            return None

        df = calculate_indicators(df)

        return df

    except Exception:

        return None


# ============================================================
# SESSION STATE
# ============================================================

if "stocks" not in st.session_state:
    st.session_state.stocks = []

if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = {}

if "last_analysis" not in st.session_state:
    st.session_state.last_analysis = "—"


# ============================================================
# ADD STOCK
# ============================================================

st.markdown("### ➕ ADD STOCK")

stock_input = st.text_input(
    "NSE Symbol",
    placeholder="Example: BSE / RATNAVEER / AIIL"
)

if st.button(
    "➕ ADD",
    use_container_width=True
):

    symbol = (
        stock_input
        .upper()
        .replace(".NS","")
        .strip()
    )

    if not symbol:

        st.warning(
            "NSE symbol નાખો."
        )

    elif symbol in st.session_state.stocks:

        st.warning(
            f"{symbol} પહેલેથી watchlistમાં છે."
        )

    elif len(st.session_state.stocks) >= 15:

        st.error(
            "Maximum 15 stocks."
        )

    else:

        st.session_state.stocks.append(
            symbol
        )

        st.rerun()


# ============================================================
# WATCHLIST
# ============================================================

st.markdown(
    f"### 📋 MY STOCKS — "
    f"{len(st.session_state.stocks)}/15"
)

if st.session_state.stocks:

    st.write(
        " • ".join(
            st.session_state.stocks
        )
    )

    if st.button(
        "🗑️ CLEAR ALL",
        use_container_width=True
    ):

        st.session_state.stocks = []
        st.session_state.analysis_results = {}
        st.rerun()


# ============================================================
# ANALYZE BUTTON
# ============================================================

if st.button(
    "🔍 ANALYZE ALL",
    use_container_width=True
):

    if not st.session_state.stocks:

        st.warning(
            "પહેલા stock add કરો."
        )

    else:

        st.session_state.analysis_results = {}

        progress = st.progress(0)

        total = len(
            st.session_state.stocks
        )

        for index, symbol in enumerate(
            st.session_state.stocks
        ):

            df = download_stock(symbol)

            if df is not None:

                signal = signal_engine(df)

                st.session_state.analysis_results[
                    symbol
                ] = (
                    df,
                    signal
                )

            progress.progress(
                int(
                    ((index + 1) / total) * 100
                )
            )

        st.session_state.last_analysis = (
            datetime.now().strftime(
                "%d/%m/%Y %H:%M"
            )
        )


# ============================================================
# LAST ANALYSIS
# ============================================================

if st.session_state.last_analysis != "—":

    st.caption(
        f"LAST ANALYSIS: "
        f"{st.session_state.last_analysis}"
    )


# ============================================================
# DASHBOARD
# ============================================================

results = st.session_state.analysis_results

if results:

    analyzed = len(results)

    positive = sum(
        1
        for _, signal in results.values()
        if signal["ems"] >= 60
    )

    risk = sum(
        1
        for _, signal in results.values()
        if signal["ems"] < 45
    )

    avg_ems = int(
        round(
            np.mean([
                signal["ems"]
                for _, signal in results.values()
            ])
        )
    )

    avg_tech = int(
        round(
            np.mean([
                signal["tech"]
                for _, signal in results.values()
            ])
        )
    )

    bulls = sum(
        1
        for _, signal in results.values()
        if signal["regime"] == "🐂 BULL"
    )

    bears = sum(
        1
        for _, signal in results.values()
        if signal["regime"] == "🐻 BEAR"
    )

    st.markdown("### 🚦 SMART SIGNAL DASHBOARD")

    dashboard = f"""
    <div class="box-grid">

        <div class="metric-box">
            <div class="metric-title">
                ANALYZED
            </div>
            <div class="metric-value">
                📊 {analyzed}
            </div>
        </div>

        <div class="metric-box">
            <div class="metric-title">
                POSITIVE
            </div>
            <div class="metric-value">
                🟢 {positive}
            </div>
        </div>

        <div class="metric-box">
            <div class="metric-title">
                RISK / EXIT
            </div>
            <div class="metric-value">
                ⚠️ {risk}
            </div>
        </div>

        <div class="metric-box">
            <div class="metric-title">
                AVG EMS
            </div>
            <div class="metric-value">
                🧠 {avg_ems}/100
            </div>
        </div>

        <div class="metric-box">
            <div class="metric-title">
                AVG TECH
            </div>
            <div class="metric-value">
                📈 {avg_tech}/100
            </div>
        </div>

        <div class="metric-box">
            <div class="metric-title">
                BULL / BEAR
            </div>
            <div class="metric-value">
                🐂 {bulls} / 🐻 {bears}
            </div>
        </div>

    </div>
    """

    render_html(dashboard)


# ============================================================
# DISPLAY STOCKS
# ============================================================

for symbol, result in results.items():

    df, signal = result

    last = df.iloc[-1]

    cmp = safe_num(
        last["Close"]
    )

    st.markdown("---")

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.markdown(
        f"## 🏢 {symbol}"
    )

    st.caption(
        f"{symbol}.NS • NSE • "
        f"Analysis: "
        f"{st.session_state.last_analysis}"
    )

    st.markdown(
        f'<div class="signal">'
        f'{signal["regime"]} &nbsp; '
        f'{signal["signal"]}'
        f'</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    st.markdown(
        "### 🚦 SMART SIGNAL DASHBOARD"
    )

    summary = f"""
    <div class="box-grid">

        <div class="metric-box">
            <div class="metric-title">
                CMP
            </div>
            <div class="metric-value">
                ₹{cmp:,.2f}
            </div>
        </div>

        <div class="metric-box">
            <div class="metric-title">
                EMS
            </div>
            <div class="metric-value">
                {signal["ems"]}/100
            </div>
        </div>

        <div class="metric-box">
            <div class="metric-title">
                TECH
            </div>
            <div class="metric-value">
                {signal["tech"]}/100
            </div>
        </div>

        <div class="metric-box">
            <div class="metric-title">
                RSI
            </div>
            <div class="metric-value">
                {safe_num(last["RSI14"],50):.1f}
            </div>
        </div>

        <div class="metric-box">
            <div class="metric-title">
                VOLUME
            </div>
            <div class="metric-value">
                {safe_num(last["VOLUME_RATIO"],0):.2f}x
            </div>
        </div>

        <div class="metric-box">
            <div class="metric-title">
                DECISION
            </div>
            <div class="metric-value">
                {signal["decision"]}
            </div>
        </div>

    </div>
    """

    render_html(summary)

    # --------------------------------------------------------
    # KEY INDICATORS
    # --------------------------------------------------------

    st.markdown(
        "### 📊 KEY INDICATORS"
    )

    render_key_indicators(df)

    # --------------------------------------------------------
    # PRICE LEVELS
    # --------------------------------------------------------

    st.markdown(
        "### 🎯 PRICE LEVELS"
    )

    render_price_levels(df)

    # --------------------------------------------------------
    # ENTRY / RISK
    # --------------------------------------------------------

    st.markdown(
        "### 🛡️ ENTRY + RISK"
    )

    render_entry_risk(
        df,
        signal
    )

    # --------------------------------------------------------
    # TARGETS
    # --------------------------------------------------------

    render_targets(cmp)

    # --------------------------------------------------------
    # BREAKOUT
    # --------------------------------------------------------

    render_breakout(
        df,
        signal
    )

    # --------------------------------------------------------
    # EMS
    # --------------------------------------------------------

    render_ems(signal)

    # --------------------------------------------------------
    # D/W/M
    # --------------------------------------------------------

    st.markdown(
        "### 📊 D / W / M"
    )

    daily_score = signal["tech"]

    # Approximate multi-timeframe trend using resampling

    try:

        weekly = (
            df.resample("W")
            .agg({
                "Open":"first",
                "High":"max",
                "Low":"min",
                "Close":"last",
                "Volume":"sum"
            })
            .dropna()
        )

        monthly = (
            df.resample("ME")
            .agg({
                "Open":"first",
                "High":"max",
                "Low":"min",
                "Close":"last",
                "Volume":"sum"
            })
            .dropna()
        )

        weekly = calculate_indicators(
            weekly
        )

        monthly = calculate_indicators(
            monthly
        )

        w_last = weekly.iloc[-1]
        m_last = monthly.iloc[-1]

        weekly_score = ema_score(
            w_last
        ) * 2

        monthly_score = ema_score(
            m_last
        ) * 2

        d_score = int(
            max(
                0,
                min(100, daily_score)
            )
        )

        w_score = int(
            max(
                0,
                min(100, weekly_score)
            )
        )

        m_score = int(
            max(
                0,
                min(100, monthly_score)
            )
        )

        dwm_score = int(
            round(
                d_score * .5 +
                w_score * .3 +
                m_score * .2
            )
        )

    except Exception:

        d_score = daily_score
        w_score = daily_score
        m_score = daily_score
        dwm_score = daily_score

    render_html(f"""
    <div class="box-grid">

        <div class="metric-box">
            <div class="metric-title">DAILY</div>
            <div class="metric-value">
                {d_score}/100
            </div>
        </div>

        <div class="metric-box">
            <div class="metric-title">WEEKLY</div>
            <div class="metric-value">
                {w_score}/100
            </div>
        </div>

        <div class="metric-box">
            <div class="metric-title">MONTHLY</div>
            <div class="metric-value">
                {m_score}/100
            </div>
        </div>

        <div class="metric-box">
            <div class="metric-title">D/W/M MASTER</div>
            <div class="metric-value">
                {dwm_score}/100
            </div>
        </div>

    </div>
    """)

    # --------------------------------------------------------
    # CHART
    # --------------------------------------------------------

    st.markdown(
        "### 📈 PRICE + 10 INDICATOR CHART"
    )

    chart_columns = [
        "Close",
        "EMA10",
        "EMA20",
        "EMA50",
        "EMA100",
        "EMA200",
        "SUPERTREND",
        "CPR_LOW",
        "CPR_HIGH"
    ]

    chart_df = df[
        [
            c
            for c in chart_columns
            if c in df.columns
        ]
    ].tail(180)

    st.line_chart(
        chart_df,
        use_container_width=True
    )

    # --------------------------------------------------------
    # CHART NOTE
    # --------------------------------------------------------

    st.caption(
        "📈 Chart: Close + EMA10 + EMA20 + "
        "EMA50 + EMA100 + EMA200 + "
        "Supertrend + CPR Low/High"
    )

    # --------------------------------------------------------
    # WHY SIGNAL
    # --------------------------------------------------------

    render_why(
        df,
        signal
    )

# ============================================================
# NO RESULTS
# ============================================================

if (
    st.session_state.stocks
    and not results
    and st.session_state.last_analysis != "—"
):

    st.warning(
        "⚠️ કોઈ stock માટે market data ઉપલબ્ધ નથી. "
        "NSE symbol તપાસો અથવા ફરી ANALYZE ALL કરો."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "🐂 RAJESH STOCK ANALYZER PRO V2.6 • "
    "NSE Manual Analyzer • EMS V3 • "
    "Research & decision-support tool • "
    "Not financial advice."
)
