import requests
import json
import time
from datetime import datetime

def fetch_ppp():
    print("Fetching data from World Bank...")
    url = "https://api.worldbank.org/v2/country/all/indicator/PA.NUS.PPP?format=json&per_page=300&date=2022" #try changing to 2023
    
    try:
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            print(f"number of countries in ppp data = {len(data[1])}")
            # available_codes = set()
            # for entry in data[1]:
            #     if entry['value'] is not None:
            #         available_codes.add(entry['country']['id'])
            # print(f"Available country codes: {sorted(list(available_codes))}")

            ppp_data = {}
            for entry in data[1]:
                if entry['value'] is not None:
                    country_code = entry['country']['id']
                    ppp_value = entry['value']

                    country_mapping = {
                        'IN': 'IN',
                        'US': 'US',
                        'GB': 'GB',
                        'JP': 'JP',
                        'AU': 'AU',
                        'CA': 'CA',
                        'DE': 'DE',  #germany
                        'FR': 'FR',
                        'BR': 'BR'
                    }

                    if country_code in country_mapping:
                        ppp_data[country_mapping[country_code]] = ppp_value
            print(f"Successfully fetched PPP data for {len(ppp_data)} countries.")
            return ppp_data
        else:
            print(f"Failed to fetch PPP data: HTTP{r.status_code}")
            return _get_sample_ppp_data()
    except Exception as e:
        print(f"Error fetching PPP data: {e}")
        return _get_sample_ppp_data()
    
def fetch_exchange_rates():
    #returns a dictionary of currency codes and their exchange rates wrt USD
    print("Fetching current exchange rates...")
    url = "https://open.er-api.com/v6/latest/USD"

    try:
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            print(f"Successfully fetched exchange rates for {len(data['rates'])} currencies.")
            return data["rates"]
        else:
            print(f"Failed to fetch exchange rates: HTTP{r.status_code}")
            return _get_sample_exchange_rates()
    
    except Exception as e:
        print(f"Error fetching exchange rates: {e}")
        return _get_sample_exchange_rates()
    
def _get_sample_ppp_data():
    print("Using sample PPP data instead:")
    return{
        "USA": 1.0,
        "IND": 21.5,
        "GBR": 0.78,
        "JPN": 102.5,
        "AUS": 1.45,
        "CAN": 1.3,
        "EUR": 0.83,
        "CHN": 4.2,
        "DEU": 0.83,
        "FRA": 0.85,
        "BRA": 2.3
    }

def _get_sample_exchange_rates():
    print("Using sample exchange rates instead:")
    return{
        "USD": 1.0,
        "INR": 83.12,
        "GBP": 0.76,
        "JPY": 149.5,
        "AUD": 1.52,
        "CAD": 1.37,
        "EUR": 0.92,
        "CNY": 7.24,
        "BRL": 5.05
    }

def get_currency_code(country_code):
    currency_mapping = {
        "US": "USD",
        "IN": "INR",
        "GB": "GBP",
        "JP": "JPY",
        "AU": "AUD",
        "CA": "CAD",
        "DE": "EUR",  # Germany uses Euro
        "FR": "EUR",  # France uses Euro
        "CH": "CNY",
        "BR": "BRL"
    }
    return currency_mapping.get(country_code, country_code)

def calculate_ppp_equivalent(amount, source_country, target_country, ppp_data=None, exchange_rates=None):
    if ppp_data is None:
        ppp_data = fetch_ppp()
    
    if exchange_rates is None:
        exchange_rates = fetch_exchange_rates()

    source_currency = get_currency_code(source_country)
    target_currency = get_currency_code(target_country)

    if source_country not in ppp_data or target_country not in ppp_data:
        raise ValueError(f"PPP data not available for {source_country} or {target_country}")
    
    if source_currency not in exchange_rates or target_currency not in exchange_rates:
        raise ValueError(f"Exchange rates not available for {source_currency} or {target_currency}")
    
    usd_ppp_value = amount / ppp_data[source_country]
    target_ppp_value = usd_ppp_value*ppp_data[target_country]
    return target_ppp_value

def get_currency_symbol(country_code):
    currency_symbols = {
        "US": "$",
        "IN": "₹",
        "GB": "£",
        "JP": "¥",
        "AU": "A$",
        "CA": "C$",
        "DE": "€",
        "FR": "€",
        "CH": "¥",
        "BR": "R$"
    }
    return currency_symbols.get(country_code, "")

def main():
    print("\nPPP Comparison Tool")

    ppp_data = fetch_ppp()
    exchange_rates = fetch_exchange_rates()

    print("\nAvailable countries for comparison:")
    available_countries = [country for country in ppp_data.keys()]
    for i, country in enumerate(available_countries, 1):
        print((f"{i}. {country}"))

    while True:
        try:
            country_index = int(input("\nSelect a country number: ")) - 1
            if 0 <= country_index < len(available_countries):
                selected_country = available_countries[country_index]
                break
            else:
                print("invalid country index. Please try again.")
        except ValueError:
            print("please enter a valid number!")

    while True:
        try:
            country_index_2 = int(input("\nSelect second country (final result will be displayed in this country's currency): ")) - 1
            if 0 <= country_index_2 < len(available_countries):
                selected_country_2 = available_countries[country_index_2]
                break
            else:
                print("invalid country index. Please try again.")
        except ValueError:
            print("please enter a valid number!")

    while True:
        try:
            amount = float(input(f"\nEnter amount in ({get_currency_symbol(selected_country)}): "))
            if amount > 0:
                break
            else:
                print("Please enter a positive amount.")
        except ValueError:
            print("please enter a valid number!")

    try:
        equivalent_amount = calculate_ppp_equivalent(
            amount, selected_country, selected_country_2, ppp_data, exchange_rates
        )

        print("\nResults:")
        print(f"{get_currency_symbol(selected_country)}{amount:.2f} in {selected_country} has the purchasing power of:")
        print(f"{equivalent_amount:.2f} in {selected_country_2} (based on PPP)")

    except Exception as e:
        print(f"Error occurred while calculating PPP: {e}")

if __name__ == "__main__":
    main()
    




