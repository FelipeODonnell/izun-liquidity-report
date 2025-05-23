
import requests
import json
import pandas as pd
import os
from datetime import datetime
import pyarrow
import streamlit as st





url = "https://open-api-v4.coinglass.com/api/grayscale/holdings-list"

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
      "symbol": "ETH",                                  // Token symbol, 
      "primary_market_price": 29.89,                    // Price in the primary market 
      "secondary_market_price": 29.71,                  // Price in the secondary market 
      "premium_rate": -0.6,                             // Premium rate (%),
      "holdings_amount": 2630007.61026,                 // Current holding amount (in tokens)
      "holdings_usd": 4290752215.8347797,               // Total market value of holdings in USD
      "holdings_amount_change_30d": 0,                  // Change in holding amount over the past 30 days (in tokens)
      "holdings_amount_change_7d": 0,                   // Change in holding amount over the past 7 days (in tokens)
      "holdings_amount_change1d": 0,                    // Change in holding amount over the past 1 day (in tokens)
      "close_time": 1721422800000,                      // Market close timestamp (milliseconds)
      "update_time": 1745203812007                      // Data update timestamp (milliseconds)
    },
    {
      "symbol": "ETC",                                  // Token symbol, e.g., ETC = Ethereum Classic
      "primary_market_price": 11.99,                    // Price in the primary market
      "secondary_market_price": 6.63,                   // Price in the secondary market
      "premium_rate": -44.7,                            // Premium rate, currently at a significant discount
      "holdings_amount": 11181376.733556,               // Current holding amount (in tokens)
      "holdings_usd": 181440200.2554132,                // Total market value of holdings in USD
      "holdings_amount_change_30d": -20697.669828,      // Change in holding amount over the past 30 days
      "holdings_amount_change_7d": -4596.123672,        // Change in holding amount over the past 7 days
      "holdings_amount_change1d": 0,                    // Change in holding amount over the past 1 day
      "close_time": 1744923600000,                      // Market close timestamp
      "update_time": 1745203812168                      // Data update timestamp
    }
  ]
}

'''