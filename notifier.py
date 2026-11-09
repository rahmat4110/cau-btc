import requests

def send_telegram_alert(token: str, chat_id: str, alert_data: dict):
    if not alert_data:
        return

    emoji = "🟢" if alert_data['type'] == "BUY" else "🔴"
    msg = (
        f"{emoji} *SIGNAL ALERT: {alert_data['symbol']}*\n\n"
        f"*Type:* {alert_data['type']}\n"
        f"*Pattern:* {alert_data['pattern']}\n"
        f"*Entry:* {alert_data['entry']:.2f}\n"
        f"*Stop Loss:* {alert_data['sl']:.2f} (70 pips)\n"
        f"*Take Profit 1 (1.5R):* {alert_data['tp1']:.2f}\n"
        f"*Take Profit 2 (2.5R):* {alert_data['tp2']:.2f}\n"
        f"*RSI (14):* {alert_data['rsi']:.2f}\n"
    )

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": msg,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print(f"Alert sent for {alert_data['symbol']}")
    except Exception as e:
        print(f"Failed to send telegram message: {e}")
