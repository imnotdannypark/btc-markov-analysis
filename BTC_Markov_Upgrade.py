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
def build_transition_matrix(df):
  transaction_counts = pd.crosstab(df['Sender_ID'], df['Receiver_ID'])

  # Reindex to make a Square
  all_unique_nodes = sorted(list(set(df['Sender_ID']) | set(df['Receiver_ID'])))
  transaction_counts = transaction_counts.reindex(index=all_unique_nodes, columns=all_unique_nodes, fill_value=0)

  # Normalize to Probability
  row_sums = transaction_counts.sum(axis=1) # sum = 1
  transition_probability = transaction_counts.div(row_sums, axis=0).fillna(0)

  return transition_probability, list(transition_probability.columns)

# ?. Main Execution
# =====================
if __name__ == "__main__":
  # Step 1: Generate Data
  df = generate_transactions()

  # Verified Data
  print(df.head(10))
  print(df.info())
  print(df.nunique())

  top_senders = df['Sender_ID'].value_counts(normalize=True).head(10).sum()
  print(f"Top 10 Senders: {top_senders}")

  just_send = set(df['Sender_ID']) - set(df['Receiver_ID'])
  print(f"Only Sender: {len(just_send)}") # I can calculate active users are 943 ppl. Therefore, inactive users are 18 ppl.

  # Step 2: Build Matrix
  matrix, nodes = build_transition_matrix(df)
  print(f"\nMatrix Shape: {matrix.shape}")
