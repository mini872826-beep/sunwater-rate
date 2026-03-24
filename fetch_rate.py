#!/usr/bin/env python3
import urllib.request, csv, json, datetime, io, sys
MULTIPLIER = 1.02
OUTPUT_FILE = "rate.json"
def fetch_cny_cash_sell():
    today = datetime.date.today().strftime("%Y-%m-%d")
    url = f"https://rate.bot.com.tw/xrt/flcsv/0/{today}/CNY"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read().decode("utf-8-sig")
    reader = csv.reader(io.StringIO(raw))
    for row in reader:
        if row and row[0].strip().upper() == "CNY":
            return float(row[11].strip()), today
    raise ValueError("找不到 CNY 資料")
def main():
    try:
        cash_sell, today = fetch_cny_cash_sell()
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr); sys.exit(1)
    diamond_rate = round(cash_sell * MULTIPLIER, 3)
    now_utc = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    now_tw = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
    data = {"date": today, "updated_at_utc": now_utc, "updated_at_tw": now_tw,
            "bot_cash_sell": cash_sell, "multiplier": MULTIPLIER, "diamond_rate": diamond_rate,
            "source": "台灣銀行牌告匯率 rate.bot.com.tw"}
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[OK] {today}  台銀現金賣出: {cash_sell}  鑽石比例: {diamond_rate}")
if __name__ == "__main__":
    main()
