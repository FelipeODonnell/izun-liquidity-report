import requests
import streamlit as st



url = "https://open-api-v4.coinglass.com/api/futures/supported-exchange-pairs"

headers = {
    "accept": "application/json",
    "CG-API-KEY": st.secrets["coinglass_api"]["api_key"]
}

response = requests.get(url, headers=headers)

print(response.text)

'''
Response Data

JSON

{
  "code": "0",
  "msg": "success",
  "data": {
    "Binance": [ // exchange name
      {
        "instrument_id": "BTCUSD_PERP",// futures pair
        "base_asset": "BTC",// base asset
        "quote_asset": "USD"// quote asset
      },
      {
        "instrument_id": "BTCUSD_250627",
        "base_asset": "BTC",
        "quote_asset": "USD"
      },
      ....
      ],
    "Bitget": [
      {
        "instrument_id": "BTCUSDT_UMCBL",
        "base_asset": "BTC",
        "quote_asset": "USDT"
      },
      {
        "instrument_id": "ETHUSDT_UMCBL",
        "base_asset": "ETH",
        "quote_asset": "USDT"
      },
      ...
      ]
      ...
   }
}


'''