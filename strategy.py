import pandas as pd
import pandas_ta as ta

def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['EMA20'] = ta.ema(df['Close'], length=20)
    df['EMA50'] = ta.ema(df['Close'], length=50)
    df['RSI14'] = ta.rsi(df['Close'], length=14)
    return df

def is_bullish_engulfing(df: pd.DataFrame, idx: int = -1) -> bool:
    curr = df.iloc[idx]
    prev = df.iloc[idx - 1]
    return (prev['Close'] < prev['Open']) and (curr['Close'] > curr['Open']) and \
           (curr['Close'] >= prev['Open']) and (curr['Open'] <= prev['Close'])

def is_bearish_engulfing(df: pd.DataFrame, idx: int = -1) -> bool:
    curr = df.iloc[idx]
    prev = df.iloc[idx - 1]
    return (prev['Close'] > prev['Open']) and (curr['Close'] < curr['Open']) and \
           (curr['Open'] >= prev['Close']) and (curr['Close'] <= prev['Open'])

def is_hammer(df: pd.DataFrame, idx: int = -1) -> bool:
    curr = df.iloc[idx]
    body = abs(curr['Close'] - curr['Open'])
    lower_wick = min(curr['Close'], curr['Open']) - curr['Low']
    upper_wick = curr['High'] - max(curr['Close'], curr['Open'])
    return lower_wick >= 2 * body and upper_wick <= body

def is_shooting_star(df: pd.DataFrame, idx: int = -1) -> bool:
    curr = df.iloc[idx]
    body = abs(curr['Close'] - curr['Open'])
    lower_wick = min(curr['Close'], curr['Open']) - curr['Low']
    upper_wick = curr['High'] - max(curr['Close'], curr['Open'])
    return upper_wick >= 2 * body and lower_wick <= body

def check_strategy(df: pd.DataFrame, symbol: str) -> dict:
    if len(df) < 55:
        return None

    df = calculate_indicators(df)
    curr = df.iloc[-1]

    price = curr['Close']
    ema20 = curr['EMA20']
    ema50 = curr['EMA50']
    rsi = curr['RSI14']

    # Avoid overbought/oversold
    if rsi > 75 or rsi < 25:
        return None

    # Trend Filter
    is_bullish_trend = (price > ema20) and (ema20 > ema50)
    is_bearish_trend = (price < ema20) and (ema20 < ema50)

    # Momentum Filter
    is_bullish_momentum = 40 <= rsi <= 70
    is_bearish_momentum = 30 <= rsi <= 60

    # Pattern Trigger
    bull_pattern = is_bullish_engulfing(df) or is_hammer(df)
    bear_pattern = is_bearish_engulfing(df) or is_shooting_star(df)

    pip_size = 0.1 if "XAU" in symbol or "GC=F" in symbol else 1.0  # basic pip adjustment for GOLD vs BTC
    sl_pips = 70.0
    sl_distance = sl_pips * pip_size

    if is_bullish_trend and is_bullish_momentum and bull_pattern:
        entry = price
        sl = entry - sl_distance
        risk = entry - sl
        tp1 = entry + (1.5 * risk)
        tp2 = entry + (2.5 * risk)
        pattern_name = "Bullish Engulfing" if is_bullish_engulfing(df) else "Hammer"
        return {
            "type": "BUY",
            "symbol": symbol,
            "entry": entry,
            "sl": sl,
            "tp1": tp1,
            "tp2": tp2,
            "rsi": rsi,
            "pattern": pattern_name
        }

    elif is_bearish_trend and is_bearish_momentum and bear_pattern:
        entry = price
        sl = entry + sl_distance
        risk = sl - entry
        tp1 = entry - (1.5 * risk)
        tp2 = entry - (2.5 * risk)
        pattern_name = "Bearish Engulfing" if is_bearish_engulfing(df) else "Shooting Star"
        return {
            "type": "SELL",
            "symbol": symbol,
            "entry": entry,
            "sl": sl,
            "tp1": tp1,
            "tp2": tp2,
            "rsi": rsi,
            "pattern": pattern_name
        }

    return None
