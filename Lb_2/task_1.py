import json
import requests

nbu_response = requests.get("https://bank.gov.ua/NBU_Exchange/exchange_site?start=20250325&end=20250409&valcode=eur&sort=exchangedate&order=asc&json")

converted_response = json.loads(nbu_response.content)

exchange_dates = []
exchange_rates = []

for item in converted_response:
    print("Date:", item["exchangedate"], " rate:", item["rate"])
    exchange_dates.append(item["exchangedate"])
    exchange_rates.append(item["rate"])

print("\nDates_massive:", exchange_dates, "\nRates_massive:", exchange_rates)

import matplotlib.pyplot as plt

plt.plot(exchange_dates, exchange_rates)
plt.show()
