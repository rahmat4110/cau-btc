import time
import os
from fetcher import fetch_data
from strategy import check_strategy
from notifier import send_telegram_alert

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_TELEGRAM_CHAT_ID")

SYMBOLS = ["BTCUSD", "XAUUSD"]
CHECK_INTERVAL_SECONDS = 300  # Cek setiap 5 menit

def main():
    print("Bot Telegram Signal Alert berjalan...")
    print(f"Monitoring pair: {', '.join(SYMBOLS)}")

    while True:
        try:
            for symbol in SYMBOLS:
                print(f"Mengambil data untuk {symbol}...")
                df = fetch_data(symbol, period="5d", interval="15m")
                alert = check_strategy(df, symbol)

                if alert:
                    print(f"Sinyal ditemukan untuk {symbol}! Mengirim notifikasi...")
                    send_telegram_alert(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, alert)
                else:
                    print(f"Tidak ada sinyal untuk {symbol}.")

        except Exception as e:
            print(f"Error terjadi dalam loop: {e}")

        time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
