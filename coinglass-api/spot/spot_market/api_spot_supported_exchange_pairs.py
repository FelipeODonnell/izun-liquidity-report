
import requests
import json
import pandas as pd
import os
from datetime import datetime
import pyarrow
import streamlit as st





url = "https://open-api-v4.coinglass.com/api/spot/supported-exchange-pairs"

headers = {
    "accept": "application/json",
    "CG-API-KEY": st.secrets["coinglass_api"]["api_key"]
}

response = requests.get(url, headers=headers)

print(response.text)

# Save response data as parquet
try:
    # Parse JSON response
    response_data = json.loads(response.text)
    
    # Check if response contains data
    if response_data.get('code') == '0' and 'data' in response_data:
        # Convert to DataFrame
        df = pd.DataFrame(response_data['data'])
        
        # Get current date for folder name
        current_date = datetime.now().strftime('%Y%m%d')
        
        # Create directory structure if it doesn't exist
        # Use current API file path to determine output path
        api_path = os.path.dirname(os.path.abspath(__file__))
        relative_path = os.path.relpath(api_path, 'coinglass-api')
        output_dir = os.path.join('data', current_date, relative_path)
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename without timestamp
        base_filename = os.path.splitext(os.path.basename(__file__))[0]
        file_path = os.path.join(output_dir, f"{base_filename}.parquet")
        
        # Save as parquet
        df.to_parquet(file_path, index=False)
        print(f"Data saved to {file_path}")
except Exception as e:
    print(f"Error saving data: {e}")

'''

Response Data
JSON

{
  "code": "0",
  "msg": "success",
  "data": {
    "Binance": [ // exchange name
      {
        "instrument_id": "BTCUSD_USDT",// Spot pair
        "base_asset": "BTC",// base asset
        "quote_asset": "USDT"// quote asset
      },
      {
        "instrument_id": "ETHUSD_USDT",
        "base_asset": "ETH",
        "quote_asset": "USDT"
      },
      ....
      ],
    "Bitget": [
      {
        "instrument_id": "AAVE:USD",
        "base_asset": "AAVE",
        "quote_asset": "USD"
      },
      {
        "instrument_id": "ADAUSD",
        "base_asset": "ADA",
        "quote_asset": "USD"
      },
      ...
      ]
      ...
   }
}

'''