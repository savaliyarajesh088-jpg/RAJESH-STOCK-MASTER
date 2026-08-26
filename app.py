import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

# ============================================================
# 🐂 RAJESH STOCK ANALYZER PRO V2.3
# NSE ONLY • 1–15 STOCKS
# EMS V3 • D/W/M
# EMA 10/20/30/40/50 • CPR
# MOMENTUM • BREAKOUT + RETEST
# SWING + LONG
# ============================================================

st.set_page_config(
    page_title="RAJESH STOCK ANALYZER PRO V2.3",
    page_icon="🐂",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# CSS — PROFESSIONAL COMPACT MOBILE UI
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at top right,#172554 0,#050505 38%);
    color:#fff;
}

.block-container {
    max-width:1450px;
    padding:0.8rem 0.8rem 3rem;
}

h1,h2,h3,h4,h5 {
    color:#fff !important;
}

.hero {
    background:linear-gradient(
        135deg,
        #020617,
        #172554,
        #312e81,
        #581c87
    );
    border:1px solid #6366f1;
    border-radius:20px;
    padding:18px;
    margin-bottom:14px;
    box-shadow:0 8px 30px rgba(0,0,0,.4);
}

.hero-title {
    font-size:28px;
    font-weight:950;
}

.hero-sub {
    font-size:12px;
    opacity:.78;
}

/* ---------------- DASHBOARD ---------------- */

.dashboard-card {
    background:linear-gradient(135deg,#0f172a,#111827);
    border:1px solid #334155;
    border-radius:14px;
    padding:10px 6px;
    text-align:center;
    min-height:72px;
}

.dashboard-number {
    font-size:20px;
    font-weight:950;
}

.dashboard-label {
    font-size:10px;
    opacity:.7;
}

/* ---------------- STOCK ---------------- */

.stock-card {
    background:linear-gradient(135deg,#0b1120,#111827);
    border:1px solid #334155;
    border-radius:18px;
    padding:14px;
    margin:10px 0;
}

/* ---------------- SIGNAL ---------------- */

.signal {
    border-radius:14px;
    padding:11px;
    text-align:center;
    font-size:21px;
    font-weight:950;
    margin:8px 0 12px;
    border:1px solid rgba(255,255,255,.2);
}

.buy {
    background:linear-gradient(135deg,#166534,#22c55e);
}

.buydip {
    background:linear-gradient(135deg,#14532d,#16a34a);
}

.breakout {
    background:linear-gradient(135deg,#047857,#10b981);
}

.hold {
    background:linear-gradient(135deg,#1d4ed8,#3b82f6);
}

.wait {
    background:linear-gradient(135deg,#a16207,#eab308);
    color:#111 !important;
}

.reduce {
    background:linear-gradient(135deg,#c2410c,#f97316);
}

.exit {
    background:linear-gradient(135deg,#991b1b,#ef4444);
}

/* ---------------- REGIME ---------------- */

.regime {
    display:inline-block;
    padding:5px 12px;
    border-radius:999px;
    font-weight:900;
    font-size:12px;
}

.bull {
    background:#14532d;
    color:#bbf7d0;
    border:1px solid #22c55e;
}

.pig {
    background:#7c2d12;
    color:#fed7aa;
    border:1px solid #f97316;
}

.bear {
    background:#7f1d1d;
    color:#fecaca;
    border:1px solid #ef4444;
}

/* ============================================================
   KEY INDICATOR SQUARE BOXES
   ============================================================ */

.key-grid {
    display:grid;
    grid-template-columns:
        repeat(6, minmax(0,1fr));
    gap:8px;
    margin:8px 0 14px;
}

.key-box {
    background:linear-gradient(
        135deg,
        #0f172a,
        #172033
    );
    border:1px solid #334155;
    border-radius:12px;
    padding:9px 5px;
    min-height:72px;
    text-align:center;
    box-shadow:0 4px 12px rgba(0,0,0,.22);
}

.key-title {
    font-size:10px;
    font-weight:800;
    opacity:.7;
}

.key-value {
    font-size:14px;
    font-weight:950;
    margin-top:5px;
}

.key-positive {
    border-color:#22c55e;
}

.key-warning {
    border-color:#eab308;
}

.key-negative {
    border-color:#ef4444;
}

@media(max-width:900px) {
    .key-grid {
        grid-template-columns:
            repeat(3, minmax(0,1fr));
    }

    .hero-title {
        font-size:22px;
    }
}

@media(max-width:500px) {
    .key-grid {
        grid-template-columns:
            repeat(3, minmax(0,1fr));
        gap:5px;
    }

    .key-box {
        min-height:64px;
        padding:7px 3px;
    }

    .key-title {
        font-size:9px;
    }

    .key-value {
        font-size:12px;
    }
}

/* ============================================================
   COMPACT PRICE BOXES
   ============================================================ */

.price-grid {
    display:grid;
    grid-template-columns:
        repeat(4, minmax(0,1fr));
    gap:8px;
    margin:8px 0;
}

.price-box {
    background:#111827;
    border:1px solid #334155;
    border-radius:12px;
    padding:9px;
    min-height:66px;
    text-align:center;
}

.price-title {
    font-size:10px;
    opacity:.7;
    font-weight:800;
}

.price-value {
    font-size:15px;
    font-weight:950;
    margin-top:4px;
}

.green-box {
    border-color:#22c55e;
}

.red-box {
    border-color:#ef4444;
}

.blue-box {
    border-color:#3b82f6;
}

.yellow-box {
    border-color:#eab308;
}

/* ============================================================
   TARGET BOXES — SMALL
   ============================================================ */

.target-grid {
    display:grid;
    grid-template-columns:
        repeat(3,minmax(0,1fr));
    gap:7px;
    margin:7px 0 13px;
}

.target-box {
    background:linear-gradient(
        135deg,
        #052e16,
        #14532d
    );
    border:1px solid #22c55e;
    border-radius:11px;
    padding:8px 5px;
    min-height:62px;
    text-align:center;
}

.target-title {
    font-size:9px;
    opacity:.78;
    font-weight:850;
}

.target-value {
    font-size:16px;
    font-weight:950;
    margin-top:3px;
}

.target-upside {
    font-size:10px;
    color:#86efac;
    font-weight:900;
}

/* ---------------- METRICS ---------------- */

div[data-testid="stMetric"] {
    background:#111827;
    border:1px solid #374151;
    border-radius:12px;
    padding:8px;
}

.stButton button {
    border-radius:10px;
    font-weight:850;
}

.small {
    font-size:11px;
    opacity:.7;
}

.live {
    color:#86efac;
    font-weight:900;
}

.fallback {
    color:#fde68a;
    font-weight:900;
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

def normalize_symbol(symbol):
    symbol = str(symbol).strip().upper()

    if symbol.endswith(".NS"):
        symbol = symbol[:-3]

    return symbol


def ticker_name(symbol):
    return normalize_symbol(symbol) + ".NS"


def safe_float(value, default=0.0):
    try:
        value = float(value)

        if np.isfinite(value):
            return value

    except Exception:
        pass

    return default


def pct_from_cmp(price, cmp):
    if cmp <= 0:
        return 0

    return ((price - cmp) / cmp) * 100


# ============================================================
# RSI
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

    rs = (
        avg_gain /
        avg_loss.replace(0,np.nan)
    )

    return 100 - (
        100 / (1 + rs)
    )


# ============================================================
# ATR
# ============================================================

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
        [tr1,tr2,tr3],
        axis=1
    ).max(axis=1)

    return tr.ewm(
        alpha=1/period,
        adjust=False
    ).mean()


# ============================================================
# INDICATORS
# ============================================================

def add_indicators(df):

    x = df.copy()

    # Requested master EMA set
    for p in [10,20,30,40,50,100,200]:

        x[f"EMA{p}"] = (
            x["Close"]
            .ewm(
                span=p,
                adjust=False
            )
            .mean()
        )

    x["RSI"] = calculate_rsi(
        x["Close"],
        14
    )

    ema12 = x["Close"].ewm(
        span=12,
        adjust=False
    ).mean()

    ema26 = x["Close"].ewm(
        span=26,
        adjust=False
    ).mean()

    x["MACD"] = ema12 - ema26

    x["MACD_SIGNAL"] = (
        x["MACD"]
        .ewm(
            span=9,
            adjust=False
        ).mean()
    )

    x["ATR"] = calculate_atr(
        x,
        14
    )

    x["VOL_AVG20"] = (
        x["Volume"]
        .rolling(20)
        .mean()
    )

    x["VOL_RATIO"] = (
        x["Volume"] /
        x["VOL_AVG20"].replace(
            0,np.nan
        )
    )

    x["HIGH_52W"] = (
        x["Close"]
        .rolling(252)
        .max()
    )

    x["LOW_52W"] = (
        x["Close"]
        .rolling(252)
        .min()
    )

    return x


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

    x = add_indicators(df)

    last = x.iloc[-1]

    close = safe_float(
        last["Close"]
    )

    checks = [
        close > safe_float(last["EMA20"]),
        close > safe_float(last["EMA50"]),
        close > safe_float(last["EMA200"]),
        safe_float(last["RSI"]) >= 50,
        safe_float(last["MACD"]) >
        safe_float(last["MACD_SIGNAL"])
    ]

    score = round(
        sum(checks) /
        len(checks) *
        100
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


# ============================================================
# DATA DOWNLOAD
# ============================================================

@st.cache_data(
    ttl=300,
    show_spinner=False
)
def download_stock(symbol):

    try:

        df = yf.download(
            ticker_name(symbol),
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

        if any(
            c not in df.columns
            for c in required
        ):
            return None

        return df.dropna(
            subset=["Close"]
        )

    except Exception:
        return None


# ============================================================
# CURRENT PRICE
# ============================================================

def get_current_price(symbol, historical_df):

    try:

        tk = yf.Ticker(
            ticker_name(symbol)
        )

        info = tk.fast_info

        price = safe_float(
            info.get("last_price"),
            0
        )

        if price > 0:

            return {
                "price":price,
                "source":"CURRENT",
                "timestamp":datetime.now()
            }

    except Exception:
        pass

    if (
        historical_df is not None
        and not historical_df.empty
    ):

        price = safe_float(
            historical_df["Close"].iloc[-1]
        )

        return {
            "price":price,
            "source":"YAHOO EOD",
            "timestamp":
                historical_df.index[-1]
        }

    return {
        "price":0,
        "source":"UNAVAILABLE",
        "timestamp":None
    }


# ============================================================
# ANALYSIS
# ============================================================

def analyze(symbol):

    symbol = normalize_symbol(symbol)

    daily = download_stock(symbol)

    if daily is None:

        return {
            "symbol":symbol,
            "error":"Market data unavailable"
        }

    if len(daily) < 220:

        return {
            "symbol":symbol,
            "error":"Insufficient market data"
        }

    d = add_indicators(daily)

    last = d.iloc[-1]

    historical_cmp = safe_float(
        last["Close"]
    )

    current = get_current_price(
        symbol,
        daily
    )

    cmp = (
        current["price"]
        if current["price"] > 0
        else historical_cmp
    )

    # --------------------------------------------------------
    # ALL INDICATOR VALUES
    # IMPORTANT: RETURN THEM SO UI NEVER GETS NameError
    # --------------------------------------------------------

    ema10 = safe_float(last["EMA10"])
    ema20 = safe_float(last["EMA20"])
    ema30 = safe_float(last["EMA30"])
    ema40 = safe_float(last["EMA40"])
    ema50 = safe_float(last["EMA50"])
    ema100 = safe_float(last["EMA100"])
    ema200 = safe_float(last["EMA200"])

    rsi = safe_float(last["RSI"])
    macd = safe_float(last["MACD"])
    macd_signal = safe_float(
        last["MACD_SIGNAL"]
    )

    atr = safe_float(last["ATR"])

    vol_ratio = safe_float(
        last["VOL_RATIO"]
    )

    high52 = safe_float(
        last["HIGH_52W"]
    )

    low52 = safe_float(
        last["LOW_52W"]
    )

    # --------------------------------------------------------
    # EMA 10/20/30/40/50 MASTER ALIGNMENT
    # --------------------------------------------------------

    ema_alignment = (
        cmp >
        ema10 >
        ema20 >
        ema30 >
        ema40 >
        ema50
    )

    # --------------------------------------------------------
    # CPR
    # --------------------------------------------------------

    pivot,cpr_low,cpr_high = (
        calculate_cpr(daily)
    )

    # --------------------------------------------------------
    # MACD
    # --------------------------------------------------------

    macd_bull = (
        macd > macd_signal
    )

    # --------------------------------------------------------
    # SUPERTREND PROXY
    # --------------------------------------------------------

    supertrend_bull = (
        cmp > ema20
        and cmp > ema50
    )

    # --------------------------------------------------------
    # SWING LEVELS
    # --------------------------------------------------------

    recent_high = (
        d["High"]
        .rolling(20)
        .max()
    )

    recent_low = (
        d["Low"]
        .rolling(20)
        .min()
    )

    recent_swing_high = safe_float(
        recent_high.iloc[-2]
    )

    recent_swing_low = safe_float(
        recent_low.iloc[-2]
    )

    # --------------------------------------------------------
    # BREAKOUT + RETEST
    # --------------------------------------------------------

    price_breakout = (
        cmp > recent_swing_high
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
        volume_confirmed
    ])

    breakout_confirmed = (
        price_breakout
        and breakout_confirmations >= 6
    )

    # --------------------------------------------------------
    # EARLY MOMENTUM
    # --------------------------------------------------------

    early_momentum = (
        cmp > ema20
        and rsi >= 55
        and macd_bull
        and vol_ratio >= 1.2
    )

    # --------------------------------------------------------
    # TECH SCORE
    # --------------------------------------------------------

    technical_checks = [
        cmp > ema10,
        cmp > ema20,
        cmp > ema30,
        cmp > ema40,
        cmp > ema50,
        rsi >= 50,
        macd_bull,
        supertrend_bull
    ]

    technical_score = round(
        sum(technical_checks) /
        len(technical_checks) *
        100
    )

    # --------------------------------------------------------
    # MOMENTUM
    # --------------------------------------------------------

    momentum_score = round(
        np.clip(
            ((rsi - 40) * 1.5)
            +
            min(vol_ratio,3) * 12,
            0,
            100
        )
    )

    # --------------------------------------------------------
    # RISK
    # --------------------------------------------------------

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
            100 -
            volatility_pct * 12,
            0,
            100
        )
    )

    # --------------------------------------------------------
    # D/W/M
    # --------------------------------------------------------

    weekly = daily.resample(
        "W-FRI"
    ).agg({
        "Open":"first",
        "High":"max",
        "Low":"min",
        "Close":"last",
        "Volume":"sum"
    }).dropna()

    try:
        monthly = daily.resample(
            "ME"
        ).agg({
            "Open":"first",
            "High":"max",
            "Low":"min",
            "Close":"last",
            "Volume":"sum"
        }).dropna()

    except Exception:
        monthly = daily.resample(
            "M"
        ).agg({
            "Open":"first",
            "High":"max",
            "Low":"min",
            "Close":"last",
            "Volume":"sum"
        }).dropna()

    d_tf = timeframe_analysis(daily)
    w_tf = timeframe_analysis(weekly)
    m_tf = timeframe_analysis(monthly)

    dwm_score = round(
        (
            d_tf["score"]
            +
            w_tf["score"]
            +
            m_tf["score"]
        ) / 3
    )

    # --------------------------------------------------------
    # SUPPORT / RESISTANCE
    # --------------------------------------------------------

    support = max(
        min(ema20,cpr_low),
        recent_swing_low
    )

    resistance = max(
        recent_swing_high,
        cpr_high
    )

    exit_price = max(
        ema50,
        support
    )

    stop_loss = max(
        0,
        min(
            support - atr * 1.25,
            cmp - atr
        )
    )

    # --------------------------------------------------------
    # BUY ZONES
    # --------------------------------------------------------

    buy_zone_low = max(
        0,
        min(
            support,
            cmp - atr*.75
        )
    )

    buy_zone_high = max(
        buy_zone_low,
        min(
            cmp,
            support + atr*.50
        )
    )

    dip_zone_low = max(
        0,
        ema50 - atr
    )

    dip_zone_high = max(
        dip_zone_low,
        ema50 + atr*.25
    )

    breakout_entry = max(
        cmp + atr*.10,
        resistance + atr*.10
    )

    # --------------------------------------------------------
    # SWING TARGETS
    # --------------------------------------------------------

    reference_high = max(
        resistance,
        recent_swing_high,
        cmp
    )

    swing_floor = max(
        cmp*1.025,
        cmp + atr*.75
    )

    swing_t1 = max(
        swing_floor,
        reference_high*1.03
    )

    swing_t2 = max(
        swing_t1 + atr*.75,
        reference_high*1.08,
        cmp*1.075
    )

    swing_t3 = max(
        swing_t2 + atr,
        reference_high*1.15,
        cmp*1.12
    )

    swing_t1 = round(swing_t1,2)
    swing_t2 = round(max(
        swing_t2,
        swing_t1+.01
    ),2)
    swing_t3 = round(max(
        swing_t3,
        swing_t2+.01
    ),2)

    # --------------------------------------------------------
    # LONG TARGETS
    # --------------------------------------------------------

    long_reference = max(
        high52,
        recent_swing_high,
        resistance,
        cmp
    )

    long_t1 = max(
        cmp*1.15,
        long_reference + atr*1.5
    )

    long_t2 = max(
        cmp*1.25,
        long_reference + atr*3.5
    )

    long_t3 = max(
        cmp*1.40,
        long_reference + atr*6
    )

    long_t1 = round(long_t1,2)
    long_t2 = round(max(
        long_t2,
        long_t1+.01
    ),2)
    long_t3 = round(max(
        long_t3,
        long_t2+.01
    ),2)

    # --------------------------------------------------------
    # EMS V3
    # --------------------------------------------------------

    ath_profit = (
        cmp >= high52*.90
    )

    outperformance = (
        momentum_score >= 65
    )

    above_exit = (
        cmp > exit_price
    )

    trend_breakdown = (
        not ema_alignment
    )

    momentum_breakdown = (
        momentum_score < 40
    )

    support_breakdown = (
        cmp < support
    )

    relative_strength = (
        technical_score >= 65
    )

    risk_deterioration = (
        risk_meter in [
            "HIGH",
            "EXTREME"
        ]
    )

    reference_match = (
        d_tf["score"] >= 60
        and
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
        reference_match
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

    # --------------------------------------------------------
    # REGIME
    # --------------------------------------------------------

    bull_points = sum([
        ema_alignment,
        rsi >= 55,
        macd_bull,
        w_tf["score"] >= 60,
        m_tf["score"] >= 55,
        momentum_score >= 60
    ])

    bear_points = sum([
        cmp < ema50,
        rsi < 45,
        not macd_bull,
        w_tf["score"] < 45,
        m_tf["score"] < 45,
        momentum_score < 35
    ])

    if bull_points >= 4:
        regime = "BULL"

    elif bear_points >= 4:
        regime = "BEAR"

    else:
        regime = "PIG"

    # --------------------------------------------------------
    # SIGNAL
    # --------------------------------------------------------

    if breakout_confirmed:

        signal = "BREAKOUT CONFIRMED"
        signal_class = "breakout"

    elif ems_score < 35:

        signal = "SELL / EXIT"
        signal_class = "exit"

    elif (
        technical_score >= 70
        and ems_score >= 60
    ):

        signal = "BUY"
        signal_class = "buy"

    elif early_momentum:

        signal = "BUY ON DIP"
        signal_class = "buydip"

    elif ems_score < 45:

        signal = "REDUCE"
        signal_class = "reduce"

    elif technical_score < 45:

        signal = "WAIT"
        signal_class = "wait"

    else:

        signal = "HOLD"
        signal_class = "hold"

    # ========================================================
    # RETURN — EVERYTHING USED BY UI
    # ========================================================

    return {

        "symbol":symbol,
        "ticker":ticker_name(symbol),

        "cmp":cmp,
        "historical_cmp":historical_cmp,

        "price_source":
            current["source"],

        "price_timestamp":
            current["timestamp"],

        "date":daily.index[-1],

        "signal":signal,
        "signal_class":signal_class,

        "regime":regime,

        "technical_score":
            technical_score,

        "momentum_score":
            momentum_score,

        "risk_score":
            risk_score,

        "risk_meter":
            risk_meter,

        "ems_score":
            ems_score,

        "ems_decision":
            ems_decision,

        # MASTER EMA VALUES
        "ema10":ema10,
        "ema20":ema20,
        "ema30":ema30,
        "ema40":ema40,
        "ema50":ema50,
        "ema100":ema100,
        "ema200":ema200,

        "rsi":rsi,

        "rsi_status":
            (
                "OVERBOUGHT"
                if rsi >= 70
                else
                "STRONG"
                if rsi >= 60
                else
                "POSITIVE"
                if rsi >= 50
                else
                "WEAK"
            ),

        "macd":macd,
        "macd_signal":macd_signal,

        "volume_ratio":vol_ratio,

        "ema_alignment":
            ema_alignment,

        "macd_bull":
            macd_bull,

        "supertrend_bull":
            supertrend_bull,

        "price_breakout":
            price_breakout,

        "breakout_confirmed":
            breakout_confirmed,

        "breakout_confirmations":
            breakout_confirmations,

        "early_momentum":
            early_momentum,

        "d_tf":d_tf,
        "w_tf":w_tf,
        "m_tf":m_tf,

        "dwm_score":
            dwm_score,

        "pivot":pivot,
        "cpr_low":cpr_low,
        "cpr_high":cpr_high,

        "support":support,
        "resistance":resistance,

        "recent_swing_high":
            recent_swing_high,

        "recent_swing_low":
            recent_swing_low,

        "high52":high52,
        "low52":low52,

        "buy_zone_low":
            buy_zone_low,

        "buy_zone_high":
            buy_zone_high,

        "dip_zone_low":
            dip_zone_low,

        "dip_zone_high":
            dip_zone_high,

        "breakout_entry":
            breakout_entry,

        "exit_price":
            exit_price,

        "stop_loss":
            stop_loss,

        "swing_t1":
            swing_t1,

        "swing_t2":
            swing_t2,

        "swing_t3":
            swing_t3,

        "swing_t1_upside":
            pct_from_cmp(
                swing_t1,cmp
            ),

        "swing_t2_upside":
            pct_from_cmp(
                swing_t2,cmp
            ),

        "swing_t3_upside":
            pct_from_cmp(
                swing_t3,cmp
            ),

        "long_t1":
            long_t1,

        "long_t2":
            long_t2,

        "long_t3":
            long_t3,

        "long_t1_upside":
            pct_from_cmp(
                long_t1,cmp
            ),

        "long_t2_upside":
            pct_from_cmp(
                long_t2,cmp
            ),

        "long_t3_upside":
            pct_from_cmp(
                long_t3,cmp
            ),

        "ath_profit":
            ath_profit,

        "outperformance":
            outperformance,

        "above_exit":
            above_exit,

        "trend_breakdown":
            trend_breakdown,

        "momentum_breakdown":
            momentum_breakdown,

        "support_breakdown":
            support_breakdown,

        "volume_confirmed":
            volume_confirmed,

        "relative_strength":
            relative_strength,

        "risk_deterioration":
            risk_deterioration,

        "reference_match":
            reference_match,

        "df":d
    }


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">

<div class="hero-title">
🐂 RAJESH STOCK ANALYZER PRO V2.3
</div>

<div class="hero-sub">
NSE • Manual 1–15 Stocks • EMS V3 • D/W/M •
EMA 10/20/30/40/50 • CPR • Momentum •
Breakout + Retest • Swing + Long
</div>

</div>
""",unsafe_allow_html=True)


# ============================================================
# MASTER SETTINGS
# ============================================================

with st.expander(
    "⚙️ MASTER SETTINGS",
    expanded=True
):

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        strategy = st.selectbox(
            "Strategy",
            [
                "SWING + LONG",
                "SWING",
                "LONG-TERM"
            ]
        )

    with c2:
        data_mode = st.selectbox(
            "Data Mode",
            [
                "AUTO",
                "EOD",
                "LIVE*"
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
    "🟢 Free Yahoo current-price attempt is used where available. "
    "If unavailable, latest EOD price is used as fallback. "
    "This is NOT an exchange-grade NSE real-time feed."
)


# ============================================================
# ADD STOCK
# ============================================================

st.subheader("➕ ADD STOCK")

a1,a2 = st.columns([4,1])

with a1:

    new_stock = st.text_input(
        "NSE Symbol",
        placeholder="BEL, BSE, AIIL, RATNAVEER...",
        label_visibility="collapsed"
    )

with a2:

    add_clicked = st.button(
        "➕ ADD",
        use_container_width=True
    )

if add_clicked:

    stock = normalize_symbol(
        new_stock
    )

    if not stock:

        st.warning(
            "NSE stock symbol નાખો."
        )

    elif stock in st.session_state.watchlist:

        st.info(
            f"{stock} પહેલેથી watchlistમાં છે."
        )

    elif len(
        st.session_state.watchlist
    ) >= 15:

        st.error(
            "Maximum 15 stocks."
        )

    else:

        st.session_state.watchlist.append(
            stock
        )

        st.success(
            f"{stock} added."
        )

        st.rerun()


# ============================================================
# WATCHLIST
# ============================================================

if st.session_state.watchlist:

    st.subheader(
        "📋 MY STOCKS"
    )

    cols = st.columns(
        min(
            len(
                st.session_state.watchlist
            ),
            5
        )
    )

    for i,stock in enumerate(
        list(
            st.session_state.watchlist
        )
    ):

        with cols[
            i % len(cols)
        ]:

            st.markdown(
                f"**{stock}**"
            )

            if st.button(
                f"✖ Remove {stock}",
                key=f"remove_{stock}",
                use_container_width=True
            ):

                # ONLY SELECTED STOCK REMOVED
                st.session_state.watchlist.remove(
                    stock
                )

                st.session_state.analysis_cache.pop(
                    stock,
                    None
                )

                st.rerun()


# ============================================================
# CONTROLS
# ============================================================

st.divider()

c1,c2,c3 = st.columns(
    [2,1,1]
)

with c1:

    analyze_all = st.button(
        "🔍 ANALYZE ALL",
        type="primary",
        use_container_width=True
    )

with c2:

    refresh_all = st.button(
        "🔄 REFRESH",
        use_container_width=True
    )

with c3:

    clear_cache = st.button(
        "🧹 CLEAR CACHE",
        use_container_width=True
    )


if clear_cache:

    st.session_state.analysis_cache = {}

    st.cache_data.clear()

    st.success(
        "All analysis cache cleared."
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
                    "error":
                        f"Analysis error: {str(e)[:150]}"
                }

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
# COLLECT RESULTS
# ============================================================

results = []
errors = []

for stock in st.session_state.watchlist:

    result = (
        st.session_state
        .analysis_cache
        .get(stock)
    )

    if (
        result
        and
        "error" not in result
    ):

        results.append(result)

    elif (
        result
        and
        "error" in result
    ):

        errors.append(result)


for e in errors:

    st.warning(
        f"⚠️ {e['symbol']}: {e['error']}"
    )


if not results:

    st.info(
        "Stock add કરો અને "
        "**ANALYZE ALL** દબાવો."
    )

    st.stop()


# ============================================================
# SMART DASHBOARD
# ============================================================

st.divider()

st.subheader(
    "🚦 SMART SIGNAL DASHBOARD"
)

total = len(results)

positive = sum(
    r["signal"] in [
        "BUY",
        "BUY ON DIP",
        "BREAKOUT CONFIRMED",
        "HOLD"
    ]
    for r in results
)

risk_exit = sum(
    r["signal"] in [
        "REDUCE",
        "SELL / EXIT",
        "WAIT"
    ]
    for r in results
)

avg_ems = round(
    np.mean([
        r["ems_score"]
        for r in results
    ])
)

avg_tech = round(
    np.mean([
        r["technical_score"]
        for r in results
    ])
)

bull_count = sum(
    r["regime"] == "BULL"
    for r in results
)

bear_count = sum(
    r["regime"] == "BEAR"
    for r in results
)

metrics = [
    ("📊","ANALYZED",total),
    ("🟢","POSITIVE",positive),
    ("⚠️","RISK / EXIT",risk_exit),
    ("🧠","AVG EMS",f"{avg_ems}/100"),
    ("📈","AVG TECH",f"{avg_tech}/100"),
    ("🐂","BULL",bull_count),
    ("🐻","BEAR",bear_count)
]

dash = st.columns(7)

for col,(icon,label,value) in zip(
    dash,
    metrics
):

    with col:

        st.markdown(
            f"""
            <div class="dashboard-card">
                <div class="dashboard-number">
                    {icon} {value}
                </div>
                <div class="dashboard-label">
                    {label}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# SUMMARY
# ============================================================

st.markdown(
    "### 📋 QUICK SUMMARY"
)

summary = []

for r in results:

    summary.append({

        "STOCK":r["symbol"],
        "REGIME":r["regime"],
        "SIGNAL":r["signal"],
        "CMP":round(r["cmp"],2),
        "EMS":r["ems_score"],
        "TECH":r["technical_score"],
        "MOM":r["momentum_score"],
        "D/W/M":r["dwm_score"],
        "RISK":r["risk_meter"],
        "SWING T1":
            f"₹{r['swing_t1']:,.0f}",
        "UPSIDE":
            f"+{r['swing_t1_upside']:.1f}%"
    })

st.dataframe(
    pd.DataFrame(summary),
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
    "BULL",
    "PIG",
    "BEAR"
]

filter_signal = st.selectbox(
    "🔎 SIGNAL FILTER",
    filter_options
)

display_results = results

if filter_signal != "ALL":

    if filter_signal in [
        "BULL",
        "PIG",
        "BEAR"
    ]:

        display_results = [
            r for r in results
            if r["regime"] == filter_signal
        ]

    else:

        display_results = [
            r for r in results
            if r["signal"] == filter_signal
        ]


# ============================================================
# STOCK RESULTS
# ============================================================

for r in display_results:

    st.divider()

    regime_class = {
        "BULL":"bull",
        "PIG":"pig",
        "BEAR":"bear"
    }.get(
        r["regime"],
        "pig"
    )

    regime_icon = {
        "BULL":"🐂",
        "PIG":"🐷",
        "BEAR":"🐻"
    }.get(
        r["regime"],
        "🐷"
    )

    price_label = (
        "🟢 CURRENT"
        if r["price_source"] == "CURRENT"
        else "🟡 EOD FALLBACK"
    )

    st.markdown(
        f"""
        <div class="stock-card">

        <h2>🏢 {r['symbol']}</h2>

        <div class="small">
        {r['ticker']} • NSE •
        Analysis: {r['date'].date()}
        </div>

        <div class="live">
        {price_label}
        </div>

        <div class="regime {regime_class}">
        {regime_icon} {r['regime']}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # SIGNAL
    # ========================================================

    st.markdown(
        f"""
        <div class="signal {r['signal_class']}">
        🚦 {r['signal']}
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # MAIN METRICS
    # ========================================================

    c1,c2,c3,c4,c5 = st.columns(5)

    c1.metric(
        "CMP",
        f"₹{r['cmp']:,.2f}"
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
        "D/W/M",
        f"{r['dwm_score']}/100"
    )


    # ========================================================
    # ⭐ KEY INDICATORS — MAIN BOARD
    # ========================================================

    st.markdown(
        "### 📊 KEY INDICATORS"
    )

    def key_class(value_type):

        if value_type == "positive":
            return "key-box key-positive"

        if value_type == "negative":
            return "key-box key-negative"

        if value_type == "warning":
            return "key-box key-warning"

        return "key-box"


    indicator_boxes = [

        (
            "EMA 10",
            f"₹{r['ema10']:,.2f}",
            "positive"
        ),

        (
            "EMA 20",
            f"₹{r['ema20']:,.2f}",
            "positive"
        ),

        (
            "EMA 30",
            f"₹{r['ema30']:,.2f}",
            "positive"
        ),

        (
            "EMA 40",
            f"₹{r['ema40']:,.2f}",
            "positive"
        ),

        (
            "EMA 50",
            f"₹{r['ema50']:,.2f}",
            "positive"
        ),

        (
            "CPR",
            f"₹{r['cpr_low']:,.0f}"
            f" – ₹{r['cpr_high']:,.0f}",
            "warning"
        ),

        (
            "RSI 14",
            f"{r['rsi']:.1f}",
            (
                "negative"
                if r["rsi"] < 40
                else "positive"
            )
        ),

        (
            "MACD",
            "🟢 BULL"
            if r["macd_bull"]
            else "🔴 BEAR",
            (
                "positive"
                if r["macd_bull"]
                else "negative"
            )
        ),

        (
            "SUPERTREND",
            "🟢 BULL"
            if r["supertrend_bull"]
            else "🔴 BEAR",
            (
                "positive"
                if r["supertrend_bull"]
                else "negative"
            )
        ),

        (
            "VOLUME",
            f"{r['volume_ratio']:.2f}x",
            (
                "positive"
                if r["volume_ratio"] >= 2
                else "warning"
            )
        ),

        (
            "52W HIGH",
            f"₹{r['high52']:,.0f}",
            "default"
        ),

        (
            "BREAKOUT",
            "🔥 CONFIRMED"
            if r["breakout_confirmed"]
            else "🟡 WATCH",
            (
                "positive"
                if r["breakout_confirmed"]
                else "warning"
            )
        )
    ]

    html = '<div class="key-grid">'

    for title,value,status in indicator_boxes:

        html += f"""
        <div class="{key_class(status)}">
            <div class="key-title">
                {title}
            </div>
            <div class="key-value">
                {value}
            </div>
        </div>
        """

    html += "</div>"

    st.markdown(
        html,
        unsafe_allow_html=True
    )


    # ========================================================
    # PRICE LEVELS
    # ========================================================

    st.markdown(
        "### 🎯 PRICE LEVELS"
    )

    html = f"""
    <div class="price-grid">

        <div class="price-box blue-box">
            <div class="price-title">SUPPORT</div>
            <div class="price-value">
                ₹{r['support']:,.2f}
            </div>
        </div>

        <div class="price-box blue-box">
            <div class="price-title">RESISTANCE</div>
            <div class="price-value">
                ₹{r['resistance']:,.2f}
            </div>
        </div>

        <div class="price-box yellow-box">
            <div class="price-title">52W HIGH</div>
            <div class="price-value">
                ₹{r['high52']:,.2f}
            </div>
        </div>

        <div class="price-box red-box">
            <div class="price-title">STOP LOSS</div>
            <div class="price-value">
                ₹{r['stop_loss']:,.2f}
            </div>
        </div>

    </div>
    """

    st.markdown(
        html,
        unsafe_allow_html=True
    )


    # ========================================================
    # ENTRY
    # ========================================================

    st.markdown(
        "### 🛡️ ENTRY + RISK"
    )

    html = f"""
    <div class="price-grid">

        <div class="price-box green-box">
            <div class="price-title">
                🟢 BUY ZONE
            </div>
            <div class="price-value">
                ₹{r['buy_zone_low']:,.0f}
                – ₹{r['buy_zone_high']:,.0f}
            </div>
        </div>

        <div class="price-box green-box">
            <div class="price-title">
                🟢 BUY ON DIP
            </div>
            <div class="price-value">
                ₹{r['dip_zone_low']:,.0f}
                – ₹{r['dip_zone_high']:,.0f}
            </div>
        </div>

        <div class="price-box blue-box">
            <div class="price-title">
                🚀 BREAKOUT
            </div>
            <div class="price-value">
                ₹{r['breakout_entry']:,.2f}
            </div>
        </div>

        <div class="price-box red-box">
            <div class="price-title">
                EXIT PRICE
            </div>
            <div class="price-value">
                ₹{r['exit_price']:,.2f}
            </div>
        </div>

    </div>
    """

    st.markdown(
        html,
        unsafe_allow_html=True
    )


    # ========================================================
    # COMPACT SWING TARGETS
    # ========================================================

    st.markdown(
        "### 🎯 SWING TARGETS"
    )

    html = '<div class="target-grid">'

    for label,target,upside in [
        (
            "T1",
            r["swing_t1"],
            r["swing_t1_upside"]
        ),
        (
            "T2",
            r["swing_t2"],
            r["swing_t2_upside"]
        ),
        (
            "T3",
            r["swing_t3"],
            r["swing_t3_upside"]
        )
    ]:

        html += f"""
        <div class="target-box">

            <div class="target-title">
                SWING {label}
            </div>

            <div class="target-value">
                ₹{target:,.2f}
            </div>

            <div class="target-upside">
                +{upside:.1f}%
            </div>

        </div>
        """

    html += "</div>"

    st.markdown(
        html,
        unsafe_allow_html=True
    )


    # ========================================================
    # COMPACT LONG TARGETS
    # ========================================================

    st.markdown(
        "### 🏆 LONG-TERM TARGETS"
    )

    html = '<div class="target-grid">'

    for label,target,upside in [
        (
            "T1",
            r["long_t1"],
            r["long_t1_upside"]
        ),
        (
            "T2",
            r["long_t2"],
            r["long_t2_upside"]
        ),
        (
            "T3",
            r["long_t3"],
            r["long_t3_upside"]
        )
    ]:

        html += f"""
        <div class="target-box">

            <div class="target-title">
                LONG {label}
            </div>

            <div class="target-value">
                ₹{target:,.2f}
            </div>

            <div class="target-upside">
                +{upside:.1f}%
            </div>

        </div>
        """

    html += "</div>"

    st.markdown(
        html,
        unsafe_allow_html=True
    )


    # ========================================================
    # TABS
    # ========================================================

    tabs = st.tabs([
        "🧠 EMS",
        "📊 D/W/M",
        "🚀 BREAKOUT",
        "⚡ MOMENTUM",
        "📈 CHART",
        "📚 ALL INDICATORS"
    ])


    # ========================================================
    # EMS
    # ========================================================

    with tabs[0]:

        st.markdown(
            f"""
            <div class="signal hold">
            🧠 EMS V3 — {r['ems_score']}/100
            • {r['ems_decision']}
            </div>
            """,
            unsafe_allow_html=True
        )

        ems_df = pd.DataFrame({

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
                "Reference Match"
            ],

            "STATUS":[

                "🟢 YES"
                if r["ath_profit"]
                else "🔴 NO",

                "🟢 YES"
                if r["outperformance"]
                else "🔴 NO",

                "🟢 YES"
                if r["above_exit"]
                else "🔴 NO",

                "🔴 YES"
                if r["trend_breakdown"]
                else "🟢 NO",

                "🔴 YES"
                if r["momentum_breakdown"]
                else "🟢 NO",

                "🔴 YES"
                if r["support_breakdown"]
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
                else "🟡 WATCH"
            ]
        })

        st.dataframe(
            ems_df,
            use_container_width=True,
            hide_index=True
        )


    # ========================================================
    # D/W/M
    # ========================================================

    with tabs[1]:

        dwm_df = pd.DataFrame({

            "TIMEFRAME":[
                "Daily",
                "Weekly",
                "Monthly"
            ],

            "TREND":[
                r["d_tf"]["trend"],
                r["w_tf"]["trend"],
                r["m_tf"]["trend"]
            ],

            "SCORE":[
                r["d_tf"]["score"],
                r["w_tf"]["score"],
                r["m_tf"]["score"]
            ]
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

    with tabs[2]:

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
                r["volume_confirmed"]
        }

        for name,status in checks.items():

            st.write(
                f"{'✅' if status else '❌'} {name}"
            )


    # ========================================================
    # MOMENTUM
    # ========================================================

    with tabs[3]:

        if r["early_momentum"]:

            st.markdown(
                """
                <div class="signal buydip">
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
    # CHART
    # ========================================================

    with tabs[4]:

        chart_df = r.get(
            "df",
            pd.DataFrame()
        )

        chart_cols = [
            "Close",
            "EMA10",
            "EMA20",
            "EMA30",
            "EMA40",
            "EMA50"
        ]

        available = [
            c for c in chart_cols
            if c in chart_df.columns
        ]

        if available:

            chart = (
                chart_df[available]
                .tail(300)
                .dropna(how="all")
            )

            st.line_chart(
                chart,
                height=380
            )

        else:

            st.warning(
                "Chart data unavailable."
            )


    # ========================================================
    # ALL INDICATORS
    # ========================================================

    with tabs[5]:

        indicator_df = pd.DataFrame({

            "INDICATOR":[
                "EMA 10",
                "EMA 20",
                "EMA 30",
                "EMA 40",
                "EMA 50",
                "EMA 100",
                "EMA 200",
                "RSI 14",
                "MACD 12/26/9",
                "Supertrend 10/3",
                "CPR",
                "Classic Pivot",
                "Volume Ratio",
                "52W High",
                "52W Low",
                "Swing High",
                "Swing Low"
            ],

            "VALUE":[

                f"₹{r['ema10']:,.2f}",
                f"₹{r['ema20']:,.2f}",
                f"₹{r['ema30']:,.2f}",
                f"₹{r['ema40']:,.2f}",
                f"₹{r['ema50']:,.2f}",
                f"₹{r['ema100']:,.2f}",
                f"₹{r['ema200']:,.2f}",

                f"{r['rsi']:.2f}",

                "🟢 BULLISH"
                if r["macd_bull"]
                else "🔴 BEARISH",

                "🟢 BULLISH"
                if r["supertrend_bull"]
                else "🔴 BEARISH",

                f"₹{r['cpr_low']:,.2f}"
                f" – ₹{r['cpr_high']:,.2f}",

                f"₹{r['pivot']:,.2f}",

                f"{r['volume_ratio']:.2f}x",

                f"₹{r['high52']:,.2f}",

                f"₹{r['low52']:,.2f}",

                f"₹{r['recent_swing_high']:,.2f}",

                f"₹{r['recent_swing_low']:,.2f}"
            ]
        })

        st.dataframe(
            indicator_df,
            use_container_width=True,
            hide_index=True
        )


    # ========================================================
    # WHY SIGNAL
    # ========================================================

    st.markdown(
        "### 🧠 WHY THIS SIGNAL?"
    )

    reasons = []

    if r["ema_alignment"]:
        reasons.append(
            "✅ EMA 10 > 20 > 30 > 40 > 50"
        )

    if r["rsi"] >= 60:
        reasons.append(
            "✅ RSI strong"
        )

    elif r["rsi"] >= 50:
        reasons.append(
            "🟢 RSI positive"
        )

    if r["macd_bull"]:
        reasons.append(
            "✅ MACD bullish"
        )

    if r["volume_confirmed"]:
        reasons.append(
            "✅ Volume ≥ 2×"
        )

    if r["breakout_confirmed"]:
        reasons.append(
            "🔥 Breakout confirmed"
        )

    if r["early_momentum"]:
        reasons.append(
            "⚡ Early momentum active"
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
    "🐂 RAJESH STOCK ANALYZER PRO V2.3 • "
    "NSE Manual Analyzer • "
    "Research & decision-support tool • "
    "Not financial advice."
)
