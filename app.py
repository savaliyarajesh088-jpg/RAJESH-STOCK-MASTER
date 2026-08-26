import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

# ============================================================
# 🐂 RAJESH STOCK ANALYZER PRO V2.2
# NSE ONLY • 1–15 STOCKS
# EMS V3 • D/W/M • CPR • EMA 10/20/30/40/50
# MOMENTUM • BREAKOUT + RETEST • SWING + LONG
# ============================================================

st.set_page_config(
    page_title="RAJESH STOCK ANALYZER PRO V2.2",
    page_icon="🐂",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

.stApp{
    background:
    radial-gradient(circle at top right,#172554 0,#050505 38%);
    color:#fff;
}

.block-container{
    max-width:1500px;
    padding:1rem 1rem 4rem 1rem;
}

h1,h2,h3,h4,h5,h6{
    color:#fff !important;
}

.hero{
    background:linear-gradient(
        135deg,
        #020617,
        #172554,
        #312e81,
        #581c87
    );
    border:1px solid #6366f1;
    border-radius:24px;
    padding:22px;
    margin-bottom:18px;
    box-shadow:0 10px 40px rgba(0,0,0,.45);
}

.hero-title{
    font-size:31px;
    font-weight:950;
}

.hero-sub{
    font-size:13px;
    opacity:.82;
}

.stock-card{
    background:linear-gradient(
        135deg,
        #0b1120,
        #111827
    );
    border:1px solid #334155;
    border-radius:22px;
    padding:18px;
    margin:15px 0;
    box-shadow:0 10px 35px rgba(0,0,0,.38);
}

.square-grid{
    display:grid;
    grid-template-columns:
        repeat(6,minmax(100px,1fr));
    gap:10px;
    margin:12px 0;
}

.square-box{
    background:linear-gradient(
        135deg,
        #111827,
        #172033
    );
    border:1px solid #334155;
    border-radius:14px;
    min-height:88px;
    padding:11px;
    text-align:center;
    display:flex;
    flex-direction:column;
    justify-content:center;
}

.square-title{
    font-size:11px;
    opacity:.72;
    font-weight:800;
}

.square-value{
    font-size:19px;
    font-weight:950;
    margin-top:5px;
}

.metric-grid{
    display:grid;
    grid-template-columns:
        repeat(5,minmax(110px,1fr));
    gap:10px;
    margin:12px 0;
}

.metric-box{
    background:#111827;
    border:1px solid #374151;
    border-radius:14px;
    padding:12px;
    text-align:center;
}

.metric-title{
    font-size:11px;
    opacity:.7;
}

.metric-value{
    font-size:22px;
    font-weight:950;
}

.regime{
    display:inline-block;
    padding:7px 16px;
    border-radius:999px;
    font-weight:950;
    margin:7px 0;
}

.bull{
    background:#14532d;
    color:#bbf7d0;
    border:1px solid #22c55e;
}

.pig{
    background:#7c2d12;
    color:#fed7aa;
    border:1px solid #f97316;
}

.bear{
    background:#7f1d1d;
    color:#fecaca;
    border:1px solid #ef4444;
}

.signal{
    border-radius:18px;
    padding:14px;
    text-align:center;
    font-size:23px;
    font-weight:950;
    margin:10px 0 14px;
    border:1px solid rgba(255,255,255,.25);
}

.buy{
    background:linear-gradient(135deg,#166534,#22c55e);
}

.buydip{
    background:linear-gradient(135deg,#14532d,#16a34a);
}

.breakout{
    background:linear-gradient(135deg,#047857,#10b981);
}

.hold{
    background:linear-gradient(135deg,#1d4ed8,#3b82f6);
}

.wait{
    background:linear-gradient(135deg,#a16207,#eab308);
    color:#111 !important;
}

.reduce{
    background:linear-gradient(135deg,#c2410c,#f97316);
}

.exit{
    background:linear-gradient(135deg,#991b1b,#ef4444);
}

.zone{
    background:linear-gradient(
        135deg,
        #172554,
        #1e3a8a
    );
    border:1px solid #3b82f6;
    border-radius:16px;
    padding:14px;
    min-height:100px;
}

.target{
    background:linear-gradient(
        135deg,
        #052e16,
        #14532d
    );
    border:1px solid #22c55e;
    border-radius:16px;
    padding:14px;
    min-height:105px;
}

.risk{
    background:linear-gradient(
        135deg,
        #450a0a,
        #7f1d1d
    );
    border:1px solid #ef4444;
    border-radius:16px;
    padding:14px;
    min-height:100px;
}

.upside{
    color:#86efac;
    font-weight:900;
}

.live{
    color:#86efac;
    font-weight:900;
}

.eod{
    color:#fde68a;
    font-weight:900;
}

.small{
    font-size:12px;
    opacity:.72;
}

.stButton button{
    border-radius:12px;
    font-weight:850;
}

@media(max-width:900px){

    .square-grid{
        grid-template-columns:
            repeat(3,minmax(90px,1fr));
    }

    .metric-grid{
        grid-template-columns:
            repeat(2,minmax(110px,1fr));
    }

    .hero-title{
        font-size:24px;
    }
}

@media(max-width:520px){

    .square-grid{
        grid-template-columns:
            repeat(2,minmax(90px,1fr));
    }

    .metric-grid{
        grid-template-columns:
            repeat(2,minmax(100px,1fr));
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
    st.session_state.last_refresh = "—"


# ============================================================
# HELPERS
# ============================================================

def normalize_symbol(symbol):
    symbol = str(symbol or "").strip().upper()

    if symbol.endswith(".NS"):
        symbol = symbol[:-3]

    return symbol


def ns_symbol(symbol):
    return normalize_symbol(symbol) + ".NS"


def safe_float(value, default=0.0):
    try:
        value = float(value)

        if np.isfinite(value):
            return value

    except Exception:
        pass

    return default


def pct(price, cmp):
    if cmp <= 0:
        return 0.0

    return ((price - cmp) / cmp) * 100


def money(value):
    return f"₹{safe_float(value):,.2f}"


def safe_bool(value):
    try:
        return bool(value)
    except Exception:
        return False


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

    rs = avg_gain / avg_loss.replace(
        0,
        np.nan
    )

    return 100 - (100 / (1 + rs))


def calculate_atr(df, period=14):

    prev_close = df["Close"].shift(1)

    tr = pd.concat(
        [
            df["High"] - df["Low"],
            (df["High"] - prev_close).abs(),
            (df["Low"] - prev_close).abs(),
        ],
        axis=1
    ).max(axis=1)

    return tr.ewm(
        alpha=1 / period,
        adjust=False
    ).mean()


def add_indicators(df):

    x = df.copy()

    # --------------------------------------------------------
    # EMA MASTER
    # --------------------------------------------------------

    for period in [
        10,
        20,
        30,
        40,
        50,
        100,
        200
    ]:

        x[f"EMA{period}"] = (
            x["Close"]
            .ewm(
                span=period,
                adjust=False
            )
            .mean()
        )

    # --------------------------------------------------------
    # RSI
    # --------------------------------------------------------

    x["RSI14"] = calculate_rsi(
        x["Close"],
        14
    )

    # --------------------------------------------------------
    # MACD 12/26/9
    # --------------------------------------------------------

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
        )
        .mean()
    )

    x["MACD_HIST"] = (
        x["MACD"] -
        x["MACD_SIGNAL"]
    )

    # --------------------------------------------------------
    # ATR
    # --------------------------------------------------------

    x["ATR14"] = calculate_atr(
        x,
        14
    )

    # --------------------------------------------------------
    # VOLUME
    # --------------------------------------------------------

    x["VOL_AVG20"] = (
        x["Volume"]
        .rolling(20)
        .mean()
    )

    x["VOL_RATIO"] = (
        x["Volume"] /
        x["VOL_AVG20"].replace(
            0,
            np.nan
        )
    )

    # --------------------------------------------------------
    # 52 WEEK
    # --------------------------------------------------------

    x["HIGH52"] = (
        x["High"]
        .rolling(252)
        .max()
    )

    x["LOW52"] = (
        x["Low"]
        .rolling(252)
        .min()
    )

    return x


# ============================================================
# CPR
# ============================================================

def calculate_cpr(df):

    if df is None or len(df) < 2:
        return 0.0, 0.0, 0.0

    previous = df.iloc[-2]

    pivot = (
        safe_float(previous["High"])
        +
        safe_float(previous["Low"])
        +
        safe_float(previous["Close"])
    ) / 3

    bc = (
        safe_float(previous["High"])
        +
        safe_float(previous["Low"])
    ) / 2

    tc = (
        2 * pivot
    ) - bc

    return (
        pivot,
        min(bc, tc),
        max(bc, tc)
    )


# ============================================================
# SUPERTREND
# ============================================================

def calculate_supertrend(
    df,
    period=10,
    multiplier=3
):

    x = df.copy()

    atr = calculate_atr(
        x,
        period
    )

    hl2 = (
        x["High"] +
        x["Low"]
    ) / 2

    upper = (
        hl2 +
        multiplier * atr
    )

    lower = (
        hl2 -
        multiplier * atr
    )

    direction = pd.Series(
        1,
        index=x.index
    )

    for i in range(1, len(x)):

        close = safe_float(
            x["Close"].iloc[i]
        )

        prev_upper = safe_float(
            upper.iloc[i - 1]
        )

        prev_lower = safe_float(
            lower.iloc[i - 1]
        )

        curr_upper = safe_float(
            upper.iloc[i]
        )

        curr_lower = safe_float(
            lower.iloc[i]
        )

        if close > prev_upper:
            direction.iloc[i] = 1

        elif close < prev_lower:
            direction.iloc[i] = -1

        else:
            direction.iloc[i] = direction.iloc[i - 1]

            if direction.iloc[i] == 1:
                lower.iloc[i] = max(
                    curr_lower,
                    prev_lower
                )

            else:
                upper.iloc[i] = min(
                    curr_upper,
                    prev_upper
                )

    x["SUPERTREND_DIR"] = direction

    return x


# ============================================================
# TIMEFRAME
# ============================================================

def timeframe_score(df):

    if df is None or len(df) < 30:

        return {
            "score": 0,
            "trend": "UNKNOWN"
        }

    x = add_indicators(df)

    x = calculate_supertrend(
        x,
        10,
        3
    )

    last = x.iloc[-1]

    close = safe_float(
        last["Close"]
    )

    checks = [
        close > safe_float(last["EMA20"]),
        close > safe_float(last["EMA50"]),
        close > safe_float(last["EMA200"]),
        safe_float(last["RSI14"]) >= 50,
        safe_float(last["MACD"]) >
        safe_float(last["MACD_SIGNAL"]),
        safe_float(last["SUPERTREND_DIR"]) > 0,
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
        "score": score,
        "trend": trend
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

        ticker = ns_symbol(symbol)

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

        df = df[
            required
        ].copy()

        df = df.apply(
            pd.to_numeric,
            errors="coerce"
        )

        df = df.dropna(
            subset=["Close"]
        )

        return df

    except Exception:

        return None


# ============================================================
# CURRENT PRICE
# ============================================================

def get_current_price(
    symbol,
    historical
):

    ticker = ns_symbol(symbol)

    # --------------------------------------------------------
    # 1. FAST INFO
    # --------------------------------------------------------

    try:

        tk = yf.Ticker(ticker)

        info = tk.fast_info

        if info:

            price = safe_float(
                info.get(
                    "last_price"
                )
            )

            if price > 0:

                return {
                    "price": price,
                    "source": "CURRENT",
                    "timestamp":
                        datetime.now()
                }

    except Exception:
        pass

    # --------------------------------------------------------
    # 2. 1D / 1M INTRADAY ATTEMPT
    # --------------------------------------------------------

    try:

        intraday = yf.download(
            ticker,
            period="1d",
            interval="1m",
            auto_adjust=False,
            progress=False,
            threads=False
        )

        if (
            intraday is not None
            and not intraday.empty
        ):

            if isinstance(
                intraday.columns,
                pd.MultiIndex
            ):

                intraday.columns = [
                    c[0]
                    if isinstance(c, tuple)
                    else c
                    for c in intraday.columns
                ]

            if "Close" in intraday.columns:

                last_price = safe_float(
                    intraday["Close"]
                    .dropna()
                    .iloc[-1]
                )

                if last_price > 0:

                    return {
                        "price": last_price,
                        "source": "INTRADAY",
                        "timestamp":
                            intraday.index[-1]
                    }

    except Exception:
        pass

    # --------------------------------------------------------
    # 3. EOD FALLBACK
    # --------------------------------------------------------

    if (
        historical is not None
        and not historical.empty
    ):

        price = safe_float(
            historical["Close"].iloc[-1]
        )

        if price > 0:

            return {
                "price": price,
                "source": "EOD FALLBACK",
                "timestamp":
                    historical.index[-1]
            }

    return {
        "price": 0,
        "source": "UNAVAILABLE",
        "timestamp": None
    }


# ============================================================
# ANALYSIS ENGINE
# ============================================================

def analyze(symbol):

    symbol = normalize_symbol(symbol)

    daily_raw = download_stock(
        symbol
    )

    if (
        daily_raw is None
        or daily_raw.empty
    ):

        return {
            "symbol": symbol,
            "error":
                "Market data unavailable"
        }

    if len(daily_raw) < 220:

        return {
            "symbol": symbol,
            "error":
                "Insufficient historical data"
        }

    d = add_indicators(
        daily_raw
    )

    d = calculate_supertrend(
        d,
        10,
        3
    )

    last = d.iloc[-1]

    historical_cmp = safe_float(
        last["Close"]
    )

    current = get_current_price(
        symbol,
        daily_raw
    )

    cmp = (
        current["price"]
        if current["price"] > 0
        else historical_cmp
    )

    if cmp <= 0:

        return {
            "symbol": symbol,
            "error":
                "Price unavailable"
        }

    # ========================================================
    # EMA
    # ========================================================

    ema10 = safe_float(last["EMA10"])
    ema20 = safe_float(last["EMA20"])
    ema30 = safe_float(last["EMA30"])
    ema40 = safe_float(last["EMA40"])
    ema50 = safe_float(last["EMA50"])
    ema100 = safe_float(last["EMA100"])
    ema200 = safe_float(last["EMA200"])

    rsi = safe_float(
        last["RSI14"]
    )

    macd = safe_float(
        last["MACD"]
    )

    macd_signal = safe_float(
        last["MACD_SIGNAL"]
    )

    atr = safe_float(
        last["ATR14"]
    )

    volume_ratio = safe_float(
        last["VOL_RATIO"]
    )

    high52 = safe_float(
        last["HIGH52"]
    )

    low52 = safe_float(
        last["LOW52"]
    )

    # ========================================================
    # EMA ALIGNMENT
    # ========================================================

    ema_alignment = (
        cmp >
        ema10 >
        ema20 >
        ema30 >
        ema40 >
        ema50
    )

    ema_bull_stack = (
        ema10 >
        ema20 >
        ema30 >
        ema40 >
        ema50
    )

    # ========================================================
    # CPR
    # ========================================================

    pivot, cpr_low, cpr_high = (
        calculate_cpr(
            daily_raw
        )
    )

    cpr_bullish = (
        cmp > cpr_high
    )

    # ========================================================
    # MACD
    # ========================================================

    macd_bull = (
        macd > macd_signal
    )

    # ========================================================
    # SUPERTREND
    # ========================================================

    supertrend_bull = (
        safe_float(
            last["SUPERTREND_DIR"]
        ) > 0
    )

    # ========================================================
    # SWING LEVELS
    # ========================================================

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

    # ========================================================
    # BREAKOUT + RETEST
    # ========================================================

    breakout_level = max(
        recent_swing_high,
        cpr_high
    )

    price_breakout = (
        cmp > breakout_level
    )

    volume_confirmed = (
        volume_ratio >= 2
    )

    # Recent bars used for retest
    retest_window = d.tail(10)

    retest_touched = (
        retest_window["Low"]
        <= breakout_level * 1.015
    ).any()

    retest_holding = (
        cmp > breakout_level
        and
        recent_swing_low >=
        breakout_level * 0.97
    )

    breakout_confirmations = sum([
        price_breakout,
        ema_alignment,
        rsi >= 60,
        macd_bull,
        supertrend_bull,
        cpr_bullish,
        volume_confirmed
    ])

    breakout_confirmed = (
        price_breakout
        and breakout_confirmations >= 6
    )

    retest_confirmed = (
        breakout_confirmed
        and retest_touched
        and retest_holding
    )

    # ========================================================
    # MOMENTUM
    # ========================================================

    early_momentum = (
        cmp > ema20
        and rsi >= 55
        and macd_bull
        and volume_ratio >= 1.2
    )

    momentum_score = round(
        np.clip(
            ((rsi - 40) * 1.5)
            +
            min(volume_ratio, 3) * 12,
            0,
            100
        )
    )

    # ========================================================
    # TECHNICAL SCORE
    # ========================================================

    technical_checks = [
        cmp > ema10,
        cmp > ema20,
        cmp > ema30,
        cmp > ema40,
        cmp > ema50,
        cmp > ema200,
        rsi >= 50,
        macd_bull,
        supertrend_bull,
        volume_ratio >= 1.2
    ]

    technical_score = round(
        sum(technical_checks)
        /
        len(technical_checks)
        * 100
    )

    # ========================================================
    # RISK
    # ========================================================

    volatility_pct = (
        atr / cmp * 100
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

    # ========================================================
    # D/W/M
    # ========================================================

    weekly = daily_raw.resample(
        "W-FRI"
    ).agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum"
    }).dropna()

    try:

        monthly = daily_raw.resample(
            "ME"
        ).agg({
            "Open": "first",
            "High": "max",
            "Low": "min",
            "Close": "last",
            "Volume": "sum"
        }).dropna()

    except Exception:

        monthly = daily_raw.resample(
            "M"
        ).agg({
            "Open": "first",
            "High": "max",
            "Low": "min",
            "Close": "last",
            "Volume": "sum"
        }).dropna()

    d_tf = timeframe_score(
        daily_raw
    )

    w_tf = timeframe_score(
        weekly
    )

    m_tf = timeframe_score(
        monthly
    )

    dwm_score = round(
        (
            d_tf["score"]
            +
            w_tf["score"]
            +
            m_tf["score"]
        ) / 3
    )

    # ========================================================
    # SUPPORT / RESISTANCE
    # ========================================================

    support_candidates = [
        ema20,
        ema30,
        ema50,
        cpr_low,
        recent_swing_low
    ]

    valid_supports = [
        x for x in support_candidates
        if x > 0
    ]

    support = max(
        min(valid_supports)
        if valid_supports
        else cmp * .95,
        cmp * .50
    )

    resistance = max(
        recent_swing_high,
        cpr_high,
        ema50
    )

    # ========================================================
    # EXIT + STOP
    # ========================================================

    exit_price = min(
        [
            x for x in [
                ema50,
                support,
                cmp * .95
            ]
            if x > 0
        ],
        default=cmp * .95
    )

    stop_candidates = [
        recent_swing_low -
        atr * .75,

        ema50 -
        atr * .75,

        cmp -
        atr * 1.25
    ]

    stop_loss = max(
        0,
        min(stop_candidates)
    )

    if stop_loss >= cmp:
        stop_loss = max(
            cmp * .90,
            cmp - atr
        )

    # ========================================================
    # BUY ZONES
    # ========================================================

    buy_zone_low = max(
        0,
        min(
            support,
            cmp - atr * .75
        )
    )

    buy_zone_high = min(
        cmp,
        max(
            buy_zone_low,
            support + atr * .50
        )
    )

    dip_zone_low = max(
        0,
        ema50 - atr
    )

    dip_zone_high = max(
        dip_zone_low,
        ema50 + atr * .25
    )

    # ========================================================
    # BREAKOUT ENTRY
    # ========================================================

    breakout_entry = max(
        cmp + atr * .10,
        breakout_level + atr * .10
    )

    # ========================================================
    # SWING TARGET ENGINE
    # ALWAYS ABOVE CMP
    # ========================================================

    reference_high = max(
        resistance,
        recent_swing_high,
        high52,
        cmp
    )

    swing_t1 = max(
        cmp * 1.03,
        reference_high * 1.03,
        cmp + atr * .75
    )

    swing_t2 = max(
        swing_t1 + atr * .75,
        reference_high * 1.08,
        cmp * 1.08
    )

    swing_t3 = max(
        swing_t2 + atr,
        reference_high * 1.15,
        cmp * 1.15
    )

    swing_t1 = round(
        swing_t1,
        2
    )

    swing_t2 = round(
        max(
            swing_t2,
            swing_t1 + .01
        ),
        2
    )

    swing_t3 = round(
        max(
            swing_t3,
            swing_t2 + .01
        ),
        2
    )

    # ========================================================
    # LONG TERM TARGETS
    # ========================================================

    long_reference = max(
        high52,
        recent_swing_high,
        resistance,
        cmp
    )

    long_t1 = max(
        cmp * 1.15,
        long_reference + atr * 1.5
    )

    long_t2 = max(
        cmp * 1.25,
        long_reference + atr * 3.5
    )

    long_t3 = max(
        cmp * 1.40,
        long_reference + atr * 6
    )

    long_t1 = round(
        long_t1,
        2
    )

    long_t2 = round(
        max(
            long_t2,
            long_t1 + .01
        ),
        2
    )

    long_t3 = round(
        max(
            long_t3,
            long_t2 + .01
        ),
        2
    )

    # ========================================================
    # EMS V3
    # ========================================================

    ath_profit = (
        cmp >= high52 * .90
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
        sum(ems_checks)
        /
        len(ems_checks)
        * 100
    )

    if ems_score >= 75:
        ems_decision = "ADD"

    elif ems_score >= 55:
        ems_decision = "HOLD"

    elif ems_score >= 40:
        ems_decision = "REDUCE"

    else:
        ems_decision = "EXIT"

    # ========================================================
    # BULL / PIG / BEAR
    # ========================================================

    bull_points = sum([
        ema_alignment,
        rsi >= 55,
        macd_bull,
        w_tf["score"] >= 60,
        m_tf["score"] >= 55,
        momentum_score >= 60,
        supertrend_bull
    ])

    bear_points = sum([
        cmp < ema50,
        rsi < 45,
        not macd_bull,
        w_tf["score"] < 45,
        m_tf["score"] < 45,
        momentum_score < 35,
        not supertrend_bull
    ])

    if bull_points >= 5:
        regime = "BULL"

    elif bear_points >= 5:
        regime = "BEAR"

    else:
        regime = "PIG"

    # ========================================================
    # FINAL SIGNAL
    # ========================================================

    if retest_confirmed:

        signal = "BREAKOUT + RETEST"
        signal_class = "breakout"

    elif breakout_confirmed:

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
    # RESULT
    # ========================================================

    return {

        "symbol": symbol,
        "ticker": ns_symbol(symbol),

        "cmp": cmp,
        "historical_cmp":
            historical_cmp,

        "price_source":
            current["source"],

        "price_timestamp":
            current["timestamp"],

        "date":
            daily_raw.index[-1],

        "signal":
            signal,

        "signal_class":
            signal_class,

        "regime":
            regime,

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

        # ----------------------------------------------------
        # EMA
        # ----------------------------------------------------

        "ema10": ema10,
        "ema20": ema20,
        "ema30": ema30,
        "ema40": ema40,
        "ema50": ema50,
        "ema100": ema100,
        "ema200": ema200,

        "ema_alignment":
            ema_alignment,

        "ema_bull_stack":
            ema_bull_stack,

        # ----------------------------------------------------
        # RSI / MACD / ST
        # ----------------------------------------------------

        "rsi": rsi,

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

        "macd": macd,
        "macd_signal": macd_signal,

        "macd_bull":
            macd_bull,

        "supertrend_bull":
            supertrend_bull,

        # ----------------------------------------------------
        # CPR
        # ----------------------------------------------------

        "pivot":
            pivot,

        "cpr_low":
            cpr_low,

        "cpr_high":
            cpr_high,

        "cpr_bullish":
            cpr_bullish,

        # ----------------------------------------------------
        # VOLUME
        # ----------------------------------------------------

        "volume_ratio":
            volume_ratio,

        "volume_confirmed":
            volume_confirmed,

        # ----------------------------------------------------
        # D/W/M
        # ----------------------------------------------------

        "d_tf": d_tf,
        "w_tf": w_tf,
        "m_tf": m_tf,
        "dwm_score": dwm_score,

        # ----------------------------------------------------
        # LEVELS
        # ----------------------------------------------------

        "support":
            support,

        "resistance":
            resistance,

        "recent_swing_high":
            recent_swing_high,

        "recent_swing_low":
            recent_swing_low,

        "high52":
            high52,

        "low52":
            low52,

        # ----------------------------------------------------
        # BREAKOUT
        # ----------------------------------------------------

        "breakout_level":
            breakout_level,

        "price_breakout":
            price_breakout,

        "breakout_confirmations":
            breakout_confirmations,

        "breakout_confirmed":
            breakout_confirmed,

        "retest_touched":
            retest_touched,

        "retest_holding":
            retest_holding,

        "retest_confirmed":
            retest_confirmed,

        # ----------------------------------------------------
        # MOMENTUM
        # ----------------------------------------------------

        "early_momentum":
            early_momentum,

        # ----------------------------------------------------
        # RISK / EMS
        # ----------------------------------------------------

        "atr":
            atr,

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

        # ----------------------------------------------------
        # TARGETS
        # ----------------------------------------------------

        "swing_t1":
            swing_t1,

        "swing_t2":
            swing_t2,

        "swing_t3":
            swing_t3,

        "swing_t1_upside":
            pct(swing_t1, cmp),

        "swing_t2_upside":
            pct(swing_t2, cmp),

        "swing_t3_upside":
            pct(swing_t3, cmp),

        "long_t1":
            long_t1,

        "long_t2":
            long_t2,

        "long_t3":
            long_t3,

        "long_t1_upside":
            pct(long_t1, cmp),

        "long_t2_upside":
            pct(long_t2, cmp),

        "long_t3_upside":
            pct(long_t3, cmp),

        # ----------------------------------------------------
        # EMS MODULES
        # ----------------------------------------------------

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

        "relative_strength":
            relative_strength,

        "risk_deterioration":
            risk_deterioration,

        "reference_match":
            reference_match,

        # ----------------------------------------------------
        # CHART DATA
        # ----------------------------------------------------

        "df":
            d.tail(400).copy()
    }


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">

<div class="hero-title">
🐂 RAJESH STOCK ANALYZER PRO V2.2
</div>

<div class="hero-sub">
NSE • Manual 1–15 Stocks • EMS V3 • D/W/M •
EMA 10/20/30/40/50 • CPR • Momentum •
Breakout + Retest • Swing + Long
</div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# SETTINGS
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
                "CURRENT*"
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
        )

st.caption(
    "🟢 Current/intraday Yahoo Finance attempt is used "
    "where available. If unavailable, EOD fallback is used. "
    "This is NOT an exchange-grade NSE real-time feed."
)


# ============================================================
# ADD STOCK
# ============================================================

st.subheader(
    "➕ ADD STOCK"
)

a1,a2 = st.columns(
    [4,1]
)

with a1:

    new_stock = st.text_input(
        "NSE Symbol",
        placeholder=
        "BEL, BSE, AIIL, RATNAVEER...",
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
            5,
            len(
                st.session_state.watchlist
            )
        )
    )

    for i, stock in enumerate(
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

                if stock in st.session_state.watchlist:

                    st.session_state.watchlist.remove(
                        stock
                    )

                # ONLY THIS STOCK CACHE
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

    stocks = list(
        st.session_state.watchlist
    )

    if not stocks:

        st.warning(
            "પહેલા stock add કરો."
        )

    else:

        progress = st.progress(
            0
        )

        for i, stock in enumerate(
            stocks
        ):

            try:

                result = analyze(
                    stock
                )

            except Exception as e:

                result = {
                    "symbol":
                        stock,
                    "error":
                        f"Analysis error: "
                        f"{str(e)[:160]}"
                }

            st.session_state.analysis_cache[
                stock
            ] = result

            progress.progress(
                int(
                    ((i + 1) /
                     len(stocks))
                    * 100
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
# RESULTS
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

        results.append(
            result
        )

    elif (
        result
        and
        "error" in result
    ):

        errors.append(
            result
        )


if errors:

    for error in errors:

        st.warning(
            f"⚠️ {error['symbol']}: "
            f"{error['error']}"
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
        "BREAKOUT + RETEST",
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

pig_count = sum(
    r["regime"] == "PIG"
    for r in results
)

bear_count = sum(
    r["regime"] == "BEAR"
    for r in results
)

dash = st.columns(7)

dashboard_metrics = [
    ("📊","ANALYZED",total),
    ("🟢","POSITIVE",positive),
    ("⚠️","RISK / EXIT",risk_exit),
    ("🧠","AVG EMS",f"{avg_ems}/100"),
    ("📈","AVG TECH",f"{avg_tech}/100"),
    ("🐂","BULL",bull_count),
    ("🐻","BEAR",bear_count)
]

for col,(icon,label,value) in zip(
    dash,
    dashboard_metrics
):

    with col:

        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-value">
                    {icon} {value}
                </div>
                <div class="metric-title">
                    {label}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# QUICK SUMMARY
# ============================================================

st.markdown(
    "### 📋 QUICK SUMMARY"
)

summary = []

for r in results:

    summary.append({

        "STOCK":
            r["symbol"],

        "REGIME":
            r["regime"],

        "SIGNAL":
            r["signal"],

        "CMP":
            round(r["cmp"],2),

        "EMS":
            r["ems_score"],

        "TECH":
            r["technical_score"],

        "MOM":
            r["momentum_score"],

        "D/W/M":
            r["dwm_score"],

        "RISK":
            r["risk_meter"],

        "SWING T1":
            round(r["swing_t1"],2),

        "T1 UPSIDE":
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
    "BREAKOUT + RETEST",
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
            if r["regime"] ==
            filter_signal
        ]

    else:

        display_results = [
            r for r in results
            if r["signal"] ==
            filter_signal
        ]


# ============================================================
# MAIN BOARD
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

    price_source = r[
        "price_source"
    ]

    source_class = (
        "live"
        if price_source in [
            "CURRENT",
            "INTRADAY"
        ]
        else "eod"
    )

    source_text = (
        "🟢 CURRENT"
        if price_source == "CURRENT"
        else
        "🟢 INTRADAY"
        if price_source == "INTRADAY"
        else
        "🟡 EOD FALLBACK"
    )

    # ========================================================
    # STOCK HEADER
    # ========================================================

    st.markdown(
        f"""
        <div class="stock-card">

            <h2>
            🏢 {r['symbol']}
            </h2>

            <div class="small">
            {r['ticker']} • NSE •
            Analysis: {r['date'].date()}
            </div>

            <div class="{source_class}">
            {source_text}
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
    # SCORE BOXES
    # ========================================================

    st.markdown(
        f"""
        <div class="metric-grid">

            <div class="metric-box">
                <div class="metric-title">CMP</div>
                <div class="metric-value">
                    ₹{r['cmp']:,.2f}
                </div>
            </div>

            <div class="metric-box">
                <div class="metric-title">EMS</div>
                <div class="metric-value">
                    {r['ems_score']}/100
                </div>
            </div>

            <div class="metric-box">
                <div class="metric-title">TECH</div>
                <div class="metric-value">
                    {r['technical_score']}/100
                </div>
            </div>

            <div class="metric-box">
                <div class="metric-title">MOMENTUM</div>
                <div class="metric-value">
                    {r['momentum_score']}/100
                </div>
            </div>

            <div class="metric-box">
                <div class="metric-title">D/W/M</div>
                <div class="metric-value">
                    {r['dwm_score']}/100
                </div>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # ========================================================
    # KEY INDICATORS — SQUARE BOXES
    # ========================================================

    st.markdown(
        "### 📊 KEY INDICATORS"
    )

    st.markdown(
        f"""
        <div class="square-grid">

            <div class="square-box">
                <div class="square-title">
                EMA 10
                </div>
                <div class="square-value">
                ₹{r['ema10']:,.2f}
                </div>
            </div>

            <div class="square-box">
                <div class="square-title">
                EMA 20
                </div>
                <div class="square-value">
                ₹{r['ema20']:,.2f}
                </div>
            </div>

            <div class="square-box">
                <div class="square-title">
                EMA 30
                </div>
                <div class="square-value">
                ₹{r['ema30']:,.2f}
                </div>
            </div>

            <div class="square-box">
                <div class="square-title">
                EMA 40
                </div>
                <div class="square-value">
                ₹{r['ema40']:,.2f}
                </div>
            </div>

            <div class="square-box">
                <div class="square-title">
                EMA 50
                </div>
                <div class="square-value">
                ₹{r['ema50']:,.2f}
                </div>
            </div>

            <div class="square-box">
                <div class="square-title">
                CPR
                </div>
                <div class="square-value">
                ₹{r['cpr_low']:,.0f}
                – ₹{r['cpr_high']:,.0f}
                </div>
            </div>

            <div class="square-box">
                <div class="square-title">
                RSI 14
                </div>
                <div class="square-value">
                {r['rsi']:.1f}
                </div>
            </div>

            <div class="square-box">
                <div class="square-title">
                MACD
                </div>
                <div class="square-value">
                {'🟢 BULL' if r['macd_bull'] else '🔴 BEAR'}
                </div>
            </div>

            <div class="square-box">
                <div class="square-title">
                SUPERTREND
                </div>
                <div class="square-value">
                {'🟢 BULL' if r['supertrend_bull'] else '🔴 BEAR'}
                </div>
            </div>

            <div class="square-box">
                <div class="square-title">
                VOLUME
                </div>
                <div class="square-value">
                {r['volume_ratio']:.2f}x
                </div>
            </div>

            <div class="square-box">
                <div class="square-title">
                52W HIGH
                </div>
                <div class="square-value">
                ₹{r['high52']:,.0f}
                </div>
            </div>

            <div class="square-box">
                <div class="square-title">
                BREAKOUT
                </div>
                <div class="square-value">
                {'🔥 YES' if r['breakout_confirmed'] else '🟡 WATCH'}
                </div>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # ========================================================
    # PRICE LEVELS
    # ========================================================

    st.markdown(
        "### 🎯 PRICE LEVELS"
    )

    p1,p2,p3,p4 = st.columns(4)

    with p1:

        st.markdown(
            f"""
            <div class="zone">
            <b>SUPPORT</b>
            <h3>₹{r['support']:,.2f}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    with p2:

        st.markdown(
            f"""
            <div class="zone">
            <b>RESISTANCE</b>
            <h3>₹{r['resistance']:,.2f}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    with p3:

        st.markdown(
            f"""
            <div class="zone">
            <b>SWING HIGH</b>
            <h3>₹{r['recent_swing_high']:,.2f}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    with p4:

        st.markdown(
            f"""
            <div class="zone">
            <b>52W HIGH</b>
            <h3>₹{r['high52']:,.2f}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ========================================================
    # ENTRY / RISK
    # ========================================================

    st.markdown(
        "### 🛡️ ENTRY + RISK"
    )

    e1,e2,e3,e4,e5 = st.columns(5)

    with e1:

        st.markdown(
            f"""
            <div class="zone">
            <b>🟢 BUY ZONE</b>
            <h3>
            ₹{r['buy_zone_low']:,.0f}
            – ₹{r['buy_zone_high']:,.0f}
            </h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    with e2:

        st.markdown(
            f"""
            <div class="zone">
            <b>🟢 BUY ON DIP</b>
            <h3>
            ₹{r['dip_zone_low']:,.0f}
            – ₹{r['dip_zone_high']:,.0f}
            </h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    with e3:

        st.markdown(
            f"""
            <div class="zone">
            <b>🚀 BREAKOUT ENTRY</b>
            <h3>
            ₹{r['breakout_entry']:,.2f}
            </h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    with e4:

        st.markdown(
            f"""
            <div class="risk">
            <b>EXIT PRICE</b>
            <h3>
            ₹{r['exit_price']:,.2f}
            </h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    with e5:

        st.markdown(
            f"""
            <div class="risk">
            <b>STOP LOSS</b>
            <h3>
            ₹{r['stop_loss']:,.2f}
            </h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ========================================================
    # SWING TARGETS
    # ========================================================

    st.markdown(
        "### 🎯 SWING TARGETS"
    )

    s1,s2,s3 = st.columns(3)

    swing_targets = [
        (
            s1,
            "SWING T1",
            r["swing_t1"],
            r["swing_t1_upside"]
        ),
        (
            s2,
            "SWING T2",
            r["swing_t2"],
            r["swing_t2_upside"]
        ),
        (
            s3,
            "SWING T3",
            r["swing_t3"],
            r["swing_t3_upside"]
        )
    ]

    for col,label,target,upside in swing_targets:

        with col:

            st.markdown(
                f"""
                <div class="target">
                <b>{label}</b>
                <h2>
                ₹{target:,.2f}
                </h2>
                <div class="upside">
                +{upside:.1f}% from CMP
                </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # ========================================================
    # LONG TARGETS
    # ========================================================

    st.markdown(
        "### 🏆 LONG-TERM TARGETS"
    )

    l1,l2,l3 = st.columns(3)

    long_targets = [
        (
            l1,
            "LONG T1",
            r["long_t1"],
            r["long_t1_upside"]
        ),
        (
            l2,
            "LONG T2",
            r["long_t2"],
            r["long_t2_upside"]
        ),
        (
            l3,
            "LONG T3",
            r["long_t3"],
            r["long_t3_upside"]
        )
    ]

    for col,label,target,upside in long_targets:

        with col:

            st.markdown(
                f"""
                <div class="target">
                <b>{label}</b>
                <h2>
                ₹{target:,.2f}
                </h2>
                <div class="upside">
                +{upside:.1f}% from CMP
                </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # ========================================================
    # BREAKOUT STATUS
    # ========================================================

    if r["retest_confirmed"]:

        st.markdown(
            """
            <div class="signal breakout">
            🔥 BREAKOUT + RETEST CONFIRMED
            </div>
            """,
            unsafe_allow_html=True
        )

    elif r["breakout_confirmed"]:

        st.markdown(
            """
            <div class="signal breakout">
            🚀 BREAKOUT CONFIRMED • RETEST WATCH
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.info(
            f"🚀 Breakout level: "
            f"₹{r['breakout_level']:,.2f} • "
            f"Confirmations: "
            f"{r['breakout_confirmations']}/7"
        )

    # ========================================================
    # CHART — MAIN BOARD
    # ========================================================

    st.markdown(
        "### 📈 PRICE + EMA CHART"
    )

    chart_df = r.get(
        "df",
        pd.DataFrame()
    )

    chart_columns = [
        "Close",
        "EMA20",
        "EMA50",
        "EMA200"
    ]

    available_columns = [
        col for col in chart_columns
        if col in chart_df.columns
    ]

    if (
        not chart_df.empty
        and available_columns
    ):

        safe_chart = (
            chart_df[
                available_columns
            ]
            .tail(300)
            .copy()
        )

        safe_chart = safe_chart.apply(
            pd.to_numeric,
            errors="coerce"
        )

        safe_chart = safe_chart.dropna(
            how="all"
        )

        if not safe_chart.empty:

            st.line_chart(
                safe_chart,
                height=350
            )

        else:

            st.info(
                "Chart data unavailable."
            )

    else:

        st.warning(
            "⚠️ Chart columns unavailable. "
            "Analysis ચાલુ છે; dashboard બંધ નહીં થાય."
        )

    # ========================================================
    # EMS + DWM
    # ========================================================

    c1,c2 = st.columns(2)

    with c1:

        st.markdown(
            "### 🧠 EMS V3"
        )

        ems_rows = [
            ("ATH Profit", r["ath_profit"]),
            ("Outperformance", r["outperformance"]),
            ("Above Exit", r["above_exit"]),
            ("Trend Breakdown", not r["trend_breakdown"]),
            ("Momentum", not r["momentum_breakdown"]),
            ("Support", not r["support_breakdown"]),
            ("Volume", r["volume_confirmed"]),
            ("Relative Strength", r["relative_strength"]),
            ("Risk Safe", not r["risk_deterioration"]),
            ("Reference Match", r["reference_match"])
        ]

        ems_df = pd.DataFrame({

            "MODULE":
                [x[0] for x in ems_rows],

            "STATUS":
                [
                    "🟢 YES"
                    if x[1]
                    else
                    "🔴 NO"
                    for x in ems_rows
                ]
        })

        st.dataframe(
            ems_df,
            use_container_width=True,
            hide_index=True
        )

        st.success(
            f"EMS {r['ems_score']}/100 • "
            f"{r['ems_decision']}"
        )

    with c2:

        st.markdown(
            "### 📊 D / W / M"
        )

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

    elif r["ema_bull_stack"]:

        reasons.append(
            "🟢 EMA bullish stack"
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

    if r["supertrend_bull"]:

        reasons.append(
            "✅ Supertrend bullish"
        )

    if r["volume_confirmed"]:

        reasons.append(
            "✅ Volume ≥ 2× average"
        )

    if r["breakout_confirmed"]:

        reasons.append(
            "🔥 Breakout confirmed"
        )

    if r["retest_confirmed"]:

        reasons.append(
            "🔥 Retest successfully holding"
        )

    if r["risk_meter"] in [
        "HIGH",
        "EXTREME"
    ]:

        reasons.append(
            "⚠️ Elevated volatility risk"
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
    "🐂 RAJESH STOCK ANALYZER PRO V2.2 • "
    "NSE Manual Analyzer • "
    "Research & decision-support tool. "
    "Not financial advice."
)
