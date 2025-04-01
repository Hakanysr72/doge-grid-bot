import os

API_KEY = os.environ.get("BINANCE_API_KEY")
API_SECRET = os.environ.get("BINANCE_API_SECRET")

print("----- API TEST -----")
print("API_KEY:", "VAR" if API_KEY else "YOK")
print("API_SECRET:", "VAR" if API_SECRET else "YOK")

if not API_KEY or not API_SECRET:
    print("API değişkenleri alınamıyor! Railway Variables kontrol et.")
else:
    print("API değişkenleri başarıyla alındı.")
