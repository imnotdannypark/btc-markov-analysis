import pandas as pd
import numpy as np

np.random.seed(42)

# 1. Data Generation
# =====================
def generate_transactions(num_transactions=100000, num_wallets=1000, filename="bitcoin_data.csv"):
  wallets = [i for i in range(num_wallets)]
  exchanges = ["Coinbase", "inance", 'Kraken', 'Upbit', 'OKX']
  all_nodes = wallets + exchanges

  weight = np.random.pareto(a=1.2, size=len(all_nodes))
  weight /= weight.sum()

  senders = np.random.choice(all_nodes, size=num_transactions, p=weight)
  receivers = np.random.choice(all_nodes, size=num_transactions, p=weight)

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
  print(df.info())
  print(df.nunique())

  top_senders = df['Sender_ID'].value_counts(normalize=True).head(10).sum()
  print(top_senders)

  just_send = set(df['Sender_ID']) - set(df['Receiver_ID'])
  print(len(just_send)) # I can calculate active users are 943 ppl. Therefore, inactive users are 18 ppl.

