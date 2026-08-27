# ============================================================
# 🐂 BULL MASTER V3.6
# CELL — ZONE + EMA + EMS UPGRADE ENGINE
# ============================================================
# 🔒 V3.5 BASE PRESERVED
# ➕ EMA 10/20/50/100/200
# ➕ EMA ALIGNMENT
# ➕ ZONE ENGINE
# ➕ 3-PILLAR EMS
# ➕ SCORE 0–3
# ➕ ADD / HOLD / REPLACE / EXIT
# ============================================================

import pandas as pd
import numpy as np

print("=" * 90)
print("🐂 BULL MASTER V3.6 — ZONE + EMA + EMS UPGRADE")
print("=" * 90)


# ------------------------------------------------------------
# 1️⃣ SOURCE DATA — V3.5 COMPATIBILITY
# ------------------------------------------------------------

_SOURCE = None

for _name in [
    "CELL5_FINAL",
    "RS_DF",
    "CELL4_FINAL",
    "NSE_HISTORICAL_OHLCV_DF"
]:
    if _name in globals():
        _obj = globals()[_name]
        if isinstance(_obj, pd.DataFrame) and not _obj.empty:
            _SOURCE = _obj.copy()
            print(f"✅ SOURCE FOUND: {_name}")
            break

if _SOURCE is None:
    raise ValueError(
        "❌ V3.5 source DataFrame not found. "
        "Expected CELL5_FINAL / RS_DF / CELL4_FINAL / "
        "NSE_HISTORICAL_OHLCV_DF."
    )


# ------------------------------------------------------------
# 2️⃣ NORMALIZE COLUMN NAMES
# ------------------------------------------------------------

df = _SOURCE.copy()

df.columns = [
    str(c).strip().upper().replace(" ", "_")
    for c in df.columns
]

# Common aliases
_aliases = {
    "CLOSE_PRICE": "CLOSE",
    "CLOSING_PRICE": "CLOSE",
    "LAST_PRICE": "CLOSE",
    "LTP": "CLOSE",
    "CMP": "CLOSE",
    "SYMBOL_NAME": "SYMBOL",
    "TICKER": "SYMBOL",
    "STOCK": "SYMBOL",
    "STOCK_NAME": "SYMBOL",
}

for old, new in _aliases.items():
    if old in df.columns and new not in df.columns:
        df[new] = df[old]


# ------------------------------------------------------------
# 3️⃣ REQUIRED PRICE DATA
# ------------------------------------------------------------

if "CLOSE" not in df.columns:
    raise ValueError("❌ CLOSE price column not found.")

df["CLOSE"] = pd.to_numeric(df["CLOSE"], errors="coerce")

df = df.dropna(subset=["CLOSE"]).copy()


# ------------------------------------------------------------
# 4️⃣ EMA ENGINE
# ------------------------------------------------------------

df["EMA_10"]  = df["CLOSE"].ewm(span=10,  adjust=False).mean()
df["EMA_20"]  = df["CLOSE"].ewm(span=20,  adjust=False).mean()
df["EMA_50"]  = df["CLOSE"].ewm(span=50,  adjust=False).mean()
df["EMA_100"] = df["CLOSE"].ewm(span=100, adjust=False).mean()
df["EMA_200"] = df["CLOSE"].ewm(span=200, adjust=False).mean()


# ------------------------------------------------------------
# 5️⃣ EMA ALIGNMENT
# ------------------------------------------------------------

def ema_alignment(row):

    c   = row["CLOSE"]
    e10 = row["EMA_10"]
    e20 = row["EMA_20"]
    e50 = row["EMA_50"]
    e100 = row["EMA_100"]
    e200 = row["EMA_200"]

    if c > e10 > e20 > e50 > e100 > e200:
        return "BULLISH"

    if c < e10 < e20 < e50 < e100 < e200:
        return "BEARISH"

    return "MIXED"


df["EMA_ALIGNMENT"] = df.apply(ema_alignment, axis=1)


# ------------------------------------------------------------
# 6️⃣ PRICE VS EMA
# ------------------------------------------------------------

def price_vs_ema(row):

    c = row["CLOSE"]

    above = sum([
        c > row["EMA_10"],
        c > row["EMA_20"],
        c > row["EMA_50"],
        c > row["EMA_100"],
        c > row["EMA_200"]
    ])

    if above == 5:
        return "ABOVE_ALL"

    if above >= 3:
        return "ABOVE_MAJORITY"

    if above == 0:
        return "BELOW_ALL"

    return "MIXED"


df["PRICE_VS_EMA"] = df.apply(price_vs_ema, axis=1)


# ------------------------------------------------------------
# 7️⃣ EMA SCORE
# ------------------------------------------------------------

def ema_score(row):

    score = 0

    if row["CLOSE"] > row["EMA_10"]:
        score += 1

    if row["CLOSE"] > row["EMA_20"]:
        score += 1

    if row["CLOSE"] > row["EMA_50"]:
        score += 1

    if row["CLOSE"] > row["EMA_100"]:
        score += 1

    if row["CLOSE"] > row["EMA_200"]:
        score += 1

    return score


df["EMA_SCORE"] = df.apply(ema_score, axis=1)


# ------------------------------------------------------------
# 8️⃣ 52 WEEK HIGH / LOW
# ------------------------------------------------------------

df["52W_HIGH"] = df["CLOSE"].rolling(252, min_periods=1).max()
df["52W_LOW"]  = df["CLOSE"].rolling(252, min_periods=1).min()


# ------------------------------------------------------------
# 9️⃣ ATH PROFIT
# ------------------------------------------------------------

df["ATH_PROFIT"] = (
    df["CLOSE"] >= df["52W_HIGH"] * 0.90
)


# ------------------------------------------------------------
# 🔟 MOMENTUM / OUTPERFORMANCE
# ------------------------------------------------------------

if "RS_SCORE" in df.columns:

    df["RS_SCORE"] = pd.to_numeric(
        df["RS_SCORE"],
        errors="coerce"
    )

    df["OUTPERFORMANCE"] = df["RS_SCORE"] >= 60

elif "RELATIVE_STRENGTH" in df.columns:

    rs = pd.to_numeric(
        df["RELATIVE_STRENGTH"],
        errors="coerce"
    )

    df["OUTPERFORMANCE"] = rs >= 60

else:

    # EMA-based fallback
    df["OUTPERFORMANCE"] = (
        (df["EMA_10"] > df["EMA_20"]) &
        (df["EMA_20"] > df["EMA_50"])
    )


# ------------------------------------------------------------
# 1️⃣1️⃣ EXIT PRICE ENGINE
# ------------------------------------------------------------

# Existing V3.5 exit price preserved if available
_exit_candidates = [
    "EXIT_PRICE",
    "EMS_EXIT_PRICE",
    "EXIT",
]

_exit_found = None

for c in _exit_candidates:
    if c in df.columns:
        _exit_found = c
        break


if _exit_found is not None:

    df["EXIT_PRICE"] = pd.to_numeric(
        df[_exit_found],
        errors="coerce"
    )

else:

    # Conservative EMA-50 based fallback
    df["EXIT_PRICE"] = df["EMA_50"]


# ------------------------------------------------------------
# 1️⃣2️⃣ ABOVE EXIT PRICE
# ------------------------------------------------------------

df["ABOVE_EXIT_PRICE"] = (
    df["CLOSE"] > df["EXIT_PRICE"]
)


# ------------------------------------------------------------
# 1️⃣3️⃣ DIFFERENCE %
# ------------------------------------------------------------

df["DIFFERENCE_%"] = np.where(
    df["EXIT_PRICE"] > 0,
    ((df["CLOSE"] - df["EXIT_PRICE"])
     / df["EXIT_PRICE"]) * 100,
    np.nan
)


# ------------------------------------------------------------
# 1️⃣4️⃣ STOP LOSS
# ------------------------------------------------------------

df["STOP_LOSS"] = (
    df["EMA_50"] * 0.95
)


# ------------------------------------------------------------
# 1️⃣5️⃣ 3-PILLAR EMS
# ------------------------------------------------------------

df["PILLAR_ATH_PROFIT"] = df["ATH_PROFIT"]

df["PILLAR_OUTPERFORMANCE"] = (
    df["OUTPERFORMANCE"]
)

df["PILLAR_ABOVE_EXIT"] = (
    df["ABOVE_EXIT_PRICE"]
)


df["EMS_SCORE"] = (
    df["PILLAR_ATH_PROFIT"].astype(int)
    +
    df["PILLAR_OUTPERFORMANCE"].astype(int)
    +
    df["PILLAR_ABOVE_EXIT"].astype(int)
)


# ------------------------------------------------------------
# 1️⃣6️⃣ ZONE ENGINE
# ------------------------------------------------------------

def zone_engine(row):

    score = row["EMS_SCORE"]
    ema = row["EMA_ALIGNMENT"]

    if score >= 3 and ema == "BULLISH":
        return "BULL"

    if score == 0 and ema == "BEARISH":
        return "BEAR"

    if score == 1 and ema == "BEARISH":
        return "BEAR"

    return "PIG"


df["ZONE"] = df.apply(zone_engine, axis=1)


# ------------------------------------------------------------
# 1️⃣7️⃣ RISK METER
# ------------------------------------------------------------

def risk_meter(row):

    if row["ZONE"] == "BULL":

        if row["EMA_SCORE"] >= 4:
            return "LOW"

        return "MEDIUM"

    if row["ZONE"] == "BEAR":
        return "HIGH"

    return "LOW"


df["RISK_METER"] = df.apply(risk_meter, axis=1)


# ------------------------------------------------------------
# 1️⃣8️⃣ FINAL DECISION ENGINE
# ------------------------------------------------------------

def final_decision(row):

    score = row["EMS_SCORE"]
    zone = row["ZONE"]

    # 3/3 = ADD
    if score == 3 and zone == "BULL":
        return "ADD"

    # 2/3 = HOLD
    if score == 2:
        return "HOLD"

    # 1/3 = REPLACE
    if score == 1:
        return "REPLACE"

    # 0/3 = EXIT
    return "EXIT"


df["FINAL_DECISION"] = df.apply(
    final_decision,
    axis=1
)


# ------------------------------------------------------------
# 1️⃣9️⃣ RATING
# ------------------------------------------------------------

def rating_engine(row):

    if row["EMS_SCORE"] == 3:
        return "BULL"

    if row["EMS_SCORE"] == 2:
        return "BULLISH"

    if row["EMS_SCORE"] == 1:
        return "PIG"

    return "BEAR"


df["RATING"] = df.apply(
    rating_engine,
    axis=1
)


# ------------------------------------------------------------
# 2️⃣0️⃣ UPGRADE STATUS
# ------------------------------------------------------------

def upgrade_status(row):

    if row["EMA_ALIGNMENT"] == "BULLISH":
        return "UPGRADED"

    if row["EMA_ALIGNMENT"] == "BEARISH":
        return "DOWNGRADED"

    return "UNCHANGED"


df["UPGRADE_STATUS"] = df.apply(
    upgrade_status,
    axis=1
)


# ------------------------------------------------------------
# 2️⃣1️⃣ SIGNAL
# ------------------------------------------------------------

_signal_map = {
    "ADD": "🟢 ADD",
    "HOLD": "🔵 HOLD",
    "REPLACE": "🟠 REPLACE",
    "EXIT": "🔴 EXIT"
}

df["SIGNAL"] = df["FINAL_DECISION"].map(
    _signal_map
).fillna(df["FINAL_DECISION"])


# ------------------------------------------------------------
# 2️⃣2️⃣ FINAL MASTER SCORE
# ------------------------------------------------------------

df["MASTER_SCORE"] = (
    df["EMA_SCORE"] / 5 * 100
).round(1)


# ------------------------------------------------------------
# 2️⃣3️⃣ FINAL OUTPUT
# ------------------------------------------------------------

CELL6_FINAL = df.copy()

RS_DF = CELL6_FINAL.copy()


# ------------------------------------------------------------
# 2️⃣4️⃣ DISPLAY
# ------------------------------------------------------------

_display_cols = [
    c for c in [
        "SYMBOL",
        "CLOSE",

        "ZONE",
        "RATING",
        "EMS_SCORE",
        "FINAL_DECISION",

        "EMA_10",
        "EMA_20",
        "EMA_50",
        "EMA_100",
        "EMA_200",

        "EMA_ALIGNMENT",
        "PRICE_VS_EMA",
        "EMA_SCORE",

        "EXIT_PRICE",
        "STOP_LOSS",
        "DIFFERENCE_%",

        "RISK_METER",
        "UPGRADE_STATUS",

        "PILLAR_ATH_PROFIT",
        "PILLAR_OUTPERFORMANCE",
        "PILLAR_ABOVE_EXIT",

        "MASTER_SCORE",
        "SIGNAL"
    ]
    if c in CELL6_FINAL.columns
]


print("\n" + "=" * 90)
print("🐂 BULL MASTER V3.6 — FINAL ZONE / EMA / EMS RESULT")
print("=" * 90)

display(
    CELL6_FINAL[_display_cols]
    .tail(20)
    .reset_index(drop=True)
)

print("\n" + "=" * 90)
print("✅ V3.6 UPGRADE COMPLETE")
print("✅ EMA 10/20/50/100/200")
print("✅ EMA ALIGNMENT")
print("✅ ZONE ENGINE")
print("✅ 3-PILLAR EMS")
print("✅ SCORE 0–3")
print("✅ ADD / HOLD / REPLACE / EXIT")
print("✅ EXIT PRICE")
print("✅ STOP LOSS")
print("✅ RISK METER")
print("✅ V3.5 BASE PRESERVED")
print("=" * 90)
