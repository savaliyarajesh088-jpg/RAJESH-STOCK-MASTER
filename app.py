import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

# ============================================================
# 🐂 RAJESH STOCK ANALYZER PRO
# NSE ONLY • 1–15 STOCKS
# EMS • EXIT MATRA • BULL/PIG/BEAR
# D/W/M • CPR • MOMENTUM • BREAKOUT
# CMP-BASED SWING + LONG-TERM TARGET ENGINE
# ============================================================

st.set_page_config(
    page_title="RAJESH STOCK ANALYZER PRO",
    page_icon="🐂",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# CSS — PROFESSIONAL FULL COLOUR / MOBILE FIRST
# ============================================================

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at top right,#172554 0%,#050505 35%),
        #050505;
    color:#fff;
}

.block-container {
    max-width:1450px;
    padding:0.7rem 0.8rem 4rem 0.8rem;
}

h1,h2,h3,h4,h5,p,label {
    color:#fff !important;
}

.hero {
    background:linear-gradient(135deg,#111827,#312e81,#1e3a8a);
    border:1px solid #6366f1;
    border-radius:24px;
    padding:20px;
    margin-bottom:16px;
    box-shadow:0 10px 35px rgba(0,0,0,.4);
}

.hero-title {
    font-size:30px;
    font-weight:950;
    margin-bottom:5px;
}

.hero-sub {
    opacity:.85;
    font-size:14px;
}

.dashboard-card {
    background:linear-gradient(145deg,#0f172a,#111827);
    border:1px solid #334155;
    border-radius:18px;
    padding:14px;
    text-align:center;
    min-height:88px;
}

.dashboard-value {
    font-size:24px;
    font-weight:950;
}

.dashboard-label {
    font-size:12px;
    opacity:.7;
}

.stock-card {
    background:linear-gradient(145deg,#0b1120,#111827);
    border:1px solid #334155;
    border-radius:22px;
    padding:17px;
    margin-top:10px;
    box-shadow:0 10px 35px rgba(0,0,0,.35);
}

.stock-head {
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:10px;
}

.stock-name {
    font-size:25px;
    font-weight:950;
}

.stock-meta {
    font-size:12px;
    opacity:.7;
}

.signal {
    border-radius:17px;
    padding:14px;
    text-align:center;
    font-size:23px;
    font-weight:950;
    color:white;
    margin:12px 0;
    border:1px solid rgba(255,255,255,.25);
    box-shadow:0 8px 22px rgba(0,0,0,.25);
}

.buy {
    background:linear-gradient(135deg,#166534,#22c55e);
}

.buydip {
    background:linear-gradient(135deg,#166534,#16a34a);
}

.breakout {
    background:linear-gradient(135deg,#047857,#10b981);
}

.hold {
    background:linear-gradient(135deg,#1d4ed8,#3b82f6);
}

.wait {
    background:linear-gradient(135deg,#a16207,#eab308);
    color:#111827 !important;
}

.reduce {
    background:linear-gradient(135deg,#c2410c,#f97316);
}

.exit {
    background:linear-gradient(135deg,#991b1b,#ef4444);
}

.early {
    background:linear-gradient(135deg,#92400e,#f59e0b);
}

.regime {
    display:inline-block;
    padding:7px 15px;
    border-radius:999px;
    font-size:15px;
    font-weight:950;
}

.bull {
    background:#14532d;
    color:#bbf7d0;
}

.pig {
    background:#7c2d12;
    color:#fed7aa;
}

.bear {
    background:#7f1d1d;
    color:#fecaca;
}

.zone-box,
.target-box,
.exit-box {
    border-radius:17px;
    padding:14px;
    margin:4px 0;
    min-height:105px;
}

.zone-box {
    background:linear-gradient(135deg,#172554,#1e3a8a);
    border:1px solid #3b82f6;
}

.target-box {
    background:linear-gradient(135deg,#052e16,#14532d);
    border:1px solid #22c55e;
}

.exit-box {
    background:linear-gradient(135deg,#450a0a,#7f1d1d);
    border:1px solid #ef4444;
}

.target-price {
    font-size:23px;
    font-weight:950;
}

.upside {
    font-size:14px;
    font-weight:800;
    opacity:.9;
}

.metric-title {
    font-size:12px;
    opacity:.7;
}

div[data-testid="stMetric"] {
    background:#111827;
    border:1px solid #263244;
    border-radius:14px;
    padding:8px;
}

.stButton button {
    border-radius:12px;
    font-weight:850;
}

@media(max-width:700px) {
    .hero-title {
        font-size:22px;
    }

    .stock-name {
        font-size:20px;
    }

    .signal {
        font-size:19px;
        padding:12px;
    }

    .target-price {
        font-size:19px;
    }

    .block-container {
        padding-left:.55rem;
        padding-right:.55rem;
    }
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

if "analysis_cache" not in st.session_state:
    st.session_state.analysis_cache = {}

if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = None


# ============================================================
# HELPERS
# ============================================================

def ticker_name(symbol):
    symbol = str(symbol).strip().upper()
    if symbol.endswith(".NS"):
        return symbol
    return symbol + ".NS"


def clean_symbol(symbol):
    symbol = str(symbol).strip().upper()
    return symbol.replace(".NS", "")


def safe_float(value, default=0.0):
    try:
        x = float(value)
        if np.isfinite(x):
            return x
    except Exception:
        pass
    return default


def pct_from_cmp(price, cmp):
    if cmp <= 0:
        return 0.0
    return ((price - cmp) / cmp) * 100


def fmt_price(x):
    return f"₹{safe_float(x):,.2f}"


def target_upside_html(price, cmp):
    upside = pct_from_cmp(price, cmp)
    return f"{fmt_price(price)} &nbsp; <span class='upside'>+{upside:.1f}%</span>"


# ============================================================
# INDICATORS
# ============================================================

def calculate_rsi(close, period=14):
    delta = close.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(
        alpha=1 / period,
        adjust=False
    ).mean()

    avg_loss = loss.ewm(
        alpha=1 / period,
        adjust=False
    ).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)

    return 100 - (100 / (1 + rs))


def calculate_atr(df, period=14):

    tr1 = df["High"] - df["Low"]

    tr2 = (
        df["High"] -
        df["Close"].shift()
    ).abs()

    tr3 = (
        df["Low"] -
        df["Close"].shift()
    ).abs()

    tr = pd.concat(
        [tr1, tr2, tr3],
        axis=1
    ).max(axis=1)

    return tr.ewm(
        alpha=1 / period,
        adjust=False
    ).mean()


def add_indicators(df):

    df = df.copy()

    close = df["Close"]

    for p in [10,20,50,100,200]:
        df[f"EMA{p}"] = close.ewm(
            span=p,
            adjust=False
        ).mean()

    df["RSI"] = calculate_rsi(close,14)

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

    df["ATR"] = calculate_atr(df,14)

    df["VOL_AVG20"] = df["Volume"].rolling(20).mean()

    df["VOL_RATIO"] = (
        df["Volume"] /
        df["VOL_AVG20"].replace(0,np.nan)
    )

    df["HIGH_52W"] = close.rolling(252).max()
    df["LOW_52W"] = close.rolling(252).min()

    return df


# ============================================================
# CPR
# ============================================================

def calculate_cpr(df):

    if len(df) < 2:
        return 0,0,0

    p = df.iloc[-2]

    pivot = (
        p["High"] +
        p["Low"] +
        p["Close"]
    ) / 3

    bc = (
        p["High"] +
        p["Low"]
    ) / 2

    tc = (
        2 * pivot
    ) - bc

    return (
        pivot,
        min(bc,tc),
        max(bc,tc)
    )


# ============================================================
# TIMEFRAME
# ============================================================

def timeframe_analysis(df):

    if df is None or len(df) < 30:
        return {
            "score":0,
            "trend":"UNKNOWN"
        }

    try:
        x = add_indicators(df)
        last = x.iloc[-1]

        close = safe_float(last["Close"])

        checks = [
            close > safe_float(last["EMA20"]),
            close > safe_float(last["EMA50"]),
            close > safe_float(last["EMA200"]),
            safe_float(last["RSI"]) >= 50,
            safe_float(last["MACD"]) >
            safe_float(last["MACD_SIGNAL"]),
        ]

        score = round(
            sum(checks) / len(checks) * 100
        )

        if score >= 75:
            trend = "BULLISH"
        elif score >= 55:
            trend = "POSITIVE"
        elif score >= 40:
            trend = "MIXED"
        else:
            trend = "BEARISH"

        return {
            "score":score,
            "trend":trend
        }

    except Exception:
        return {
            "score":0,
            "trend":"UNKNOWN"
        }


# ============================================================
# DATA DOWNLOAD
# ============================================================

@st.cache_data(
    ttl=300,
    show_spinner=False
)
def download_stock(symbol):

    ticker = ticker_name(symbol)

    try:

        df = yf.download(
            ticker,
            period="5y",
            interval="1d",
            auto_adjust=False,
            progress=False,
        )

        if df is None or df.empty:
            return None

        if isinstance(df.columns,pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        required = [
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
        ]

        missing = [
            c for c in required
            if c not in df.columns
        ]

        if missing:
            return None

        return df.dropna(
            subset=["Close"]
        )

    except Exception:
        return None


# ============================================================
# TARGET ENGINE
# ============================================================

def build_targets(
    cmp,
    atr,
    resistance,
    recent_high,
    high52,
    ema20,
    ema50
):

    # --------------------------------------------------------
    # All candidate levels
    # --------------------------------------------------------

    atr = max(atr, cmp * 0.01)

    resistance = max(resistance, cmp)
    recent_high = max(recent_high, cmp)
    high52 = max(high52, cmp)

    # ========================================================
    # SWING ENGINE
    # CMP + MARKET STRUCTURE
    # ========================================================

    swing_candidates = [
        resistance,
        recent_high,
        high52,
        cmp + atr * 1.25,
        cmp + atr * 2.25,
        cmp + atr * 3.50,
    ]

    above = sorted(
        set(
            round(x,2)
            for x in swing_candidates
            if x > cmp * 1.005
        )
    )

    # If resistance/recent high is too close,
    # create ATR based ladder above CMP.
    minimums = [
        cmp + atr * 1.0,
        cmp + atr * 2.0,
        cmp + atr * 3.25,
    ]

    swing_t1 = above[0] if len(above) >= 1 else minimums[0]

    higher = [
        x for x in above
        if x > swing_t1 * 1.03
    ]

    swing_t2 = (
        higher[0]
        if higher
        else max(
            swing_t1 + atr,
            minimums[1]
        )
    )

    higher2 = [
        x for x in above
        if x > swing_t2 * 1.03
    ]

    swing_t3 = (
        higher2[0]
        if higher2
        else max(
            swing_t2 + atr * 1.25,
            minimums[2]
        )
    )

    # Force ascending order.
    swing_t1 = max(
        swing_t1,
        cmp * 1.01
    )

    swing_t2 = max(
        swing_t2,
        swing_t1 * 1.04
    )

    swing_t3 = max(
        swing_t3,
        swing_t2 * 1.05
    )

    # ========================================================
    # LONG TERM ENGINE
    # 52W HIGH + ATR EXPANSION
    # ========================================================

    long_base = max(
        high52,
        recent_high,
        resistance,
        cmp
    )

    long_t1 = max(
        long_base + atr * 2,
        cmp * 1.12
    )

    long_t2 = max(
        long_base + atr * 4,
        long_t1 * 1.12
    )

    long_t3 = max(
        long_base + atr * 7,
        long_t2 * 1.15
    )

    return {
        "swing_t1":round(swing_t1,2),
        "swing_t2":round(swing_t2,2),
        "swing_t3":round(swing_t3,2),
        "long_t1":round(long_t1,2),
        "long_t2":round(long_t2,2),
        "long_t3":round(long_t3,2),
    }


# ============================================================
# ANALYSIS ENGINE
# ============================================================

def analyze(symbol):

    symbol = clean_symbol(symbol)

    daily = download_stock(symbol)

    if daily is None:
        return {
            "symbol":symbol,
            "error":"Yahoo Finance data unavailable"
        }

    if len(daily) < 220:
        return {
            "symbol":symbol,
            "error":"Insufficient market data"
        }

    try:

        d = add_indicators(daily)

        last = d.iloc[-1]

        cmp = safe_float(last["Close"])

        ema10 = safe_float(last["EMA10"])
        ema20 = safe_float(last["EMA20"])
        ema50 = safe_float(last["EMA50"])
        ema100 = safe_float(last["EMA100"])
        ema200 = safe_float(last["EMA200"])

        rsi = safe_float(last["RSI"])
        macd = safe_float(last["MACD"])
        macd_signal = safe_float(last["MACD_SIGNAL"])
        atr = safe_float(last["ATR"])
        vol_ratio = safe_float(last["VOL_RATIO"])

        high52 = safe_float(last["HIGH_52W"])
        low52 = safe_float(last["LOW_52W"])

        # ----------------------------------------------------
        # EMA
        # ----------------------------------------------------

        ema_alignment = (
            cmp >
            ema10 >
            ema20 >
            ema50 >
            ema100 >
            ema200
        )

        # ----------------------------------------------------
        # CPR
        # ----------------------------------------------------

        pivot,cpr_low,cpr_high = calculate_cpr(daily)

        # ----------------------------------------------------
        # MACD
        # ----------------------------------------------------

        macd_bull = macd > macd_signal

        # ----------------------------------------------------
        # Supertrend proxy
        # ----------------------------------------------------

        supertrend_bull = (
            cmp > ema20 and
            cmp > ema50
        )

        # ----------------------------------------------------
        # Breakout
        # ----------------------------------------------------

        previous_20_high = safe_float(
            d["High"]
            .rolling(20)
            .max()
            .iloc[-2]
        )

        price_breakout = (
            cmp > previous_20_high
        )

        volume_confirmed = (
            vol_ratio >= 2
        )

        breakout_confirmations = sum([
            price_breakout,
            ema_alignment,
            rsi >= 60,
            macd_bull,
            supertrend_bull,
            cmp > cpr_high,
            volume_confirmed,
        ])

        breakout_confirmed = (
            price_breakout and
            breakout_confirmations >= 6
        )

        # ----------------------------------------------------
        # Momentum
        # ----------------------------------------------------

        early_momentum = (
            cmp > ema20 and
            rsi >= 55 and
            macd_bull and
            vol_ratio >= 1.2
        )

        technical_checks = [
            cmp > ema10,
            cmp > ema20,
            cmp > ema50,
            cmp > ema200,
            rsi >= 50,
            macd_bull,
            supertrend_bull,
            vol_ratio >= 1.2,
        ]

        technical_score = round(
            sum(technical_checks) /
            len(technical_checks) *
            100
        )

        momentum_score = round(
            np.clip(
                ((rsi - 40) * 1.5) +
                min(vol_ratio,3) * 12,
                0,
                100
            )
        )

        # ----------------------------------------------------
        # Risk
        # ----------------------------------------------------

        volatility_pct = (
            atr / cmp * 100
            if cmp > 0
            else 100
        )

        if volatility_pct < 2.5:
            risk_meter = "LOW"
        elif volatility_pct < 4:
            risk_meter = "MODERATE"
        elif volatility_pct < 6:
            risk_meter = "HIGH"
        else:
            risk_meter = "EXTREME"

        risk_score = round(
            np.clip(
                100 - volatility_pct * 12,
                0,
                100
            )
        )

        # ----------------------------------------------------
        # D/W/M
        # ----------------------------------------------------

        weekly = daily.resample(
            "W-FRI"
        ).agg({
            "Open":"first",
            "High":"max",
            "Low":"min",
            "Close":"last",
            "Volume":"sum",
        }).dropna()

        monthly = daily.resample(
            "ME"
        ).agg({
            "Open":"first",
            "High":"max",
            "Low":"min",
            "Close":"last",
            "Volume":"sum",
        }).dropna()

        d_tf = timeframe_analysis(daily)
        w_tf = timeframe_analysis(weekly)
        m_tf = timeframe_analysis(monthly)

        dwm_score = round(
            (
                d_tf["score"] +
                w_tf["score"] +
                m_tf["score"]
            ) / 3
        )

        # ----------------------------------------------------
        # Recent swing high
        # ----------------------------------------------------

        recent_window = d.tail(60)

        recent_swing_high = safe_float(
            recent_window["High"].max()
        )

        # ----------------------------------------------------
        # Structure
        # ----------------------------------------------------

        support = max(
            ema20,
            cpr_low
        )

        resistance = max(
            previous_20_high,
            cpr_high
        )

        # ----------------------------------------------------
        # Zones
        # ----------------------------------------------------

        buy_zone_low = max(
            0,
            support - atr * .5
        )

        buy_zone_high = (
            support + atr * .5
        )

        dip_zone_low = max(
            0,
            ema50 - atr
        )

        dip_zone_high = (
            ema50 + atr * .25
        )

        breakout_entry = max(
            previous_20_high + atr*.10,
            cmp*1.01
        )

        # ----------------------------------------------------
        # Exit / SL
        # ----------------------------------------------------

        exit_price = max(
            ema50,
            support
        )

        stop_loss = max(
            0,
            support - atr * 1.5
        )

        # ----------------------------------------------------
        # TARGET ENGINE
        # ----------------------------------------------------

        targets = build_targets(
            cmp=cmp,
            atr=atr,
            resistance=resistance,
            recent_high=recent_swing_high,
            high52=high52,
            ema20=ema20,
            ema50=ema50,
        )

        # ----------------------------------------------------
        # EMS
        # ----------------------------------------------------

        ath_profit = (
            cmp >= high52 * .90
        )

        outperformance = (
            momentum_score >= 65
        )

        above_exit = (
            cmp > exit_price
        )

        trend_breakdown = not ema_alignment
        momentum_breakdown = momentum_score < 40
        support_breakdown = cmp < support

        relative_strength = technical_score >= 65

        risk_deterioration = risk_meter in [
            "HIGH",
            "EXTREME"
        ]

        reference_match = (
            d_tf["score"] >= 60 and
            w_tf["score"] >= 55
        )

        ems_checks = [
            ath_profit,
            outperformance,
            above_exit,
            not trend_breakdown,
            not momentum_breakdown,
            not support_breakdown,
            volume_confirmed,
            relative_strength,
            not risk_deterioration,
            reference_match,
        ]

        ems_score = round(
            sum(ems_checks) /
            len(ems_checks) *
            100
        )

        if ems_score >= 75:
            ems_decision = "ADD"
        elif ems_score >= 55:
            ems_decision = "HOLD"
        elif ems_score >= 40:
            ems_decision = "REDUCE"
        else:
            ems_decision = "EXIT"

        # ----------------------------------------------------
        # BULL / PIG / BEAR
        # ----------------------------------------------------

        bull_points = sum([
            ema_alignment,
            rsi >= 55,
            macd_bull,
            w_tf["score"] >= 60,
            m_tf["score"] >= 55,
            momentum_score >= 60,
        ])

        bear_points = sum([
            cmp < ema50,
            rsi < 45,
            not macd_bull,
            w_tf["score"] < 45,
            m_tf["score"] < 45,
            momentum_score < 35,
        ])

        if bull_points >= 4:
            regime = "BULL"
        elif bear_points >= 4:
            regime = "BEAR"
        else:
            regime = "PIG"

        # ----------------------------------------------------
        # FINAL SIGNAL
        # ----------------------------------------------------

        if breakout_confirmed:
            signal = "BREAKOUT CONFIRMED"
            signal_class = "breakout"

        elif ems_score < 35:
            signal = "SELL / EXIT"
            signal_class = "exit"

        elif early_momentum:
            signal = "BUY ON DIP"
            signal_class = "buydip"

        elif (
            technical_score >= 70 and
            ems_score >= 60
        ):
            signal = "BUY"
            signal_class = "buy"

        elif ems_score < 45:
            signal = "REDUCE"
            signal_class = "reduce"

        elif technical_score < 45:
            signal = "WAIT"
            signal_class = "wait"

        else:
            signal = "HOLD"
            signal_class = "hold"

        difference = (
            ((cmp-exit_price)/exit_price)*100
            if exit_price > 0
            else 0
        )

        return {
            "symbol":symbol,
            "ticker":ticker_name(symbol),
            "cmp":cmp,
            "date":daily.index[-1],

            "signal":signal,
            "signal_class":signal_class,
            "regime":regime,

            "technical_score":technical_score,
            "momentum_score":momentum_score,
            "risk_score":risk_score,
            "risk_meter":risk_meter,

            "ems_score":ems_score,
            "ems_decision":ems_decision,

            "rsi":rsi,
            "volume_ratio":vol_ratio,

            "ema_alignment":ema_alignment,
            "macd_bull":macd_bull,
            "supertrend_bull":supertrend_bull,

            "price_breakout":price_breakout,
            "breakout_confirmed":breakout_confirmed,
            "breakout_confirmations":breakout_confirmations,
            "early_momentum":early_momentum,

            "d_tf":d_tf,
            "w_tf":w_tf,
            "m_tf":m_tf,
            "dwm_score":dwm_score,

            "pivot":pivot,
            "cpr_low":cpr_low,
            "cpr_high":cpr_high,

            "support":support,
            "resistance":resistance,
            "recent_swing_high":recent_swing_high,

            "buy_zone_low":buy_zone_low,
            "buy_zone_high":buy_zone_high,
            "dip_zone_low":dip_zone_low,
            "dip_zone_high":dip_zone_high,
            "breakout_entry":breakout_entry,

            "exit_price":exit_price,
            "stop_loss":stop_loss,

            "swing_t1":targets["swing_t1"],
            "swing_t2":targets["swing_t2"],
            "swing_t3":targets["swing_t3"],

            "long_t1":targets["long_t1"],
            "long_t2":targets["long_t2"],
            "long_t3":targets["long_t3"],

            "high52":high52,
            "low52":low52,

            "ath_profit":ath_profit,
            "outperformance":outperformance,
            "above_exit":above_exit,
            "trend_breakdown":trend_breakdown,
            "momentum_breakdown":momentum_breakdown,
            "support_breakdown":support_breakdown,
            "volume_confirmed":volume_confirmed,
            "relative_strength":relative_strength,
            "risk_deterioration":risk_deterioration,
            "reference_match":reference_match,

            "difference":difference,
            "df":d,
        }

    except Exception as e:

        return {
            "symbol":symbol,
            "error":f"Analysis error: {str(e)[:180]}"
        }


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="hero">
    <div class="hero-title">🐂 RAJESH STOCK ANALYZER PRO</div>
    <div class="hero-sub">
        NSE • Manual Stock Analyzer • EMS • Exit Matra Zones •
        D/W/M • CPR • Momentum • Breakout • Swing + Long
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# MASTER SETTINGS
# ============================================================

with st.expander("⚙️ MASTER SETTINGS", expanded=True):

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        strategy = st.selectbox(
            "Strategy",
            [
                "SWING + LONG",
                "SWING",
                "LONG-TERM",
            ]
        )

    with c2:
        data_mode = st.selectbox(
            "Data Mode",
            [
                "AUTO",
                "EOD",
                "LIVE*",
            ]
        )

    with c3:
        st.metric(
            "WATCHLIST",
            f"{len(st.session_state.watchlist)}/15"
        )

    with c4:
        st.metric(
            "LAST ANALYSIS",
            st.session_state.last_refresh
            or "—"
        )

    st.caption(
        "Yahoo Finance latest available data is used. "
        "LIVE* is not an exchange-grade real-time feed."
    )


# ============================================================
# ADD STOCK
# ============================================================

st.subheader("➕ ADD STOCK")

add1,add2 = st.columns([4,1])

with add1:
    new_stock = st.text_input(
        "NSE Symbol",
        placeholder="BEL / BSE / AIIL / CEMINDIA",
        label_visibility="collapsed"
    )

with add2:
    add_clicked = st.button(
        "➕ ADD",
        use_container_width=True
    )


if add_clicked:

    stock = clean_symbol(new_stock)

    if not stock:
        st.warning("NSE stock symbol નાખો.")

    elif stock in st.session_state.watchlist:
        st.info(f"{stock} પહેલેથી watchlistમાં છે.")

    elif len(st.session_state.watchlist) >= 15:
        st.error("Maximum 15 stocks.")

    else:
        st.session_state.watchlist.append(stock)
        st.success(f"{stock} added.")
        st.rerun()


# ============================================================
# WATCHLIST
# ============================================================

if st.session_state.watchlist:

    st.subheader("📋 MY STOCKS")

    cols = st.columns(
        min(len(st.session_state.watchlist),5)
    )

    for i,stock in enumerate(
        list(st.session_state.watchlist)
    ):

        with cols[i % len(cols)]:

            st.markdown(
                f"**{stock}**"
            )

            if st.button(
                f"✖ Remove {stock}",
                key=f"remove_{stock}",
                use_container_width=True
            ):

                # IMPORTANT:
                # Remove only selected stock.
                st.session_state.watchlist.remove(stock)

                st.session_state.analysis_cache.pop(
                    stock,
                    None
                )

                st.rerun()


# ============================================================
# CONTROLS
# ============================================================

st.divider()

a1,a2,a3 = st.columns([2,1,1])

with a1:
    analyze_all = st.button(
        "🔍 ANALYZE ALL",
        type="primary",
        use_container_width=True
    )

with a2:
    refresh_all = st.button(
        "🔄 REFRESH DATA",
        use_container_width=True
    )

with a3:
    clear_cache = st.button(
        "🧹 CLEAR CACHE",
        use_container_width=True
    )


if clear_cache:

    st.session_state.analysis_cache = {}

    st.cache_data.clear()

    st.success(
        "Analysis cache cleared."
    )


if refresh_all:

    st.cache_data.clear()

    analyze_all = True


# ============================================================
# ANALYZE
# ============================================================

if analyze_all:

    total = len(
        st.session_state.watchlist
    )

    if total == 0:

        st.warning(
            "પહેલા stock add કરો."
        )

    else:

        progress = st.progress(0)

        for i,stock in enumerate(
            st.session_state.watchlist
        ):

            try:
                result = analyze(stock)
            except Exception as e:
                result = {
                    "symbol":stock,
                    "error":str(e)
                }

            # IMPORTANT:
            # One stock error never stops others.
            st.session_state.analysis_cache[
                stock
            ] = result

            progress.progress(
                int(
                    ((i+1)/total)*100
                )
            )

        st.session_state.last_refresh = (
            datetime.now().strftime(
                "%d/%m/%Y %H:%M"
            )
        )

        progress.empty()

        st.success(
            "Analysis completed."
        )


# ============================================================
# RESULTS — SAFE
# ============================================================

results = []
errors = []

for stock in st.session_state.watchlist:

    result = st.session_state.analysis_cache.get(
        stock
    )

    if not result:
        continue

    if result.get("error"):
        errors.append(result)
    else:
        results.append(result)


if errors:

    with st.expander(
        f"⚠️ DATA WARNINGS ({len(errors)})",
        expanded=False
    ):

        for item in errors:
            st.warning(
                f"⚠️ {item['symbol']}: "
                f"{item.get('error','Unknown error')}"
            )


if not results:

    st.info(
        "Stock add કરો અને **ANALYZE ALL** દબાવો."
    )

    st.stop()


# ============================================================
# SMART DASHBOARD
# ============================================================

st.divider()

st.subheader("🚦 SMART SIGNAL DASHBOARD")

signal_counts = {}

for r in results:

    signal_counts[r["signal"]] = (
        signal_counts.get(
            r["signal"],0
        ) + 1
    )

d1,d2,d3,d4,d5 = st.columns(5)

with d1:
    st.markdown(
        f"""
        <div class="dashboard-card">
        <div class="dashboard-value">
        {len(results)}
        </div>
        <div class="dashboard-label">
        ANALYZED
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with d2:
    buys = sum(
        1 for r in results
        if r["signal"] in [
            "BUY",
            "BUY ON DIP",
            "BREAKOUT CONFIRMED"
        ]
    )

    st.markdown(
        f"""
        <div class="dashboard-card">
        <div class="dashboard-value">
        {buys}
        </div>
        <div class="dashboard-label">
        POSITIVE
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with d3:
    exits = sum(
        1 for r in results
        if r["signal"] in [
            "REDUCE",
            "SELL / EXIT"
        ]
    )

    st.markdown(
        f"""
        <div class="dashboard-card">
        <div class="dashboard-value">
        {exits}
        </div>
        <div class="dashboard-label">
        RISK / EXIT
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with d4:
    avg_ems = round(
        np.mean([
            r["ems_score"]
            for r in results
        ])
    )

    st.markdown(
        f"""
        <div class="dashboard-card">
        <div class="dashboard-value">
        {avg_ems}/100
        </div>
        <div class="dashboard-label">
        AVG EMS
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with d5:
    avg_tech = round(
        np.mean([
            r["technical_score"]
            for r in results
        ])
    )

    st.markdown(
        f"""
        <div class="dashboard-card">
        <div class="dashboard-value">
        {avg_tech}/100
        </div>
        <div class="dashboard-label">
        AVG TECH
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# SUMMARY TABLE
# ============================================================

summary = []

for r in results:

    summary.append({
        "STOCK":r["symbol"],
        "SIGNAL":r["signal"],
        "ZONE":r["regime"],
        "CMP":round(r["cmp"],2),
        "EMS":r["ems_score"],
        "TECH":r["technical_score"],
        "MOM":r["momentum_score"],
        "D/W/M":r["dwm_score"],
        "RISK":r["risk_meter"],
    })

summary_df = pd.DataFrame(summary)

st.dataframe(
    summary_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# FILTER
# ============================================================

filter_options = [
    "ALL",
    "BUY",
    "BUY ON DIP",
    "BREAKOUT CONFIRMED",
    "HOLD",
    "WAIT",
    "REDUCE",
    "SELL / EXIT",
]

filter_signal = st.selectbox(
    "🔎 SIGNAL FILTER",
    filter_options
)

if filter_signal == "ALL":

    display_results = results

else:

    display_results = [
        r for r in results
        if r["signal"] == filter_signal
    ]


if not display_results:

    st.info(
        "આ filterમાં કોઈ stock નથી."
    )


# ============================================================
# STOCK DETAILS
# ============================================================

for r in display_results:

    regime_class = {
        "BULL":"bull",
        "PIG":"pig",
        "BEAR":"bear",
    }.get(r["regime"],"pig")

    regime_icon = {
        "BULL":"🐂",
        "PIG":"🐷",
        "BEAR":"🐻",
    }.get(r["regime"],"🐷")

    # --------------------------------------------------------
    # HEADER CARD
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="stock-card">
            <div class="stock-head">
                <div>
                    <div class="stock-name">
                    🏢 {r['symbol']}
                    </div>
                    <div class="stock-meta">
                    {r['ticker']} • NSE •
                    Latest: {r['date'].date()}
                    </div>
                </div>

                <div class="regime {regime_class}">
                    {regime_icon} {r['regime']}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # SIGNAL
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="signal {r['signal_class']}">
        🚦 {r['signal']}
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    c1,c2,c3,c4,c5 = st.columns(5)

    c1.metric(
        "CMP",
        fmt_price(r["cmp"])
    )

    c2.metric(
        "EMS",
        f"{r['ems_score']}/100"
    )

    c3.metric(
        "TECH",
        f"{r['technical_score']}/100"
    )

    c4.metric(
        "MOMENTUM",
        f"{r['momentum_score']}/100"
    )

    c5.metric(
        "RISK",
        r["risk_meter"]
    )

    # --------------------------------------------------------
    # EXIT MATRA STYLE
    # --------------------------------------------------------

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="zone-box">
            <b>ZONE</b>
            <h3>{regime_icon} {r['regime']}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="exit-box">
            <b>EXIT PRICE</b>
            <h3>{fmt_price(r['exit_price'])}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="exit-box">
            <b>STOP LOSS</b>
            <h3>{fmt_price(r['stop_loss'])}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            f"""
            <div class="target-box">
            <b>EMS DECISION</b>
            <h3>{r['ems_decision']}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    # --------------------------------------------------------
    # TABS
    # --------------------------------------------------------

    tabs = st.tabs([
        "🎯 TARGETS",
        "🧠 EMS",
        "📊 D/W/M",
        "🚀 BREAKOUT",
        "⚡ MOMENTUM",
        "📈 CHART",
    ])

    # ========================================================
    # TARGETS
    # ========================================================

    with tabs[0]:

        z1,z2,z3 = st.columns(3)

        with z1:
            st.markdown(
                f"""
                <div class="zone-box">
                <b>🟢 BUY ZONE</b>
                <h3>
                {fmt_price(r['buy_zone_low'])}
                –
                {fmt_price(r['buy_zone_high'])}
                </h3>
                </div>
                """,
                unsafe_allow_html=True
            )

        with z2:
            st.markdown(
                f"""
                <div class="zone-box">
                <b>🟢 BUY ON DIP</b>
                <h3>
                {fmt_price(r['dip_zone_low'])}
                –
                {fmt_price(r['dip_zone_high'])}
                </h3>
                </div>
                """,
                unsafe_allow_html=True
            )

        with z3:
            st.markdown(
                f"""
                <div class="zone-box">
                <b>🚀 BREAKOUT ENTRY</b>
                <h3>{fmt_price(r['breakout_entry'])}</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("### 🎯 SWING TARGETS")

        s1,s2,s3 = st.columns(3)

        for col,label,key in [
            (s1,"SWING T1","swing_t1"),
            (s2,"SWING T2","swing_t2"),
            (s3,"SWING T3","swing_t3"),
        ]:

            with col:

                price = r[key]
                upside = pct_from_cmp(
                    price,
                    r["cmp"]
                )

                st.markdown(
                    f"""
                    <div class="target-box">
                    <b>{label}</b>
                    <div class="target-price">
                    {fmt_price(price)}
                    </div>
                    <div class="upside">
                    +{upside:.1f}% from CMP
                    </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown("### 🏆 LONG-TERM TARGETS")

        l1,l2,l3 = st.columns(3)

        for col,label,key in [
            (l1,"LONG T1","long_t1"),
            (l2,"LONG T2","long_t2"),
            (l3,"LONG T3","long_t3"),
        ]:

            with col:

                price = r[key]
                upside = pct_from_cmp(
                    price,
                    r["cmp"]
                )

                st.markdown(
                    f"""
                    <div class="target-box">
                    <b>{label}</b>
                    <div class="target-price">
                    {fmt_price(price)}
                    </div>
                    <div class="upside">
                    +{upside:.1f}% from CMP
                    </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.info(
            f"Support {fmt_price(r['support'])} | "
            f"Resistance {fmt_price(r['resistance'])} | "
            f"Recent Swing High {fmt_price(r['recent_swing_high'])} | "
            f"52W High {fmt_price(r['high52'])} | "
            f"CPR {fmt_price(r['cpr_low'])}–{fmt_price(r['cpr_high'])} | "
            f"Pivot {fmt_price(r['pivot'])}"
        )

    # ========================================================
    # EMS
    # ========================================================

    with tabs[1]:

        st.markdown(
            f"""
            <div class="signal hold">
            🧠 EMS {r['ems_score']}/100
            • {r['ems_decision']}
            </div>
            """,
            unsafe_allow_html=True
        )

        ems_data = pd.DataFrame({
            "EMS MODULE":[
                "ATH Profit",
                "Outperformance",
                "Above Exit Price",
                "Trend Breakdown",
                "Momentum Breakdown",
                "Support Breakdown",
                "Volume Confirmation",
                "Relative Strength",
                "Risk Deterioration",
                "Reference Match",
            ],
            "STATUS":[

                "🟢 YES" if r["ath_profit"]
                else "🔴 NO",

                "🟢 YES" if r["outperformance"]
                else "🔴 NO",

                "🟢 YES" if r["above_exit"]
                else "🔴 NO",

                "🔴 YES" if r["trend_breakdown"]
                else "🟢 NO",

                "🔴 YES" if r["momentum_breakdown"]
                else "🟢 NO",

                "🔴 YES" if r["support_breakdown"]
                else "🟢 NO",

                "🟢 CONFIRMED"
                if r["volume_confirmed"]
                else "🟡 PENDING",

                "🟢 STRONG"
                if r["relative_strength"]
                else "🟡 WATCH",

                "🔴 YES"
                if r["risk_deterioration"]
                else "🟢 NO",

                "🟢 MATCH"
                if r["reference_match"]
                else "🟡 WATCH",
            ]
        })

        st.dataframe(
            ems_data,
            use_container_width=True,
            hide_index=True
        )

    # ========================================================
    # D/W/M
    # ========================================================

    with tabs[2]:

        dwm_df = pd.DataFrame({
            "TIMEFRAME":[
                "Daily",
                "Weekly",
                "Monthly",
            ],
            "TREND":[
                r["d_tf"]["trend"],
                r["w_tf"]["trend"],
                r["m_tf"]["trend"],
            ],
            "SCORE":[
                r["d_tf"]["score"],
                r["w_tf"]["score"],
                r["m_tf"]["score"],
            ],
        })

        st.dataframe(
            dwm_df,
            use_container_width=True,
            hide_index=True
        )

        st.metric(
            "D/W/M MASTER SCORE",
            f"{r['dwm_score']}/100"
        )

    # ========================================================
    # BREAKOUT
    # ========================================================

    with tabs[3]:

        st.markdown(
            f"""
            <div class="signal breakout">
            {'🔥 BREAKOUT CONFIRMED'
            if r['breakout_confirmed']
            else '🟡 BREAKOUT WATCH'}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.metric(
            "CONFIRMATIONS",
            f"{r['breakout_confirmations']}/7"
        )

        checks = {
            "Price Breakout":
                r["price_breakout"],

            "EMA Alignment":
                r["ema_alignment"],

            "RSI ≥ 60":
                r["rsi"] >= 60,

            "MACD Bullish":
                r["macd_bull"],

            "Supertrend":
                r["supertrend_bull"],

            "CPR Bullish":
                r["cmp"] > r["cpr_high"],

            "Volume ≥ 2×":
                r["volume_confirmed"],
        }

        for name,status in checks.items():

            st.write(
                f"{'✅' if status else '❌'} {name}"
            )

    # ========================================================
    # MOMENTUM
    # ========================================================

    with tabs[4]:

        if r["early_momentum"]:

            st.markdown(
                """
                <div class="signal early">
                ⚡ EARLY MOMENTUM ACTIVE
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.info(
                "Early Momentum currently not confirmed."
            )

        m1,m2,m3 = st.columns(3)

        m1.metric(
            "RSI",
            f"{r['rsi']:.2f}"
        )

        m2.metric(
            "VOLUME",
            f"{r['volume_ratio']:.2f}x"
        )

        m3.metric(
            "MOMENTUM",
            f"{r['momentum_score']}/100"
        )

    # ========================================================
    # CHART — SAFE
    # ========================================================

    with tabs[5]:

        chart_columns = [
            "Close",
            "EMA10",
            "EMA20",
            "EMA50",
            "EMA200",
        ]

        chart_df = r.get("df")

        if chart_df is None or chart_df.empty:

            st.warning(
                "Chart data unavailable."
            )

        else:

            available = [
                c for c in chart_columns
                if c in chart_df.columns
            ]

            if "Close" not in available:

                st.warning(
                    "Close price column unavailable. "
                    "Chart skipped safely."
                )

            else:

                chart = (
                    chart_df[available]
                    .tail(300)
                    .dropna(how="all")
                )

                st.line_chart(
                    chart,
                    height=400
                )

    # ========================================================
    # WHY SIGNAL
    # ========================================================

    st.markdown("### 🧠 WHY THIS SIGNAL?")

    reasons = []

    if r["ema_alignment"]:
        reasons.append(
            "✅ EMA 10 > 20 > 50 > 100 > 200"
        )

    if r["rsi"] >= 60:
        reasons.append(
            "✅ RSI strong"
        )

    if r["macd_bull"]:
        reasons.append(
            "✅ MACD bullish"
        )

    if r["volume_confirmed"]:
        reasons.append(
            "✅ Volume confirmation ≥ 2×"
        )

    if r["early_momentum"]:
        reasons.append(
            "⚡ Early momentum active"
        )

    if r["breakout_confirmed"]:
        reasons.append(
            "🔥 Breakout confirmed"
        )

    if r["risk_meter"] in [
        "HIGH",
        "EXTREME"
    ]:
        reasons.append(
            "⚠️ Elevated risk"
        )

    if not reasons:
        reasons.append(
            "🟡 No strong confirmation"
        )

    for reason in reasons:
        st.write(reason)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🐂 RAJESH STOCK ANALYZER PRO • "
    "NSE Manual Analyzer • "
    "Research & decision-support tool. "
    "Not financial advice."
)
