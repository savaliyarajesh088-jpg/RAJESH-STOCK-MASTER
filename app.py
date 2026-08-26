# ============================================================
# 🐂 RAJESH STOCK ANALYZER PRO V2.4
# NSE • Manual 1–15 Stocks
# EMS V3 • D/W/M
# EMA 10/20/30/40/50 • CPR
# Momentum • Breakout + Retest • Swing + Long
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
    page_title="RAJESH STOCK ANALYZER PRO V2.4",
    page_icon="🐂",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CSS — MOBILE FIRST / COMPACT BOXES
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
    padding-top:0.7rem;
    padding-left:0.7rem;
    padding-right:0.7rem;
}

/* HEADER */

.app-title {
    font-size:24px;
    font-weight:800;
    margin-bottom:2px;
}

.app-subtitle {
    font-size:12px;
    opacity:.75;
    margin-bottom:12px;
}

/* GENERAL BOX */

.box-grid {
    display:grid;
    grid-template-columns:repeat(6, minmax(0,1fr));
    gap:6px;
    margin-bottom:10px;
}

.metric-box,
.key-box,
.price-box,
.target-box {
    border:1px solid #303030;
    border-radius:8px;
    background:#101010;
    padding:7px 5px;
    text-align:center;
    overflow:hidden;
}

.metric-title,
.key-title,
.price-title,
.target-title {
    font-size:10px;
    font-weight:700;
    opacity:.75;
    white-space:nowrap;
}

.metric-value,
.key-value,
.price-value,
.target-value {
    font-size:14px;
    font-weight:800;
    margin-top:3px;
    white-space:nowrap;
}

.target-upside {
    font-size:10px;
    margin-top:2px;
    opacity:.8;
}

/* KEY INDICATORS */

.key-grid {
    display:grid;
    grid-template-columns:repeat(6, minmax(0,1fr));
    gap:5px;
}

.key-box {
    min-height:58px;
    display:flex;
    flex-direction:column;
    justify-content:center;
}

.key-value {
    font-size:12px;
}

/* TARGETS */

.target-grid {
    display:grid;
    grid-template-columns:repeat(6, minmax(0,1fr));
    gap:5px;
}

.target-box {
    min-height:57px;
    padding:6px 3px;
}

.target-value {
    font-size:13px;
}

.target-upside {
    font-size:9px;
}

/* COLORS */

.key-positive {
    border-color:#176b36;
}

.key-negative {
    border-color:#7b2020;
}

.key-warning {
    border-color:#80651a;
}

.green-box {
    border-color:#176b36;
}

.blue-box {
    border-color:#244e86;
}

.red-box {
    border-color:#7b2020;
}

.yellow-box {
    border-color:#80651a;
}

/* SIGNAL */

.signal {
    font-size:20px;
    font-weight:900;
    padding:5px 0;
}

/* MOBILE */

@media (max-width: 900px) {

    .box-grid {
        grid-template-columns:repeat(3,1fr);
    }

    .key-grid {
        grid-template-columns:repeat(3,1fr);
    }

    .target-grid {
        grid-template-columns:repeat(3,1fr);
    }

}

@media (max-width: 500px) {

    .app-title {
        font-size:19px;
    }

    .box-grid {
        grid-template-columns:repeat(2,1fr);
    }

    .key-grid {
        grid-template-columns:repeat(3,1fr);
        gap:4px;
    }

    .target-grid {
        grid-template-columns:repeat(3,1fr);
        gap:4px;
    }

    .key-box {
        min-height:52px;
    }

    .key-value {
        font-size:11px;
    }

    .target-value {
        font-size:11px;
    }

    .target-title {
        font-size:9px;
    }

    .metric-value {
        font-size:13px;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="app-title">🐂 RAJESH STOCK ANALYZER PRO V2.4</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="app-subtitle">'
    'NSE • Manual 1–15 Stocks • EMS V3 • D/W/M • '
    'EMA 10/20/30/40/50 • CPR • Momentum • Breakout + Retest • Swing + Long'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SAFE NUMBER
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


# ============================================================
# SAFE HTML
# ============================================================

def render_html(html):

    st.markdown(html, unsafe_allow_html=True)


# ============================================================
# INDICATOR CALCULATIONS
# ============================================================

def calculate_indicators(df):

    close = df["Close"]

    for period in [10, 20, 30, 40, 50]:
        df[f"EMA{period}"] = close.ewm(
            span=period,
            adjust=False
        ).mean()

    delta = close.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)

    df["RSI14"] = 100 - (100 / (1 + rs))

    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()

    df["MACD"] = ema12 - ema26
    df["MACD_SIGNAL"] = df["MACD"].ewm(
        span=9,
        adjust=False
    ).mean()

    df["VOLUME_AVG20"] = df["Volume"].rolling(20).mean()

    df["VOLUME_RATIO"] = (
        df["Volume"] /
        df["VOLUME_AVG20"].replace(0, np.nan)
    )

    df["52W_HIGH"] = close.rolling(252).max()

    df["52W_LOW"] = close.rolling(252).min()

    # CPR
    df["PP"] = (
        df["High"].shift(1)
        + df["Low"].shift(1)
        + df["Close"].shift(1)
    ) / 3

    df["BC"] = (
        df["High"].shift(1)
        + df["Low"].shift(1)
    ) / 2

    df["TC"] = (
        2 * df["PP"] - df["BC"]
    )

    df["CPR_LOW"] = df[["BC", "TC"]].min(axis=1)
    df["CPR_HIGH"] = df[["BC", "TC"]].max(axis=1)

    return df


# ============================================================
# SIGNAL ENGINE
# ============================================================

def signal_engine(df):

    last = df.iloc[-1]

    close = safe_num(last["Close"])

    ema10 = safe_num(last["EMA10"])
    ema20 = safe_num(last["EMA20"])
    ema30 = safe_num(last["EMA30"])
    ema40 = safe_num(last["EMA40"])
    ema50 = safe_num(last["EMA50"])

    rsi = safe_num(last["RSI14"], 50)

    macd = safe_num(last["MACD"])
    macd_signal = safe_num(last["MACD_SIGNAL"])

    volume_ratio = safe_num(
        last["VOLUME_RATIO"],
        0
    )

    ema_bull = (
        close > ema10 > ema20 >
        ema30 > ema40 > ema50
    )

    ema_bear = (
        close < ema10 < ema20 <
        ema30 < ema40 < ema50
    )

    score = 50

    if ema_bull:
        score += 25

    elif ema_bear:
        score -= 25

    if rsi >= 60:
        score += 10

    elif rsi < 40:
        score -= 10

    if macd > macd_signal:
        score += 10

    else:
        score -= 10

    if volume_ratio >= 2:
        score += 5

    score = max(0, min(100, score))

    if score >= 70:
        regime = "🐂 BULL"
        signal = "🚦 BUY"

    elif score >= 50:
        regime = "🟡 NEUTRAL"
        signal = "🟡 HOLD"

    else:
        regime = "🐻 BEAR"
        signal = "🚦 SELL / EXIT"

    return {
        "score": score,
        "regime": regime,
        "signal": signal,
        "ema_bull": ema_bull,
        "ema_bear": ema_bear
    }


# ============================================================
# COMPACT KEY INDICATORS
# ============================================================

def key_indicator_box(title, value, css=""):

    return f"""
    <div class="key-box {css}">
        <div class="key-title">{title}</div>
        <div class="key-value">{value}</div>
    </div>
    """


def render_key_indicators(df):

    last = df.iloc[-1]

    ema10 = safe_num(last["EMA10"])
    ema20 = safe_num(last["EMA20"])
    ema30 = safe_num(last["EMA30"])
    ema40 = safe_num(last["EMA40"])
    ema50 = safe_num(last["EMA50"])

    rsi = safe_num(last["RSI14"], 50)

    macd = safe_num(last["MACD"])
    macd_signal = safe_num(last["MACD_SIGNAL"])

    volume = safe_num(
        last["VOLUME_RATIO"],
        0
    )

    high52 = safe_num(
        last["52W_HIGH"]
    )

    cpr_low = safe_num(
        last["CPR_LOW"]
    )

    cpr_high = safe_num(
        last["CPR_HIGH"]
    )

    ema_css = "key-positive"

    if ema10 < ema20:
        ema_css = "key-negative"

    macd_text = (
        "🟢 BULL"
        if macd > macd_signal
        else "🔴 BEAR"
    )

    rsi_css = (
        "key-positive"
        if rsi >= 50
        else "key-negative"
    )

    macd_css = (
        "key-positive"
        if macd > macd_signal
        else "key-negative"
    )

    volume_css = (
        "key-positive"
        if volume >= 1.5
        else "key-warning"
    )

    html = f"""
    <div class="key-grid">

        {key_indicator_box(
            "EMA 10",
            f"₹{ema10:,.2f}",
            ema_css
        )}

        {key_indicator_box(
            "EMA 20",
            f"₹{ema20:,.2f}",
            ema_css
        )}

        {key_indicator_box(
            "EMA 30",
            f"₹{ema30:,.2f}",
            ema_css
        )}

        {key_indicator_box(
            "EMA 40",
            f"₹{ema40:,.2f}",
            ema_css
        )}

        {key_indicator_box(
            "EMA 50",
            f"₹{ema50:,.2f}",
            ema_css
        )}

        {key_indicator_box(
            "CPR",
            f"₹{cpr_low:,.0f} – ₹{cpr_high:,.0f}",
            "key-warning"
        )}

        {key_indicator_box(
            "RSI 14",
            f"{rsi:.1f}",
            rsi_css
        )}

        {key_indicator_box(
            "MACD",
            macd_text,
            macd_css
        )}

        {key_indicator_box(
            "SUPERTREND",
            "🟢 BULL" if not ema_css == "key-negative"
            else "🔴 BEAR",
            "key-positive"
            if ema_css != "key-negative"
            else "key-negative"
        )}

        {key_indicator_box(
            "VOLUME",
            f"{volume:.2f}x",
            volume_css
        )}

        {key_indicator_box(
            "52W HIGH",
            f"₹{high52:,.0f}",
            ""
        )}

        {key_indicator_box(
            "BREAKOUT",
            "🟢 CONFIRMED"
            if volume >= 2
            else "🟡 WATCH",
            "key-positive"
            if volume >= 2
            else "key-warning"
        )}

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
        <div class="target-value">₹{price:,.2f}</div>
        <div class="target-upside">{upside:+.1f}%</div>
    </div>
    """


def render_targets(cmp):

    swing1 = cmp * 1.04
    swing2 = cmp * 1.09
    swing3 = cmp * 1.16

    long1 = cmp * 1.15
    long2 = cmp * 1.25
    long3 = cmp * 1.40

    swing_html = f"""
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
    """

    long_html = f"""
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
    """

    st.markdown("### 🎯 SWING TARGETS")
    render_html(swing_html)

    st.markdown("### 🏆 LONG-TERM TARGETS")
    render_html(long_html)


# ============================================================
# ENTRY / RISK
# ============================================================

def render_entry_risk(df, signal):

    last = df.iloc[-1]

    cmp = safe_num(last["Close"])

    ema50 = safe_num(last["EMA50"])

    support = safe_num(
        df["Low"].rolling(20).min().iloc[-1],
        cmp * .95
    )

    resistance = safe_num(
        df["High"].rolling(20).max().iloc[-1],
        cmp * 1.05
    )

    stop_loss = support * .97

    # IMPORTANT:
    # BEAR / SELL માં BUY ZONE બતાવશો નહીં.

    if signal["regime"] == "🐻 BEAR":

        html = f"""
        <div class="box-grid">

            <div class="price-box red-box">
                <div class="price-title">STATUS</div>
                <div class="price-value">🚫 NO BUY</div>
            </div>

            <div class="price-box blue-box">
                <div class="price-title">SUPPORT</div>
                <div class="price-value">₹{support:,.2f}</div>
            </div>

            <div class="price-box blue-box">
                <div class="price-title">RESISTANCE</div>
                <div class="price-value">₹{resistance:,.2f}</div>
            </div>

            <div class="price-box red-box">
                <div class="price-title">STOP LOSS</div>
                <div class="price-value">₹{stop_loss:,.2f}</div>
            </div>

        </div>
        """

        render_html(html)

    else:

        buy_low = min(ema50, cmp * .97)
        buy_high = max(ema50, cmp * 1.01)

        breakout = resistance * 1.003

        html = f"""
        <div class="box-grid">

            <div class="price-box green-box">
                <div class="price-title">🟢 BUY ZONE</div>
                <div class="price-value">
                    ₹{buy_low:,.0f} – ₹{buy_high:,.0f}
                </div>
            </div>

            <div class="price-box green-box">
                <div class="price-title">🟢 BUY ON DIP</div>
                <div class="price-value">
                    ₹{support:,.0f} – ₹{ema50:,.0f}
                </div>
            </div>

            <div class="price-box blue-box">
                <div class="price-title">🚀 BREAKOUT</div>
                <div class="price-value">
                    ₹{breakout:,.2f}
                </div>
            </div>

            <div class="price-box red-box">
                <div class="price-title">STOP LOSS</div>
                <div class="price-value">
                    ₹{stop_loss:,.2f}
                </div>
            </div>

        </div>
        """

        render_html(html)


# ============================================================
# STOCK ANALYSIS
# ============================================================

def analyze_stock(symbol):

    ticker = symbol.upper().strip()

    if not ticker.endswith(".NS"):
        ticker = ticker + ".NS"

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

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        required = [
            "Open",
            "High",
            "Low",
            "Close",
            "Volume"
        ]

        df = df.dropna(
            subset=required
        )

        if len(df) < 100:
            return None

        df = calculate_indicators(df)

        signal = signal_engine(df)

        return df, signal

    except Exception:
        return None


# ============================================================
# INPUT
# ============================================================

st.markdown("### ➕ ADD STOCK")

stock_input = st.text_input(
    "NSE Symbol",
    placeholder="Example: BSE / RATNAVEER / AIIL"
)

if "stocks" not in st.session_state:
    st.session_state.stocks = []

if stock_input:

    symbol = stock_input.upper().replace(
        ".NS",
        ""
    ).strip()

    if symbol and symbol not in st.session_state.stocks:

        if len(st.session_state.stocks) < 15:

            st.session_state.stocks.append(symbol)


# ============================================================
# WATCHLIST
# ============================================================

st.markdown(
    f"### 📋 MY STOCKS — "
    f"{len(st.session_state.stocks)}/15"
)

if st.session_state.stocks:

    st.write(
        " • ".join(st.session_state.stocks)
    )


# ============================================================
# ANALYZE ALL
# ============================================================

if st.button(
    "🔍 ANALYZE ALL",
    use_container_width=True
):

    for symbol in st.session_state.stocks:

        result = analyze_stock(symbol)

        if result is None:

            st.error(
                f"⚠️ {symbol}: Market data unavailable"
            )

            continue

        df, signal = result

        last = df.iloc[-1]

        cmp = safe_num(last["Close"])

        st.markdown("---")

        # ----------------------------------------------------
        # STOCK HEADER
        # ----------------------------------------------------

        st.markdown(
            f"## 🏢 {symbol}"
        )

        st.caption(
            f"{symbol}.NS • NSE • "
            f"Analysis: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        )

        st.markdown(
            f'<div class="signal">{signal["regime"]} '
            f' {signal["signal"]}</div>',
            unsafe_allow_html=True
        )

        # ----------------------------------------------------
        # SUMMARY
        # ----------------------------------------------------

        st.markdown("### 🚦 SMART SIGNAL DASHBOARD")

        summary_html = f"""
        <div class="box-grid">

            <div class="metric-box">
                <div class="metric-title">CMP</div>
                <div class="metric-value">
                    ₹{cmp:,.2f}
                </div>
            </div>

            <div class="metric-box">
                <div class="metric-title">EMS</div>
                <div class="metric-value">
                    {signal["score"]}/100
                </div>
            </div>

            <div class="metric-box">
                <div class="metric-title">TECH</div>
                <div class="metric-value">
                    {signal["score"]}/100
                </div>
            </div>

            <div class="metric-box">
                <div class="metric-title">RSI</div>
                <div class="metric-value">
                    {safe_num(last["RSI14"],50):.1f}
                </div>
            </div>

            <div class="metric-box">
                <div class="metric-title">VOLUME</div>
                <div class="metric-value">
                    {safe_num(last["VOLUME_RATIO"],0):.2f}x
                </div>
            </div>

            <div class="metric-box">
                <div class="metric-title">REGIME</div>
                <div class="metric-value">
                    {signal["regime"]}
                </div>
            </div>

        </div>
        """

        render_html(summary_html)

        # ----------------------------------------------------
        # KEY INDICATORS
        # ----------------------------------------------------

        st.markdown("### 📊 KEY INDICATORS")

        render_key_indicators(df)

        # ----------------------------------------------------
        # PRICE LEVELS
        # ----------------------------------------------------

        st.markdown("### 🎯 PRICE LEVELS")

        support = safe_num(
            df["Low"].rolling(20).min().iloc[-1],
            cmp * .95
        )

        resistance = safe_num(
            df["High"].rolling(20).max().iloc[-1],
            cmp * 1.05
        )

        high52 = safe_num(
            last["52W_HIGH"],
            resistance
        )

        levels_html = f"""
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

        </div>
        """

        render_html(levels_html)

        # ----------------------------------------------------
        # ENTRY / RISK
        # ----------------------------------------------------

        st.markdown("### 🛡️ ENTRY + RISK")

        render_entry_risk(
            df,
            signal
        )

        # ----------------------------------------------------
        # TARGETS
        # ----------------------------------------------------

        render_targets(cmp)

        # ----------------------------------------------------
        # CHART
        # ----------------------------------------------------

        st.markdown("### 📈 PRICE + EMA CHART")

        chart_df = df[
            [
                "Close",
                "EMA10",
                "EMA20",
                "EMA30",
                "EMA40",
                "EMA50"
            ]
        ].tail(180)

        st.line_chart(
            chart_df,
            use_container_width=True
        )

        # ----------------------------------------------------
        # WHY SIGNAL
        # ----------------------------------------------------

        st.markdown("### 🧠 WHY THIS SIGNAL?")

        if signal["ema_bull"]:

            st.success(
                "✅ EMA 10 > 20 > 30 > 40 > 50"
            )

        elif signal["ema_bear"]:

            st.error(
                "🔴 EMA 10 < 20 < 30 < 40 < 50"
            )

        else:

            st.warning(
                "🟡 EMA structure mixed"
            )

        if safe_num(last["RSI14"],50) >= 50:
            st.write("🟢 RSI positive")
        else:
            st.write("🔴 RSI weak")

        if safe_num(last["MACD"]) > safe_num(last["MACD_SIGNAL"]):
            st.write("🟢 MACD bullish")
        else:
            st.write("🔴 MACD bearish")

        st.caption(
            "🐂 RAJESH STOCK ANALYZER PRO V2.4 • "
            "NSE Manual Analyzer • Research & decision-support tool • "
            "Not financial advice."
        )
