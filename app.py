# app.py
import os
import time
import requests

# 🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧
# ここだけ編集！他は触らなくて大丈夫！
# 🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧

# 監視するコインと各コインの変動率（順番厳守！）
SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]  # 監視したいコインを追加
PERCENTAGES = [5, 7, 10]                     # 対応する変動率（%）

# ntfyの設定（トピック名を自由に）
NTFY_TOPIC = "mexc_price_alerts"

# 🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧
# ここまで編集！下のコードは触らないで！
# 🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧

# 初期設定（自動処理）
symbol_settings = {s: p for s, p in zip(SYMBOLS, PERCENTAGES)}
initial_prices = {symbol: None for symbol in SYMBOLS}

def get_price(symbol):
    try:
        url = f"https://api.mexc.com/api/v3/ticker/price?symbol={symbol}"
        response = requests.get(url)
        return float(response.json()['price'])  # 括弧修正
    except Exception as e:
        print(f"{symbol} の価格取得に失敗: {str(e)}")
        return None

def send_alert(message):
    try:
        requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data=message.encode('utf-8'),
            headers={
                "Title": "価格変動アラート！",
                "Priority": "urgent",
                "Tags": "warning"
            }
        )
    except Exception as e:
        print(f"通知送信失敗: {str(e)}")

def check_prices():
    for symbol in SYMBOLS:
        current_price = get_price(symbol)
        if current_price is None:
            continue
        
        if initial_prices[symbol] is None:
            initial_prices[symbol] = current_price
            print(f"{symbol} 初期価格設定: {current_price}")
            continue
            
        change = ((current_price - initial_prices[symbol]) / initial_prices[symbol]) * 100
        
        if abs(change) >= symbol_settings[symbol]:  # 修正済み
            msg = f"{symbol}\n現在: {current_price:.4f}\n変動: {change:.1f}%"
            send_alert(msg)
            print(f"アラート送信: {msg}")
            initial_prices[symbol] = current_price

if __name__ == "__main__":
    print("監視を開始します...")
    while True:
        check_prices()
        time.sleep(60)