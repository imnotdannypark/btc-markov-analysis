import pandas as pd
import numpy as np

np.random.seed(42)

# 1. Data Generation
# =====================
def generate_transactions(num_transactions=100000, num_wallets=1000, filename="bitcoin_data.csv"):
  wallets = [i for i in range(num_wallets)]
  exchanges = ["Coinbase", "inance", 'Kraken', 'Upbit', 'OKX']
  all_nodes = wallets + exchanges

  senders = np.random.choice(all_nodes, num_transactions)
  receivers = np.random.choice(all_nodes, num_transactions)

  # Create DataFrame
  data_frame = pd.DataFrame({'Sender_ID': senders, 'Receiver_ID': receivers, 'Amount_BTC': np.random.exponential(scale=0.5, size=num_transactions).round(4), 
                     'Timestamp': pd.date_range(start='2026-01-01', periods=num_transactions, freq='min')})

  # Delete self loop
  data_frame = data_frame[data_frame['Sender_ID'] != data_frame['Receiver_ID']]

  data_frame.to_csv(filename, index=False)
  return data_frame

# 2. Data Wrangling
# =====================
if __name__ == "__main__":
  df = generate_transactions()

  # Verified Data
  print(df.head(10))

