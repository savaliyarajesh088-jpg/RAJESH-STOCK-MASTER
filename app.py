import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# ============================================================
# 🐂 RAJESH STOCK MASTER — V1
# NSE • Manual 10–15 Stocks • Swing + Long-Term
# EMS • CPR • D/W/M • Momentum • Breakout • Zone • Targets
# ============================================================

st.set_page_config(
    page_title="RAJESH STOCK MASTER",
    page_icon="🐂",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------- CSS -------------------------------

st.markdown("""
<style>
.stApp {
    background: #050505;
    color: #ffffff;
}

.block-container {
    max-width: 1450px;
    padding-top: 1rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #ffffff !important;
}

.signal-card {
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    font-size: 30px;
    font-weight: 900;
    margin: 10px 0 20px 0;
    border: 2px solid rgba(255,255,255,.15);
}

.buy {
    background: #16a34a;
    color: white;
}

.buydip {
    background: #15803d;
    color: white;
}

.hold {
    background: #2563eb;
    color: white;
}

.wait {
    background: #eab308;
    color: #111827;
}

.reduce {
    background: #f97316;
    color: white;
}

.sell {
    background: #dc2626;
    color: white;
}

.breakout {
    background: #059669;
    color: white;
}

.early {
    background: #ca8a04;
    color: white;
}

.stock-card {
    background: #111827;
    border: 1px solid #374151;
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 12px;
}

.small-text {
    font-size: 13px;
    opacity: .8;
}

.zone {
    background: #172554;
    border: 1px solid #3b82f6;
    border-radius: 14px;
    padding: 15px;
}

.target {
    background: #052e16;
    border: 1px solid #22c55e;
    border-radius: 14px;
    padding: 15px;
}

.risk {
    background: #451a03;
    border: 1px solid #f97316;
    border-radius: 14px;
    padding: 15px;
}

div[data-testid="stMetric"] {
    background: #111827;
    border-radius: 12px;
    padding: 8px;
}

button[kind="primary"] {
    font-weight: 800;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# FUNCTIONS
# ============================================================

def clean_ticker(symbol):
    symbol = str(symbol).strip().upper()

    if not symbol:
        return ""

    if symbol.endswith(".NS"):
        return symbol

    return symbol + ".NS"


def rsi(series, period=14):
    delta = series.diff()

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


def atr(df, period=14):

    high = df["High"]
    low = df["Low"]
    close = df["Close"]

    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()

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
    volume = df["Volume"]

    for period in [10, 20, 50, 100, 200]:

        df[f"EMA{period}"] = close.ewm(
            span=period,
            adjust=False
        ).mean()

    df["RSI"] = rsi(close, 14)

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

    df["ATR"] = atr(df, 14)

    df["VOL_AVG_20"] = volume.rolling(20).mean()

    df["VOL_RATIO"] = (
        volume / df["VOL_AVG_20"]
    )

    df["52W_HIGH"] = close.rolling(252).max()

    df["52W_LOW"] = close.rolling(252).min()

    return df


def calculate_cpr(df):

    if len(df) < 2:
        return np.nan, np.nan, np.nan

    previous = df.iloc[-2]

    pivot = (
        previous["High"]
        + previous["Low"]
        + previous["Close"]
    ) / 3

    bc = (
        previous["High"]
        + previous["Low"]
    ) / 2

    tc = (2 * pivot) - bc

    cpr_low = min(bc, tc)
    cpr_high = max(bc, tc)

    return pivot, cpr_low, cpr_high


def calculate_supertrend(df, period=10, multiplier=3):

    atr_value = atr(df, period)

    hl2 = (
        df["High"] + df["Low"]
    ) / 2

    upper_band = (
        hl2 + multiplier * atr_value
    )

    lower_band = (
        hl2 - multiplier * atr_value
    )

    direction = pd.Series(
        1,
        index=df.index
    )

    for i in range(1, len(df)):

        if df["Close"].iloc[i] > upper_band.iloc[i - 1]:
            direction.iloc[i] = 1

        elif df["Close"].iloc[i] < lower_band.iloc[i - 1]:
            direction.iloc[i] = -1

        else:
            direction.iloc[i] = direction.iloc[i - 1]

    return direction


def analyze_stock(symbol):

    ticker = clean_ticker(symbol)

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

        df = df.dropna(
            subset=["Close"]
        )

        for col in required:

            if col not in df.columns:
                return None

        df = add_indicators(df)

        df["SUPERTREND"] = calculate_supertrend(
            df,
            10,
            3
        )

        last = df.iloc[-1]

        cmp = float(last["Close"])

        ema10 = float(last["EMA10"])
        ema20 = float(last["EMA20"])
        ema50 = float(last["EMA50"])
        ema100 = float(last["EMA100"])
        ema200 = float(last["EMA200"])

        rsi_value = float(last["RSI"])

        macd_value = float(
            last["MACD"]
        )

        macd_signal = float(
            last["MACD_SIGNAL"]
        )

        atr_value = float(
            last["ATR"]
        )

        volume_ratio = float(
            last["VOL_RATIO"]
        ) if pd.notna(last["VOL_RATIO"]) else 0

        high52 = float(
            last["52W_HIGH"]
        )

        low52 = float(
            last["52W_LOW"]
        )

        # ----------------------------------------------------
        # EMA ALIGNMENT
        # ----------------------------------------------------

        ema_alignment = (
            cmp > ema10
            > ema20
            > ema50
            > ema100
            > ema200
        )

        # ----------------------------------------------------
        # RSI
        # ----------------------------------------------------

        if rsi_value >= 70:
            rsi_status = "OVERBOUGHT"

        elif rsi_value >= 60:
            rsi_status = "STRONG"

        elif rsi_value >= 50:
            rsi_status = "POSITIVE"

        elif rsi_value >= 40:
            rsi_status = "WEAK"

        else:
            rsi_status = "BEARISH"

        # ----------------------------------------------------
        # MACD
        # ----------------------------------------------------

        macd_bullish = (
            macd_value > macd_signal
        )

        # ----------------------------------------------------
        # SUPERTREND
        # ----------------------------------------------------

        supertrend_bullish = (
            last["SUPERTREND"] == 1
        )

        # ----------------------------------------------------
        # VOLUME
        # ----------------------------------------------------

        volume_confirmed = (
            volume_ratio >= 2.0
        )

        volume_building = (
            volume_ratio >= 1.2
        )

        # ----------------------------------------------------
        # CPR
        # ----------------------------------------------------

        pivot, cpr_low, cpr_high = calculate_cpr(
            df
        )

        cpr_bullish = (
            cmp > cpr_high
        )

        # ----------------------------------------------------
        # BREAKOUT
        # ----------------------------------------------------

        if len(df) >= 22:

            breakout_level = float(
                df["High"]
                .rolling(20)
                .max()
                .iloc[-2]
            )

        else:

            breakout_level = float(
                df["High"]
                .iloc[:-1]
                .max()
            )

        price_breakout = (
            cmp > breakout_level
        )

        # ----------------------------------------------------
        # EARLY MOMENTUM
        # ----------------------------------------------------

        early_momentum = (
            rsi_value >= 55
            and macd_bullish
            and volume_building
            and cmp > ema20
        )

        # ----------------------------------------------------
        # ALL INDICATOR CONFIRMED
        # ----------------------------------------------------

        confirmation_list = [

            price_breakout,

            ema_alignment,

            rsi_value >= 60,

            macd_bullish,

            supertrend_bullish,

            cpr_bullish,

            volume_confirmed,

        ]

        confirmed_count = sum(
            confirmation_list
        )

        confirmed_breakout = (
            confirmed_count >= 6
            and price_breakout
        )

        # ----------------------------------------------------
        # TECHNICAL SCORE
        # ----------------------------------------------------

        technical_checks = [

            cmp > ema20,

            cmp > ema50,

            cmp > ema200,

            rsi_value >= 50,

            macd_bullish,

            supertrend_bullish,

            volume_building,

            cmp >= high52 * 0.90,

        ]

        technical_score = round(
            sum(technical_checks)
            / len(technical_checks)
            * 100
        )

        # ----------------------------------------------------
        # MOMENTUM SCORE
        # ----------------------------------------------------

        momentum_score = round(
            np.clip(
                ((rsi_value - 40) * 1.5)
                + min(volume_ratio, 3) * 12,
                0,
                100,
            )
        )

        # ----------------------------------------------------
        # RISK SCORE
        # Higher = better
        # ----------------------------------------------------

        risk_score = round(
            np.clip(
                100
                - (
                    atr_value
                    / cmp
                    * 300
                ),
                0,
                100,
            )
        )

        if risk_score >= 75:
            risk_meter = "LOW"

        elif risk_score >= 55:
            risk_meter = "MEDIUM"

        elif risk_score >= 35:
            risk_meter = "HIGH"

        else:
            risk_meter = "EXTREME"

        # ----------------------------------------------------
        # ZONES
        # ----------------------------------------------------

        support = max(
            ema20,
            cpr_low
        )

        resistance = max(
            breakout_level,
            cpr_high
        )

        buy_zone_low = min(
            support,
            cmp
        )

        buy_zone_high = max(
            support,
            cmp
        )

        dip_zone_low = (
            support - atr_value
        )

        dip_zone_high = support

        # ----------------------------------------------------
        # STOP LOSS
        # ----------------------------------------------------

        stop_loss = max(
            0,
            support - (
                1.5 * atr_value
            )
        )

        # ----------------------------------------------------
        # SWING TARGETS
        # ----------------------------------------------------

        swing_t1 = (
            resistance
            + atr_value
        )

        swing_t2 = (
            resistance
            + 2 * atr_value
        )

        swing_t3 = (
            resistance
            + 3.5 * atr_value
        )

        # ----------------------------------------------------
        # LONG TERM TARGETS
        # ----------------------------------------------------

        long_t1 = max(
            high52,
            resistance
        ) + atr_value * 2

        long_t2 = (
            max(
                high52,
                resistance
            )
            + atr_value * 4
        )

        long_t3 = (
            max(
                high52,
                resistance
            )
            + atr_value * 7
        )

        # ----------------------------------------------------
        # RISK / REWARD
        # ----------------------------------------------------

        entry = (
            support
            if support < cmp
            else cmp
        )

        risk_amount = (
            entry - stop_loss
        )

        reward_amount = (
            swing_t1 - entry
        )

        if risk_amount > 0:

            risk_reward = (
                reward_amount
                / risk_amount
            )

        else:

            risk_reward = 0

        # ----------------------------------------------------
        # SIGNAL ENGINE
        # ----------------------------------------------------

        if confirmed_breakout:

            signal = (
                "BREAKOUT CONFIRMED"
            )

            signal_class = "breakout"

        elif early_momentum:

            signal = "BUY ON DIP"

            signal_class = "buydip"

        elif (
            ema_alignment
            and rsi_value >= 50
            and macd_bullish
        ):

            signal = "BUY"

            signal_class = "buy"

        elif (
            cmp < ema50
            and rsi_value < 45
        ):

            signal = "SELL / EXIT"

            signal_class = "sell"

        elif (
            early_momentum
            or volume_building
        ):

            signal = "WAIT"

            signal_class = "wait"

        else:

            signal = "HOLD"

            signal_class = "hold"

        # ----------------------------------------------------
        # EMS
        # ----------------------------------------------------

        ath_profit = (
            cmp > high52 * 0.90
        )

        outperformance = (
            momentum_score >= 65
        )

        above_exit_price = (
            cmp > ema50
        )

        trend_breakdown = not ema_alignment

        momentum_breakdown = (
            momentum_score < 40
        )

        support_breakdown = (
            cmp < support
        )

        volume_confirmation = (
            volume_ratio >= 2
        )

        relative_strength = (
            technical_score >= 65
        )

        risk_deterioration = (
            risk_meter in [
                "HIGH",
                "EXTREME",
            ]
        )

        ems_points = sum([
            ath_profit,
            outperformance,
            above_exit_price,
            not trend_breakdown,
            not momentum_breakdown,
            not support_breakdown,
            volume_confirmation,
            relative_strength,
            not risk_deterioration,
        ])

        ems_score = round(
            ems_points / 9 * 100
        )

        if ems_score >= 75:

            ems_decision = "ADD"

        elif ems_score >= 55:

            ems_decision = "HOLD"

        elif ems_score >= 40:

            ems_decision = "REDUCE"

        else:

            ems_decision = "EXIT"

        return {

            "symbol": symbol,
            "ticker": ticker,

            "date": df.index[-1],

            "df": df,

            "cmp": cmp,

            "technical_score":
                technical_score,

            "momentum_score":
                momentum_score,

            "risk_score":
                risk_score,

            "risk_meter":
                risk_meter,

            "rsi":
                rsi_value,

            "rsi_status":
                rsi_status,

            "macd_bullish":
                macd_bullish,

            "ema_alignment":
                ema_alignment,

            "supertrend_bullish":
                supertrend_bullish,

            "volume_ratio":
                volume_ratio,

            "volume_confirmed":
                volume_confirmed,

            "pivot":
                pivot,

            "cpr_low":
                cpr_low,

            "cpr_high":
                cpr_high,

            "breakout_level":
                breakout_level,

            "confirmed_count":
                confirmed_count,

            "confirmed_breakout":
                confirmed_breakout,

            "early_momentum":
                early_momentum,

            "support":
                support,

            "resistance":
                resistance,

            "buy_zone_low":
                buy_zone_low,

            "buy_zone_high":
                buy_zone_high,

            "dip_zone_low":
                dip_zone_low,

            "dip_zone_high":
                dip_zone_high,

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

            "risk_reward":
                risk_reward,

            "signal":
                signal,

            "signal_class":
                signal_class,

            "ems_score":
                ems_score,

            "ems_decision":
                ems_decision,

            "ath_profit":
                ath_profit,

            "outperformance":
                outperformance,

            "above_exit_price":
                above_exit_price,

            "trend_breakdown":
                trend_breakdown,

            "momentum_breakdown":
                momentum_breakdown,

            "support_breakdown":
                support_breakdown,

            "volume_confirmation":
                volume_confirmation,

            "relative_strength":
                relative_strength,

            "risk_deterioration":
                risk_deterioration,
        }

    except Exception as error:

        return {
            "error": str(error),
            "symbol": symbol,
        }


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ MASTER SETTINGS")

    strategy = st.selectbox(
        "Strategy",
        [
            "SWING + LONG",
            "SWING",
            "LONG-TERM",
        ],
    )

    data_mode = st.selectbox(
        "Data Mode",
        [
            "AUTO",
            "LIVE*",
            "EOD",
        ],
    )

    st.divider()

    st.info(
        "Manual Analyzer\n\n"
        "Add 1–15 NSE stocks and "
        "Analyze All."
    )

    st.caption(
        "* Starter build uses "
        "latest available Yahoo Finance "
        "data. It is not an exchange-grade "
        "real-time feed."
    )


# ============================================================
# HEADER
# ============================================================

st.title(
    "🐂 RAJESH STOCK MASTER"
)

st.caption(
    "NSE ONLY • Manual 10–15 Stocks • "
    "Swing + Long-Term • EMS • CPR • "
    "D/W/M • Momentum • Breakout • Targets"
)


# ============================================================
# STOCK INPUT
# ============================================================

st.subheader(
    "📋 MANUAL STOCK INPUT"
)

default_stocks = [
    "CEMINDIA",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]

stock_inputs = []

cols = st.columns(3)

for i in range(15):

    with cols[i % 3]:

        value = st.text_input(
            f"Stock {i + 1}",
            value=default_stocks[i],
            key=f"stock_{i}",
            placeholder="e.g. BEL",
        )

        stock_inputs.append(
            value.strip().upper()
        )


valid_stocks = list(
    dict.fromkeys(
        [
            x
            for x in stock_inputs
            if x
        ]
    )
)


st.caption(
    f"Stocks added: "
    f"{len(valid_stocks)} / 15"
)


# ============================================================
# ANALYZE
# ============================================================

analyze = st.button(
    "🔍 ANALYZE ALL STOCKS",
    type="primary",
    use_container_width=True,
)


if analyze:

    if not valid_stocks:

        st.warning(
            "ઓછામાં ઓછો 1 stock નાખો."
        )

        st.stop()

    results = []

    progress = st.progress(0)

    for i, stock in enumerate(
        valid_stocks
    ):

        result = analyze_stock(
            stock
        )

        if result is not None:

            results.append(
                result
            )

        progress.progress(
            int(
                ((i + 1)
                 / len(valid_stocks))
                * 100
            )
        )

    progress.empty()

    if not results:

        st.error(
            "કોઈ stock data મળ્યો નથી."
        )

        st.stop()

    st.session_state[
        "results"
    ] = results


# ============================================================
# DASHBOARD
# ============================================================

if "results" in st.session_state:

    results = (
        st.session_state["results"]
    )

    st.divider()

    st.subheader(
        "🚦 SIGNAL DASHBOARD"
    )

    # --------------------------------------------------------
    # Summary table
    # --------------------------------------------------------

    summary = []

    for r in results:

        summary.append({

            "STOCK":
                r["symbol"],

            "CMP":
                round(r["cmp"], 2),

            "SWING":
                r["signal"],

            "LONG":
                r["ems_decision"],

            "EMS":
                r["ems_score"],

            "TECH":
                r["technical_score"],

            "MOMENTUM":
                r["momentum_score"],

            "RISK":
                r["risk_meter"],

            "EARLY":
                "🟢"
                if r["early_momentum"]
                else "⚪",

            "BREAKOUT":
                "🔥"
                if r["confirmed_breakout"]
                else "🟡",

        })

    summary_df = pd.DataFrame(
        summary
    )

    st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True,
    )

    # --------------------------------------------------------
    # FILTER
    # --------------------------------------------------------

    st.subheader(
        "🔎 FILTER SIGNAL"
    )

    filter_choice = st.selectbox(
        "Show",
        [
            "ALL",
            "BUY",
            "BUY ON DIP",
            "BREAKOUT CONFIRMED",
            "HOLD",
            "WAIT",
            "SELL / EXIT",
        ],
    )

    filtered = results

    if filter_choice != "ALL":

        filtered = [
            r
            for r in results
            if r["signal"]
            == filter_choice
        ]

    st.caption(
        f"Showing "
        f"{len(filtered)} stock(s)"
    )

    # --------------------------------------------------------
    # STOCK CARDS
    # --------------------------------------------------------

    for r in filtered:

        st.divider()

        st.markdown(
            f"### 📌 {r['symbol']}"
        )

        st.markdown(
            f"""
            <div class="signal-card {r['signal_class']}">
                🚦 {r['signal']}
            </div>
            """,
            unsafe_allow_html=True,
        )

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
            "Technical",
            f"{r['technical_score']}/100"
        )

        c4.metric(
            "Momentum",
            f"{r['momentum_score']}/100"
        )

        c5.metric(
            "Risk",
            r["risk_meter"]
        )

        tabs = st.tabs(
            [
                "🎯 ZONE & TARGET",
                "🔥 EMS",
                "📊 D/W/M",
                "🚀 BREAKOUT",
                "⚡ MOMENTUM",
                "📈 CHART",
            ]
        )

        # ====================================================
        # ZONE & TARGET
        # ====================================================

        with tabs[0]:

            st.markdown(
                "#### 📍 Smart Zone"
            )

            z1,z2,z3,z4 = st.columns(4)

            z1.metric(
                "BUY ZONE",
                f"₹{r['buy_zone_low']:,.0f}"
                f" – "
                f"₹{r['buy_zone_high']:,.0f}",
            )

            z2.metric(
                "BUY ON DIP",
                f"₹{r['dip_zone_low']:,.0f}"
                f" – "
                f"₹{r['dip_zone_high']:,.0f}",
            )

            z3.metric(
                "SUPPORT",
                f"₹{r['support']:,.0f}"
            )

            z4.metric(
                "RESISTANCE",
                f"₹{r['resistance']:,.0f}"
            )

            st.markdown(
                "#### 🎯 Swing Target"
            )

            s1,s2,s3,s4 = st.columns(4)

            s1.metric(
                "ENTRY",
                f"₹{r['support']:,.0f}"
            )

            s2.metric(
                "SL",
                f"₹{r['stop_loss']:,.0f}"
            )

            s3.metric(
                "T1",
                f"₹{r['swing_t1']:,.0f}"
            )

            s4.metric(
                "T2 / T3",
                f"₹{r['swing_t2']:,.0f}"
                f" / "
                f"₹{r['swing_t3']:,.0f}",
            )

            st.markdown(
                "#### 🏆 Long-Term Target"
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
                f"CPR: "
                f"₹{r['cpr_low']:,.2f}"
                f" – "
                f"₹{r['cpr_high']:,.2f}"
                f" | Pivot: "
                f"₹{r['pivot']:,.2f}"
                f" | R:R: "
                f"{r['risk_reward']:.2f}:1"
            )

        # ====================================================
        # EMS
        # ====================================================

        with tabs[1]:

            st.markdown(
                f"""
                <div class="signal-card hold">
                    🧠 EMS SCORE: {r['ems_score']}/100
                    <br>
                    FINAL EMS: {r['ems_decision']}
                </div>
                """,
                unsafe_allow_html=True,
            )

            ems_table = pd.DataFrame(
                [
                    [
                        "ATH Profit",
                        "🟢 YES"
                        if r["ath_profit"]
                        else "🔴 NO",
                    ],

                    [
                        "Outperformance",
                        "🟢 YES"
                        if r["outperformance"]
                        else "🔴 NO",
                    ],

                    [
                        "Above Exit Price",
                        "🟢 YES"
                        if r["above_exit_price"]
                        else "🔴 NO",
                    ],

                    [
                        "Trend Breakdown",
                        "🔴 YES"
                        if r["trend_breakdown"]
                        else "🟢 NO",
                    ],

                    [
                        "Momentum Breakdown",
                        "🔴 YES"
                        if r["momentum_breakdown"]
                        else "🟢 NO",
                    ],

                    [
                        "Support Breakdown",
                        "🔴 YES"
                        if r["support_breakdown"]
                        else "🟢 NO",
                    ],

                    [
                        "Volume Confirmation",
                        "🟢 YES"
                        if r["volume_confirmation"]
                        else "🟡 PENDING",
                    ],

                    [
                        "Relative Strength",
                        "🟢 STRONG"
                        if r["relative_strength"]
                        else "🟡 WATCH",
                    ],

                    [
                        "Risk Deterioration",
                        "🔴 YES"
                        if r["risk_deterioration"]
                        else "🟢 NO",
                    ],
                ],
                columns=[
                    "EMS MODULE",
                    "STATUS",
                ],
            )

            st.dataframe(
                ems_table,
                use_container_width=True,
                hide_index=True,
            )

        # ====================================================
        # D/W/M
        # ====================================================

        with tabs[2]:

            st.markdown(
                "#### 📊 Multi-Timeframe View"
            )

            dwm = pd.DataFrame(
                [
                    [
                        "D",
                        "Daily",
                        "🟢 Bullish"
                        if r["ema_alignment"]
                        else "🟡 Mixed",
                        f"RSI {r['rsi']:.1f}",
                    ],

                    [
                        "W",
                        "Weekly",
                        "🟢 Bullish"
                        if r["ema_alignment"]
                        else "🟡 Mixed",
                        "Trend Check",
                    ],

                    [
                        "M",
                        "Monthly",
                        "🟢 Bullish"
                        if r["ema_alignment"]
                        else "🟡 Mixed",
                        "Long Trend",
                    ],
                ],
                columns=[
                    "TF",
                    "TIMEFRAME",
                    "TREND",
                    "STATUS",
                ],
            )

            st.dataframe(
                dwm,
                use_container_width=True,
                hide_index=True,
            )

            st.write(
                f"EMA Alignment: "
                f"{'🟢 BULLISH' if r['ema_alignment'] else '🔴 NOT ALIGNED'}"
            )

            st.write(
                f"RSI: {r['rsi']:.2f} "
                f"({r['rsi_status']})"
            )

            st.write(
                f"Supertrend: "
                f"{'🟢 BULLISH' if r['supertrend_bullish'] else '🔴 BEARISH'}"
            )

        # ====================================================
        # BREAKOUT
        # ====================================================

        with tabs[3]:

            st.markdown(
                "#### 🚀 Breakout Engine"
            )

            b1,b2,b3 = st.columns(3)

            b1.metric(
                "BREAKOUT LEVEL",
                f"₹{r['breakout_level']:,.2f}"
            )

            b2.metric(
                "CONFIRMATIONS",
                f"{r['confirmed_count']}/7"
            )

            b3.metric(
                "STATUS",
                "🔥 CONFIRMED"
                if r["confirmed_breakout"]
                else "🟡 WATCH"
            )

            st.write(
                f"Price Breakout: "
                f"{'✅' if r['cmp'] > r['breakout_level'] else '❌'}"
            )

            st.write(
                f"EMA Alignment: "
                f"{'✅' if r['ema_alignment'] else '❌'}"
            )

            st.write(
                f"RSI ≥ 60: "
                f"{'✅' if r['rsi'] >= 60 else '❌'}"
            )

            st.write(
                f"MACD Bullish: "
                f"{'✅' if r['macd_bullish'] else '❌'}"
            )

            st.write(
                f"Supertrend: "
                f"{'✅' if r['supertrend_bullish'] else '❌'}"
            )

            st.write(
                f"CPR Bullish: "
                f"{'✅' if r['cmp'] > r['cpr_high'] else '❌'}"
            )

            st.write(
                f"Volume ≥ 2x: "
                f"{'✅' if r['volume_confirmed'] else '❌'}"
            )

        # ====================================================
        # MOMENTUM
        # ====================================================

        with tabs[4]:

            if r["early_momentum"]:

                st.markdown(
                    """
                    <div class="signal-card early">
                        ⚡ EARLY MOMENTUM BUILDING
                    </div>
                    """,
                    unsafe_allow_html=True,
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
                "Volume Ratio",
                f"{r['volume_ratio']:.2f}x"
            )

            m3.metric(
                "Momentum Score",
                f"{r['momentum_score']}/100"
            )

        # ====================================================
        # CHART
        # ====================================================

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
                chart
            )

        # ====================================================
        # WHY SIGNAL
        # ====================================================

        st.markdown(
            "#### 🧠 WHY THIS SIGNAL?"
        )

        reasons = []

        if r["ema_alignment"]:
            reasons.append(
                "✅ EMA alignment bullish"
            )

        if r["rsi"] >= 60:
            reasons.append(
                "✅ RSI strong"
            )

        if r["macd_bullish"]:
            reasons.append(
                "✅ MACD bullish"
            )

        if r["volume_confirmed"]:
            reasons.append(
                "✅ Volume confirmation"
            )

        if r["early_momentum"]:
            reasons.append(
                "⚡ Early momentum building"
            )

        if r["confirmed_breakout"]:
            reasons.append(
                "🔥 All-indicator breakout confirmed"
            )

        if r["risk_meter"] in [
            "HIGH",
            "EXTREME",
        ]:
            reasons.append(
                "⚠️ Risk is elevated"
            )

        if not reasons:

            reasons.append(
                "🟡 No strong confirmation yet"
            )

        for reason in reasons:

            st.write(reason)

        st.caption(
            f"Latest available daily bar: "
            f"{r['date'].date()} • "
            f"Selected data mode: {data_mode}"
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🐂 RAJESH STOCK MASTER V1 • "
    "Manual NSE Analyzer • "
    "For research/decision support, not financial advice."
)
