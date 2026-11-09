import yfinance as yf
import pandas as pd

def fetch_data(symbol: str, period: str = "7d", interval: str = "15m") -> pd.DataFrame:
    """
    Mengambil data OHLCV menggunakan yfinance.
    Symbol mapping:
    - BTCUSD -> BTC-USD
    - XAUUSD -> GC=F (Gold Futures) atau XAUUSD=X
    """
    symbol_map = {
        "BTCUSD": "BTC-USD",
        "XAUUSD": "GC=F"  # Alternatif: "XAUUSD=X"
    }

    target_symbol = symbol_map.get(symbol.upper(), symbol)
    df = yf.download(tickers=target_symbol, period=period, interval=interval, progress=False)

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    return df
