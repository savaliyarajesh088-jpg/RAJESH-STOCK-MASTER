import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

# ============================================================
# 🐂 RAJESH STOCK ANALYZER PRO
# Exit-Matra Style • EMS • D/W/M • CPR • Breakout
# Swing + Long • Bull/Bear/Pig • Persistent Watchlist
# ============================================================

st.set_page_config(
    page_title="RAJESH STOCK ANALYZER PRO",
    page_icon="🐂",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# CSS — FULL COLOUR MOBILE-FIRST UI
# ============================================================

st.markdown("""
<style>
.stApp {
    background: #050505;
    color: #ffffff;
}

.block-container {
    max-width: 1450px;
    padding: 1rem 1rem 4rem 1rem;
}

h1,h2,h3,h4 {
    color: white !important;
}

.hero {
    background: linear-gradient(
        135deg,
        #111827,
        #1e1b4b,
        #312e81
    );
    border: 1px solid #6366f1;
    border-radius: 22px;
    padding: 22px;
    margin-bottom: 18px;
}

.stock-card {
    background: #0b1120;
    border: 1px solid #334155;
    border-radius: 20px;
    padding: 18px;
    margin: 10px 0 20px 0;
    box-shadow: 0 8px 30px rgba(0,0,0,.35);
}

.buy {
    background: linear-gradient(135deg,#15803d,#22c55e);
}

.buydip {
    background: linear-gradient(135deg,#166534,#16a34a);
}

.breakout {
    background: linear-gradient(135deg,#047857,#10b981);
}

.early {
    background: linear-gradient(135deg,#a16207,#f59e0b);
}

.hold {
    background: linear-gradient(135deg,#1d4ed8,#3b82f6);
}

.wait {
    background: linear-gradient(135deg,#a16207,#eab308);
    color:#111827 !important;
}

.reduce {
    background: linear-gradient(135deg,#c2410c,#f97316);
}

.exit {
    background: linear-gradient(135deg,#991b1b,#ef4444);
}

.signal {
    border-radius: 17px;
    padding: 16px;
    text-align: center;
    font-size: 26px;
    font-weight: 900;
    margin: 10px 0 18px 0;
    color: white;
    border: 1px solid rgba(255,255,255,.25);
}

.regime {
    display: inline-block;
    padding: 7px 14px;
    border-radius: 999px;
    font-size: 16px;
    font-weight: 900;
    margin: 4px;
}

.bull {
    background:#166534;
    color:#bbf7d0;
}

.bear {
    background:#991b1b;
    color:#fecaca;
}

.pig {
    background:#9a3412;
    color:#fed7aa;
}

.zone-box {
    background: linear-gradient(
        135deg,
        #172554,
        #1e3a8a
    );
    border:1px solid #3b82f6;
    border-radius:16px;
    padding:16px;
    margin:5px 0;
}

.target-box {
    background: linear-gradient(
        135deg,
        #052e16,
        #14532d
    );
    border:1px solid #22c55e;
    border-radius:16px;
    padding:16px;
    margin:5px 0;
}

.exit-box {
    background: linear-gradient(
        135deg,
        #450a0a,
        #7f1d1d
    );
    border:1px solid #ef4444;
    border-radius:16px;
    padding:16px;
    margin:5px 0;
}

.metric-box {
    background:#111827;
    border:1px solid #374151;
    border-radius:14px;
    padding:12px;
    text-align:center;
}

.small {
    font-size:13px;
    opacity:.75;
}

div[data-testid="stMetric"] {
    background:#111827;
    border-radius:13px;
    padding:8px;
}

.stButton button {
    border-radius:12px;
    font-weight:800;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE — PERSISTENT WATCHLIST
# ============================================================

if "watchlist" not in st.session_state:
    st.session_state.watchlist = ["CEMINDIA"]

if "analysis_cache" not in st.session_state:
    st.session_state.analysis_cache = {}

if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = None


# ============================================================
# HELPERS
# ============================================================

def ticker_name(symbol):
    symbol = str(symbol).strip().upper()

    if not symbol:
        return ""

    if symbol.endswith(".NS"):
        return symbol

    return symbol + ".NS"


def safe_float(value, default=0.0):
    try:
        value = float(value)

        if np.isfinite(value):
            return value

    except:
        pass

    return default


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

    return 100 - (
        100 / (1 + rs)
    )


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

        df[f"EMA{p}"] = (
            close.ewm(
                span=p,
                adjust=False
            ).mean()
        )

    df["RSI"] = calculate_rsi(
        close,
        14
    )

    ema12 = close.ewm(
        span=12,
        adjust=False
    ).mean()

    ema26 = close.ewm(
        span=26,
        adjust=False
    ).mean()

    df["MACD"] = ema12 - ema26

    df["MACD_SIGNAL"] = (
        df["MACD"].ewm(
            span=9,
            adjust=False
        ).mean()
    )

    df["ATR"] = calculate_atr(
        df,
        14
    )

    df["VOL_AVG20"] = (
        df["Volume"]
        .rolling(20)
        .mean()
    )

    df["VOL_RATIO"] = (
        df["Volume"] /
        df["VOL_AVG20"]
    )

    df["HIGH_52W"] = (
        close
        .rolling(252)
        .max()
    )

    df["LOW_52W"] = (
        close
        .rolling(252)
        .min()
    )

    return df


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


def timeframe_analysis(df):

    if df.empty:
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
        safe_float(last["MACD_SIGNAL"]),
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
# FETCH DATA
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

        if df.empty:
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
            "Volume",
        ]

        for col in required:

            if col not in df.columns:
                return None

        return df.dropna(
            subset=["Close"]
        )

    except:

        return None


# ============================================================
# ANALYSIS ENGINE
# ============================================================

def analyze(symbol):

    daily = download_stock(
        symbol
    )

    if daily is None or len(daily) < 220:

        return {
            "symbol":symbol,
            "error":
                "Insufficient market data"
        }

    d = add_indicators(
        daily
    )

    last = d.iloc[-1]

    cmp = safe_float(
        last["Close"]
    )

    ema10 = safe_float(
        last["EMA10"]
    )

    ema20 = safe_float(
        last["EMA20"]
    )

    ema50 = safe_float(
        last["EMA50"]
    )

    ema100 = safe_float(
        last["EMA100"]
    )

    ema200 = safe_float(
        last["EMA200"]
    )

    rsi = safe_float(
        last["RSI"]
    )

    macd = safe_float(
        last["MACD"]
    )

    macd_signal = safe_float(
        last["MACD_SIGNAL"]
    )

    atr = safe_float(
        last["ATR"]
    )

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
    # EMA
    # --------------------------------------------------------

    ema_alignment = (
        cmp >
        ema10 >
        ema20 >
        ema50 >
        ema100 >
        ema200
    )

    # --------------------------------------------------------
    # CPR
    # --------------------------------------------------------

    pivot, cpr_low, cpr_high = (
        calculate_cpr(daily)
    )

    # --------------------------------------------------------
    # MACD
    # --------------------------------------------------------

    macd_bull = (
        macd >
        macd_signal
    )

    # --------------------------------------------------------
    # SUPERTREND
    # simplified directional calculation
    # --------------------------------------------------------

    supertrend_bull = (
        cmp > ema20
        and cmp > ema50
    )

    # --------------------------------------------------------
    # BREAKOUT
    # --------------------------------------------------------

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
    # TECHNICAL SCORE
    # --------------------------------------------------------

    tech_checks = [

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
        sum(tech_checks) /
        len(tech_checks) *
        100
    )

    # --------------------------------------------------------
    # MOMENTUM SCORE
    # --------------------------------------------------------

    momentum_score = round(
        np.clip(
            (
                (rsi - 40) * 1.5
            )
            +
            min(
                vol_ratio,
                3
            ) * 12,
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
    # MULTI TIMEFRAME
    # --------------------------------------------------------

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

    d_tf = timeframe_analysis(
        daily
    )

    w_tf = timeframe_analysis(
        weekly
    )

    m_tf = timeframe_analysis(
        monthly
    )

    dwm_score = round(
        (
            d_tf["score"]
            + w_tf["score"]
            + m_tf["score"]
        ) / 3
    )

    # --------------------------------------------------------
    # ZONES
    # --------------------------------------------------------

    support = max(
        ema20,
        cpr_low
    )

    resistance = max(
        previous_20_high,
        cpr_high
    )

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

    breakout_entry = (
        previous_20_high
        + atr * .10
    )

    # --------------------------------------------------------
    # EXIT PRICE / SL
    # --------------------------------------------------------

    exit_price = max(
        ema50,
        support
    )

    stop_loss = max(
        0,
        support - atr * 1.5
    )

    # --------------------------------------------------------
    # SWING TARGETS
    # --------------------------------------------------------

    swing_t1 = (
        resistance + atr
    )

    swing_t2 = (
        resistance + atr * 2
    )

    swing_t3 = (
        resistance + atr * 3.5
    )

    # --------------------------------------------------------
    # LONG TARGETS
    # --------------------------------------------------------

    long_base = max(
        high52,
        resistance
    )

    long_t1 = (
        long_base + atr * 2
    )

    long_t2 = (
        long_base + atr * 4
    )

    long_t3 = (
        long_base + atr * 7
    )

    # --------------------------------------------------------
    # EMS
    # --------------------------------------------------------

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
        and w_tf["score"] >= 55
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

    # --------------------------------------------------------
    # BULL / BEAR / PIG
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # FINAL SIGNAL
    # --------------------------------------------------------

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
        technical_score >= 70
        and ems_score >= 60
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

    # --------------------------------------------------------
    # OUTCOME
    # --------------------------------------------------------

    difference = (
        ((cmp - exit_price) /
         exit_price) * 100
        if exit_price > 0
        else 0
    )

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    return {

        "symbol":symbol,
        "ticker":ticker_name(symbol),

        "cmp":cmp,

        "change":None,

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

        "volume_ratio":
            vol_ratio,

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
        "dwm_score":dwm_score,

        "pivot":pivot,
        "cpr_low":cpr_low,
        "cpr_high":cpr_high,

        "support":support,
        "resistance":resistance,

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

        "long_t1":
            long_t1,

        "long_t2":
            long_t2,

        "long_t3":
            long_t3,

        "high52":
            high52,

        "low52":
            low52,

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

        "difference":
            difference,

        "df":daily,
    }


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="hero">
<h1>🐂 RAJESH STOCK ANALYZER PRO</h1>
<p>
NSE • Manual Stock Analyzer • EMS • Exit Matra Zones •
D/W/M • CPR • Momentum • Breakout • Swing + Long
</p>
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

        if st.session_state.last_refresh:

            st.metric(
                "LAST ANALYSIS",
                st.session_state.last_refresh
            )

        else:

            st.metric(
                "LAST ANALYSIS",
                "—"
            )

    st.caption(
        "Yahoo Finance latest available data is used "
        "in this starter build. LIVE* is not an "
        "exchange-grade real-time feed."
    )


# ============================================================
# ADD STOCK
# ============================================================

st.subheader(
    "➕ ADD STOCK"
)

add1,add2 = st.columns(
    [4,1]
)

with add1:

    new_stock = st.text_input(
        "NSE Symbol",
        placeholder="Example: BEL, BSE, AIIL, CEMINDIA",
        label_visibility="collapsed"
    )

with add2:

    add_clicked = st.button(
        "➕ ADD",
        use_container_width=True
    )


if add_clicked:

    stock = new_stock.strip().upper()

    if not stock:

        st.warning(
            "Stock symbol નાખો."
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
# WATCHLIST REMOVE
# ============================================================

if st.session_state.watchlist:

    st.subheader(
        "📋 MY STOCKS"
    )

    remove_cols = st.columns(
        min(
            len(
                st.session_state.watchlist
            ),
            5
        )
    )

    for i, stock in enumerate(
        st.session_state.watchlist
    ):

        with remove_cols[
            i % len(remove_cols)
        ]:

            st.write(
                f"**{stock}**"
            )

            if st.button(
                f"✖ Remove {stock}",
                key=f"remove_{stock}",
                use_container_width=True
            ):

                st.session_state.watchlist.remove(
                    stock
                )

                # Remove only that stock's cache.
                st.session_state.analysis_cache.pop(
                    stock,
                    None
                )

                st.rerun()


# ============================================================
# ANALYZE CONTROLS
# ============================================================

st.divider()

a1,a2,a3 = st.columns(
    [2,1,1]
)

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
# RUN ANALYSIS
# ============================================================

if analyze_all:

    progress = st.progress(0)

    total = len(
        st.session_state.watchlist
    )

    for i, stock in enumerate(
        st.session_state.watchlist
    ):

        result = analyze(
            stock
        )

        st.session_state.analysis_cache[
            stock
        ] = result

        progress.progress(
            int(
                ((i + 1) / total)
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

for stock in (
    st.session_state.watchlist
):

    if stock in (
        st.session_state.analysis_cache
    ):

        result = (
            st.session_state
            .analysis_cache[stock]
        )

        if result:

            results.append(
                result
            )


if not results:

    st.info(
        "Stock add કરો અને "
        "**ANALYZE ALL** દબાવો."
    )

    st.stop()


# ============================================================
# DASHBOARD
# ============================================================

st.divider()

st.subheader(
    "🚦 SIGNAL DASHBOARD"
)

summary = []

for r in results:

    summary.append({

        "STOCK":
            r["symbol"],

        "SIGNAL":
            r["signal"],

        "REGIME":
            r["regime"],

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

    })


summary_df = pd.DataFrame(
    summary
)

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
    "EARLY MOMENTUM",
    "HOLD",
    "WAIT",
    "REDUCE",
    "SELL / EXIT",
]

filter_signal = st.selectbox(
    "🔎 SIGNAL FILTER",
    filter_options
)


display_results = results

if filter_signal != "ALL":

    if filter_signal == "EARLY MOMENTUM":

        display_results = [
            r for r in results
            if r["early_momentum"]
        ]

    else:

        display_results = [
            r for r in results
            if r["signal"] ==
            filter_signal
        ]


# ============================================================
# STOCK DETAIL
# ============================================================

for r in display_results:

    st.divider()

    # --------------------------------------------------------
    # REGIME
    # --------------------------------------------------------

    regime_class = {
        "BULL":"bull",
        "BEAR":"bear",
        "PIG":"pig",
    }.get(
        r["regime"],
        "pig"
    )

    st.markdown(
        f"""
        <div class="stock-card">

        <h2>🏢 {r['symbol']}</h2>

        <div class="small">
        {r['ticker']} • NSE •
        Latest available data:
        {r['date'].date()}
        </div>

        <div style="margin-top:10px">

        <span class="regime {regime_class}">
        {'🐂' if r['regime']=='BULL'
        else '🐻' if r['regime']=='BEAR'
        else '🐷'}
        {r['regime']}
        </span>

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
    # TOP METRICS
    # --------------------------------------------------------

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
        "RISK",
        r["risk_meter"]
    )

    # --------------------------------------------------------
    # EXIT MATRA STYLE SUMMARY
    # --------------------------------------------------------

    c1,c2,c3,c4 = st.columns(4)

    with c1:

        st.markdown(
            f"""
            <div class="zone-box">
            <b>ZONE</b><br>
            <h3>{r['regime']}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            f"""
            <div class="exit-box">
            <b>EXIT PRICE</b><br>
            <h3>₹{r['exit_price']:,.2f}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:

        st.markdown(
            f"""
            <div class="exit-box">
            <b>STOP LOSS</b><br>
            <h3>₹{r['stop_loss']:,.2f}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:

        st.markdown(
            f"""
            <div class="target-box">
            <b>EMS DECISION</b><br>
            <h3>{r['ems_decision']}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    # --------------------------------------------------------
    # TABS
    # --------------------------------------------------------

    tabs = st.tabs([
        "🎯 ZONES & TARGETS",
        "🧠 EMS",
        "📊 D/W/M",
        "🚀 BREAKOUT",
        "⚡ MOMENTUM",
        "📈 CHART",
    ])

    # ========================================================
    # ZONES
    # ========================================================

    with tabs[0]:

        z1,z2,z3 = st.columns(3)

        with z1:

            st.markdown(
                f"""
                <div class="zone-box">
                <h4>🟢 BUY ZONE</h4>
                <h3>
                ₹{r['buy_zone_low']:,.0f}
                –
                ₹{r['buy_zone_high']:,.0f}
                </h3>
                </div>
                """,
                unsafe_allow_html=True
            )

        with z2:

            st.markdown(
                f"""
                <div class="zone-box">
                <h4>🟢 BUY ON DIP</h4>
                <h3>
                ₹{r['dip_zone_low']:,.0f}
                –
                ₹{r['dip_zone_high']:,.0f}
                </h3>
                </div>
                """,
                unsafe_allow_html=True
            )

        with z3:

            st.markdown(
                f"""
                <div class="zone-box">
                <h4>🚀 BREAKOUT ENTRY</h4>
                <h3>
                ₹{r['breakout_entry']:,.0f}
                </h3>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            "### 🎯 Swing Targets"
        )

        s1,s2,s3 = st.columns(3)

        s1.metric(
            "SWING T1",
            f"₹{r['swing_t1']:,.0f}"
        )

        s2.metric(
            "SWING T2",
            f"₹{r['swing_t2']:,.0f}"
        )

        s3.metric(
            "SWING T3",
            f"₹{r['swing_t3']:,.0f}"
        )

        st.markdown(
            "### 🏆 Long-Term Targets"
        )

        l1,l2,l3 = st.columns(3)

        l1.metric(
            "LONG T1",
            f"₹{r['long_t1']:,.0f}"
        )

        l2.metric(
            "LONG T2",
            f"₹{r['long_t2']:,.0f}"
        )

        l3.metric(
            "LONG T3",
            f"₹{r['long_t3']:,.0f}"
        )

        st.info(
            f"Support ₹{r['support']:,.2f} | "
            f"Resistance ₹{r['resistance']:,.2f} | "
            f"CPR ₹{r['cpr_low']:,.2f}–₹{r['cpr_high']:,.2f} | "
            f"Pivot ₹{r['pivot']:,.2f}"
        )

    # ========================================================
    # EMS
    # ========================================================

    with tabs[1]:

        st.markdown(
            f"""
            <div class="signal hold">
            🧠 EMS SCORE {r['ems_score']}/100
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
                f"{'✅' if status else '❌'} "
                f"{name}"
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
    # CHART
    # ========================================================

    with tabs[5]:

        chart = r["df"][
            [
                "Close",
                "EMA10",
                "EMA20",
                "EMA50",
                "EMA200",
            ]
        ].tail(300)

        st.line_chart(
            chart,
            height=400
        )

    # ========================================================
    # WHY
    # ========================================================

    st.markdown(
        "### 🧠 WHY THIS SIGNAL?"
    )

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
            "🔥 Breakout confirmed by multiple indicators"
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
