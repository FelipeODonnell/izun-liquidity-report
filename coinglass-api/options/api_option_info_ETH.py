
import requests
import json
import pandas as pd
import os
from datetime import datetime
import pyarrow
import streamlit as st





url = "https://open-api-v4.coinglass.com/api/option/info?symbol=ETH&start_time=1731498631418&end_time=1747133431418"

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
  "data": [
    {
      "exchange_name": "All",                           // Exchange name
      "open_interest": 361038.78,                       // Open interest (contracts)
      "oi_market_share": 100,                           // Market share (%)
      "open_interest_change_24h": 2.72,                 // 24h open interest change (%)
      "open_interest_usd": 31623069708.138245,          // Open interest value (USD)
      "volume_usd_24h": 2764676957.0569425,             // 24h trading volume (USD)
      "volume_change_percent_24h": 303.1                // 24h volume change (%)
    },
    {
      "exchange_name": "Deribit",                       // Exchange name
      "open_interest": 262641.9,                        // Open interest (contracts)
      "oi_market_share": 72.74,                         // Market share (%)
      "open_interest_change_24h": 2.57,                 // 24h open interest change (%)
      "open_interest_usd": 23005403973.349,             // Open interest value (USD)
      "volume_usd_24h": 2080336672.709                  // 24h trading volume (USD)
    }
  ]
}
Query Params
symbol
string
required
Defaults to BTC
Trading coin (e.g., BTC,ETH).

'''