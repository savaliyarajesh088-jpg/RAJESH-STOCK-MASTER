# ============================================================
# 🐂 RAJESH STOCK ANALYZER PRO V2.5
# NSE • Manual 1–15 Stocks
# EMS V3 • D/W/M
# EMA 10/20/50/100/200 • CPR
# RSI • MACD • Supertrend • Volume
# Breakout + Retest • Swing + Long
# MOBILE FIRST • NAMEERROR SAFE
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
    page_title="RAJESH STOCK ANALYZER PRO V2.5",
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
    padding-left:.6rem;
    padding-right:.6rem;
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

/* COMMON GRID */

.box-grid {
    display:grid;
    grid-template-columns:repeat(6,minmax(0,1fr));
    gap:5px;
    margin-bottom:8px;
}

/* BOXES */

.metric-box,
.key-box,
.price-box,
.target-box {
    background:#101010;
    border:1px solid #303030;
    border-radius:7px;
    padding:6px 4px;
    text-align:center;
    overflow:hidden;
}

.metric-title,
.key-title,
.price-title,
.target-title {
    font-size:9px;
    font-weight:700;
    opacity:.72;
    white-space:nowrap;
}

.metric-value,
.key-value,
.price-value,
.target-value {
    font-size:13px;
    font-weight:900;
    margin-top:2px;
    white-space:nowrap;
}

.key-grid {
    display:grid;
    grid-template-columns:repeat(6,minmax(0,1fr));
    gap:4px;
}

.key-box {
    min-height:54px;
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
    min-height:53px;
    padding:5px 3px;
}

.target-value {
    font-size:12px;
}

.target-upside {
    font-size:9px;
    opacity:.75;
    margin-top:1px;
}

/* BORDER SIGNAL COLORS */

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
    font-size:19px;
    font-weight:900;
    padding:3px 0;
}

/* MOBILE */

@media(max-width:900px){

    .box-grid {
        grid-template-columns:repeat(3,1fr);
    }

    .key-grid {
        grid-template-columns:repeat(3,1fr);
    }
}

@media(max-width:500px){

    .app-title {
        font-size:18px;
    }

    .app-subtitle {
        font-size:10px;
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
        padding:5px 2px;
    }

    .key-title {
        font-size:8px;
    }

    .key-value {
        font-size:10px;
    }

    .metric-value {
        font-size:12px;
    }

    .price-value {
        font-size:12px;
    }

    .target-value {
        font-size:11px;
    }
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="app-title">🐂 RAJESH STOCK ANALYZER PRO V2.5</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="app-subtitle">'
    'NSE • Manual 1–15 Stocks • EMS V3 • D/W/M • '
    'EMA 10/20/50/100/200 • CPR • RSI • MACD • '
    'Supertrend • Momentum • Breakout + Retest • Swing + Long'
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
# HTML
# ============================================================

def render_html(html):
    st.markdown(html, unsafe_allow_html=True)


# ============================================================
# INDICATORS
# ============================================================

def calculate_indicators(df):

    df = df.copy()

    close = pd.to_numeric(
        df["Close"],
        errors="coerce"
    )

    high = pd.to_numeric(
        df["High"],
        errors="coerce"
    )

    low = pd.to_numeric(
        df["Low"],
        errors="coerce"
    )

    volume = pd.to_numeric(
        df["Volume"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # EMA MASTER
    # --------------------------------------------------------

    for period in [10,20,50,100,200]:

        df[f"EMA{period}"] = close.ewm(
            span=period,
            adjust=False,
            min_periods=1
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

    rs = avg_gain / avg_loss.replace(
        0,
        np.nan
    )

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
        df["MACD"] -
        df["MACD_SIGNAL"]
    )

    # --------------------------------------------------------
    # VOLUME
    # --------------------------------------------------------

    df["VOLUME_AVG20"] = volume.rolling(
        20,
        min_periods=1
    ).mean()

    df["VOLUME_RATIO"] = (
        volume /
        df["VOLUME_AVG20"].replace(
            0,
            np.nan
        )
    )

    # --------------------------------------------------------
    # 52 WEEK
    # --------------------------------------------------------

    df["52W_HIGH"] = close.rolling(
        252,
        min_periods=1
    ).max()

    df["52W_LOW"] = close.rolling(
        252,
        min_periods=1
    ).min()

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

    # --------------------------------------------------------
    # SIMPLE SUPERTREND
    # --------------------------------------------------------

    prev_close_series = close.shift(1)

    tr1 = high - low

    tr2 = (
        high -
        prev_close_series
    ).abs()

    tr3 = (
        low -
        prev_close_series
    ).abs()

    tr = pd.concat(
        [tr1,tr2,tr3],
        axis=1
    ).max(axis=1)

    atr = tr.rolling(
        10,
        min_periods=1
    ).mean()

    hl2 = (high + low) / 2

    upper = hl2 + (3 * atr)
    lower = hl2 - (3 * atr)

    df["SUPERTREND"] = lower

    df["ST_BULL"] = close >= lower

    # --------------------------------------------------------
    # SUPPORT / RESISTANCE
    # --------------------------------------------------------

    df["SUPPORT20"] = low.rolling(
        20,
        min_periods=1
    ).min()

    df["RESISTANCE20"] = high.rolling(
        20,
        min_periods=1
    ).max()

    return df


# ============================================================
# SIGNAL ENGINE
# ============================================================

def signal_engine(df):

    last = df.iloc[-1]

    close = safe_num(
        last.get("Close")
    )

    ema10 = safe_num(
        last.get("EMA10"),
        close
    )

    ema20 = safe_num(
        last.get("EMA20"),
        close
    )

    ema50 = safe_num(
        last.get("EMA50"),
        close
    )

    ema100 = safe_num(
        last.get("EMA100"),
        close
    )

    ema200 = safe_num(
        last.get("EMA200"),
        close
    )

    rsi = safe_num(
        last.get("RSI14"),
        50
    )

    macd = safe_num(
        last.get("MACD")
    )

    macd_signal = safe_num(
        last.get("MACD_SIGNAL")
    )

    volume_ratio = safe_num(
        last.get("VOLUME_RATIO")
    )

    # --------------------------------------------------------
    # EMA MASTER STRUCTURE
    # --------------------------------------------------------

    ema_bull = (
        close > ema10 >
        ema20 > ema50 >
        ema100 > ema200
    )

    ema_bear = (
        close < ema10 <
        ema20 < ema50 <
        ema100 < ema200
    )

    # --------------------------------------------------------
    # SCORE
    # --------------------------------------------------------

    score = 50

    if ema_bull:
        score += 25

    elif ema_bear:
        score -= 25

    # RSI

    if rsi >= 60:
        score += 10

    elif rsi < 40:
        score -= 10

    # MACD

    if macd > macd_signal:
        score += 10

    else:
        score -= 10

    # Volume

    if volume_ratio >= 2:
        score += 5

    score = int(
        max(
            0,
            min(
                100,
                score
            )
        )
    )

    # --------------------------------------------------------
    # REGIME
    # --------------------------------------------------------

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
# KEY BOX
# ============================================================

def key_indicator_box(
    title,
    value,
    css=""
):

    return f"""
    <div class="key-box {css}">
        <div class="key-title">
            {title}
        </div>

        <div class="key-value">
            {value}
        </div>
    </div>
    """


# ============================================================
# KEY INDICATORS
# ============================================================

def render_key_indicators(df):

    last = df.iloc[-1]

    ema10 = safe_num(
        last.get("EMA10")
    )

    ema20 = safe_num(
        last.get("EMA20")
    )

    ema50 = safe_num(
        last.get("EMA50")
    )

    ema100 = safe_num(
        last.get("EMA100")
    )

    ema200 = safe_num(
        last.get("EMA200")
    )

    cpr_low = safe_num(
        last.get("CPR_LOW")
    )

    cpr_high = safe_num(
        last.get("CPR_HIGH")
    )

    rsi = safe_num(
        last.get("RSI14"),
        50
    )

    macd = safe_num(
        last.get("MACD")
    )

    macd_signal = safe_num(
        last.get("MACD_SIGNAL")
    )

    volume = safe_num(
        last.get("VOLUME_RATIO")
    )

    high52 = safe_num(
        last.get("52W_HIGH")
    )

    low52 = safe_num(
        last.get("52W_LOW")
    )

    ema_bull = (
        ema10 > ema20 >
        ema50 > ema100 >
        ema200
    )

    ema_bear = (
        ema10 < ema20 <
        ema50 < ema100 <
        ema200
    )

    ema_css = (
        "key-positive"
        if ema_bull
        else "key-negative"
        if ema_bear
        else "key-warning"
    )

    macd_bull = (
        macd > macd_signal
    )

    macd_css = (
        "key-positive"
        if macd_bull
        else "key-negative"
    )

    rsi_css = (
        "key-positive"
        if rsi >= 50
        else "key-negative"
    )

    volume_css = (
        "key-positive"
        if volume >= 2
        else "key-warning"
    )

    super_bull = safe_num(
        last.get("Close")
    ) >= safe_num(
        last.get("SUPERTREND")
    )

    super_css = (
        "key-positive"
        if super_bull
        else "key-negative"
    )

    breakout = (
        volume >= 2
        and safe_num(last.get("Close"))
        >= safe_num(last.get("RESISTANCE20"))
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
            "EMA 50",
            f"₹{ema50:,.2f}",
            ema_css
        )}

        {key_indicator_box(
            "EMA 100",
            f"₹{ema100:,.2f}",
            ema_css
        )}

        {key_indicator_box(
            "EMA 200",
            f"₹{ema200:,.2f}",
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
            "🟢 BULL"
            if macd_bull
            else "🔴 BEAR",
            macd_css
        )}

        {key_indicator_box(
            "SUPERTREND",
            "🟢 BULL"
            if super_bull
            else "🔴 BEAR",
            super_css
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
            "52W LOW",
            f"₹{low52:,.0f}",
            ""
        )}

        {key_indicator_box(
            "BREAKOUT",
            "🟢 CONFIRMED"
            if breakout
            else "🟡 WATCH",
            "key-positive"
            if breakout
            else "key-warning"
        )}

    </div>
    """

    render_html(html)


# ============================================================
# TARGET BOX
# ============================================================

def target_box(
    title,
    price,
    upside
):

    return f"""
    <div class="target-box">

        <div class="target-title">
            {title}
        </div>

        <div class="target-value">
            ₹{price:,.2f}
        </div>

        <div class="target-upside">
            {upside:+.1f}%
        </div>

    </div>
    """


# ============================================================
# TARGETS
# ============================================================

def render_targets(cmp):

    swing1 = cmp * 1.04
    swing2 = cmp * 1.09
    swing3 = cmp * 1.16

    long1 = cmp * 1.15
    long2 = cmp * 1.25
    long3 = cmp * 1.40

    st.markdown("### 🎯 SWING TARGETS")

    render_html(
        f"""
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
    )

    st.markdown("### 🏆 LONG-TERM TARGETS")

    render_html(
        f"""
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
    )


# ============================================================
# ENTRY / RISK
# ============================================================

def render_entry_risk(
    df,
    signal
):

    last = df.iloc[-1]

    cmp = safe_num(
        last.get("Close")
    )

    ema50 = safe_num(
        last.get("EMA50"),
        cmp
    )

    support = safe_num(
        last.get("SUPPORT20"),
        cmp * .95
    )

    resistance = safe_num(
        last.get("RESISTANCE20"),
        cmp * 1.05
    )

    stop_loss = support * .97

    # --------------------------------------------------------
    # BEAR = NO BUY
    # --------------------------------------------------------

    if signal["regime"] == "🐻 BEAR":

        render_html(
            f"""
            <div class="box-grid">

                <div class="price-box red-box">
                    <div class="price-title">
                        STATUS
                    </div>

                    <div class="price-value">
                        🚫 NO BUY
                    </div>
                </div>

                <div class="price-box blue-box">
                    <div class="price-title">
                        SUPPORT
                    </div>

                    <div class="price-value">
                        ₹{support:,.2f}
                    </div>
                </div>

                <div class="price-box blue-box">
                    <div class="price-title">
                        RESISTANCE
                    </div>

                    <div class="price-value">
                        ₹{resistance:,.2f}
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
        )

        return

    # --------------------------------------------------------
    # BUY / HOLD
    # --------------------------------------------------------

    buy_low = min(
        ema50,
        cmp * .97
    )

    buy_high = max(
        ema50,
        cmp * 1.01
    )

    dip_low = support
    dip_high = ema50

    breakout = resistance * 1.003

    render_html(
        f"""
        <div class="box-grid">

            <div class="price-box green-box">
                <div class="price-title">
                    🟢 BUY ZONE
                </div>

                <div class="price-value">
                    ₹{buy_low:,.0f}
                    – ₹{buy_high:,.0f}
                </div>
            </div>

            <div class="price-box green-box">
                <div class="price-title">
                    🟢 BUY ON DIP
                </div>

                <div class="price-value">
                    ₹{dip_low:,.0f}
                    – ₹{dip_high:,.0f}
                </div>
            </div>

            <div class="price-box blue-box">
                <div class="price-title">
                    🚀 BREAKOUT
                </div>

                <div class="price-value">
                    ₹{breakout:,.2f}
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
    )


# ============================================================
# DOWNLOAD DATA
# ============================================================

def download_stock(symbol):

    ticker = symbol.upper().strip()

    if ticker.endswith(".NS"):
        ticker = ticker[:-3]

    ticker_ns = ticker + ".NS"

    try:

        df = yf.download(
            ticker_ns,
            period="5y",
            interval="1d",
            auto_adjust=False,
            progress=False,
            threads=False
        )

        if df is None or df.empty:
            return None

        # MultiIndex SAFE

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

        for column in required:

            if column not in df.columns:
                return None

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

        df = df.dropna(
            subset=required
        )

        if df.empty:
            return None

        return df

    except Exception:

        return None


# ============================================================
# ANALYZE
# ============================================================

def analyze_stock(symbol):

    df = download_stock(symbol)

    if df is None:
        return None

    try:

        df = calculate_indicators(df)

        signal = signal_engine(df)

        return df, signal

    except Exception:

        return None


# ============================================================
# SESSION STATE
# ============================================================

if "stocks" not in st.session_state:
    st.session_state.stocks = []


# ============================================================
# ADD STOCK
# ============================================================

st.markdown("### ➕ ADD STOCK")

stock_input = st.text_input(
    "NSE Symbol",
    placeholder="Example: BSE / RATNAVEER / AIIL"
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


# ============================================================
# CLEAR BUTTON
# ============================================================

if st.session_state.stocks:

    if st.button(
        "🗑️ CLEAR ALL STOCKS",
        use_container_width=True
    ):

        st.session_state.stocks = []

        st.rerun()


# ============================================================
# ANALYZE ALL
# ============================================================

if st.button(
    "🔍 ANALYZE ALL",
    use_container_width=True
):

    if not st.session_state.stocks:

        st.warning(
            "⚠️ પહેલા ઓછામાં ઓછો 1 NSE stock add કરો."
        )

    else:

        for symbol in st.session_state.stocks:

            result = analyze_stock(symbol)

            if result is None:

                st.error(
                    f"⚠️ {symbol}: Market data unavailable"
                )

                continue

            df, signal = result

            last = df.iloc[-1]

            cmp = safe_num(
                last.get("Close")
            )

            st.markdown("---")

            # ------------------------------------------------
            # HEADER
            # ------------------------------------------------

            st.markdown(
                f"## 🏢 {symbol}"
            )

            st.caption(
                f"{symbol}.NS • NSE • "
                f"Analysis: "
                f"{datetime.now().strftime('%d/%m/%Y %H:%M')}"
            )

            st.markdown(
                f"""
                <div class="signal">
                    {signal["regime"]}
                    &nbsp;
                    {signal["signal"]}
                </div>
                """,
                unsafe_allow_html=True
            )

            # ------------------------------------------------
            # DASHBOARD
            # ------------------------------------------------

            st.markdown(
                "### 🚦 SMART SIGNAL DASHBOARD"
            )

            rsi_value = safe_num(
                last.get("RSI14"),
                50
            )

            volume_value = safe_num(
                last.get("VOLUME_RATIO")
            )

            summary_html = f"""
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
                        {signal["score"]}/100
                    </div>
                </div>

                <div class="metric-box">
                    <div class="metric-title">
                        TECH
                    </div>
                    <div class="metric-value">
                        {signal["score"]}/100
                    </div>
                </div>

                <div class="metric-box">
                    <div class="metric-title">
                        RSI
                    </div>
                    <div class="metric-value">
                        {rsi_value:.1f}
                    </div>
                </div>

                <div class="metric-box">
                    <div class="metric-title">
                        VOLUME
                    </div>
                    <div class="metric-value">
                        {volume_value:.2f}x
                    </div>
                </div>

                <div class="metric-box">
                    <div class="metric-title">
                        REGIME
                    </div>
                    <div class="metric-value">
                        {signal["regime"]}
                    </div>
                </div>

            </div>
            """

            render_html(
                summary_html
            )

            # ------------------------------------------------
            # KEY INDICATORS
            # ------------------------------------------------

            st.markdown(
                "### 📊 KEY INDICATORS"
            )

            render_key_indicators(
                df
            )

            # ------------------------------------------------
            # PRICE LEVELS
            # ------------------------------------------------

            st.markdown(
                "### 🎯 PRICE LEVELS"
            )

            support = safe_num(
                last.get("SUPPORT20"),
                cmp * .95
            )

            resistance = safe_num(
                last.get("RESISTANCE20"),
                cmp * 1.05
            )

            high52 = safe_num(
                last.get("52W_HIGH"),
                resistance
            )

            low52 = safe_num(
                last.get("52W_LOW"),
                support
            )

            levels_html = f"""
            <div class="box-grid">

                <div class="price-box blue-box">
                    <div class="price-title">
                        SUPPORT
                    </div>

                    <div class="price-value">
                        ₹{support:,.2f}
                    </div>
                </div>

                <div class="price-box blue-box">
                    <div class="price-title">
                        RESISTANCE
                    </div>

                    <div class="price-value">
                        ₹{resistance:,.2f}
                    </div>
                </div>

                <div class="price-box yellow-box">
                    <div class="price-title">
                        52W HIGH
                    </div>

                    <div class="price-value">
                        ₹{high52:,.2f}
                    </div>
                </div>

                <div class="price-box blue-box">
                    <div class="price-title">
                        52W LOW
                    </div>

                    <div class="price-value">
                        ₹{low52:,.2f}
                    </div>
                </div>

            </div>
            """

            render_html(
                levels_html
            )

            # ------------------------------------------------
            # ENTRY RISK
            # ------------------------------------------------

            st.markdown(
                "### 🛡️ ENTRY + RISK"
            )

            render_entry_risk(
                df,
                signal
            )

            # ------------------------------------------------
            # TARGETS
            # ------------------------------------------------

            render_targets(
                cmp
            )

            # ------------------------------------------------
            # CHART
            # ------------------------------------------------

            st.markdown(
                "### 📈 PRICE + EMA CHART"
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
            ].tail(180)

            chart_df = chart_df.apply(
                pd.to_numeric,
                errors="coerce"
            ).dropna(
                how="all"
            )

            st.line_chart(
                chart_df,
                use_container_width=True
            )

            # ------------------------------------------------
            # WHY SIGNAL
            # ------------------------------------------------

            st.markdown(
                "### 🧠 WHY THIS SIGNAL?"
            )

            if signal["ema_bull"]:

                st.success(
                    "✅ EMA 10 > 20 > 50 > 100 > 200"
                )

            elif signal["ema_bear"]:

                st.error(
                    "🔴 EMA 10 < 20 < 50 < 100 < 200"
                )

            else:

                st.warning(
                    "🟡 EMA structure mixed"
                )

            if rsi_value >= 50:

                st.write(
                    "🟢 RSI positive"
                )

            else:

                st.write(
                    "🔴 RSI weak"
                )

            macd_value = safe_num(
                last.get("MACD")
            )

            macd_signal_value = safe_num(
                last.get("MACD_SIGNAL")
            )

            if macd_value > macd_signal_value:

                st.write(
                    "🟢 MACD bullish"
                )

            else:

                st.write(
                    "🔴 MACD bearish"
                )

            if volume_value >= 2:

                st.write(
                    "🚀 Volume breakout confirmation"
                )

            else:

                st.write(
                    "🟡 Volume confirmation pending"
                )

            st.caption(
                "🐂 RAJESH STOCK ANALYZER PRO V2.5 • "
                "NSE Manual Analyzer • "
                "Research & decision-support tool • "
                "Not financial advice."
            )
