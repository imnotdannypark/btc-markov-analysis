import pandas as pd
import numpy as np

np.random.seed(42)

# 1. Data Generation
# =====================
def generate_transactions(num_transactions=100000, num_wallets=1000, filename="bitcoin_data.csv"):
  wallets = [f"Wallet_{i}" for i in range(num_wallets)]
  exchanges = ["Coinbase", "Binance", 'Kraken', 'Upbit', 'OKX']
  all_nodes = wallets + exchanges

  wallet_weights = np.random.pareto(a=3.0, size=len(wallets))
  exchange_weights = np.random.uniform(low=np.max(wallet_weights) * 25, high=np.max(wallet_weights) * 100, size=len(exchanges))

  all_weights = np.concatenate([wallet_weights, exchange_weights])
  all_weights /= all_weights.sum()

  senders = np.random.choice(all_nodes, size=num_transactions, p=all_weights)
  receivers = np.random.choice(all_nodes, size=num_transactions, p=all_weights)

  # Create DataFrame
  data_frame = pd.DataFrame({'Sender_ID': senders, 'Receiver_ID': receivers, 'Amount_BTC': np.random.exponential(scale=0.5, size=num_transactions).round(4), 
                     'Timestamp': pd.date_range(start='2026-01-01', periods=num_transactions, freq='min')})

  # Return non self-loops
  data_frame = data_frame[data_frame['Sender_ID'] != data_frame['Receiver_ID']].reset_index(drop=True)

  data_frame.to_csv(filename, index=False)
  return data_frame

# 2. Data Wrangling
# =====================
def build_transition_matrix(df):
  transaction_counts = pd.crosstab(df['Sender_ID'], df['Receiver_ID'])

  # Reindex to make a Square
  all_unique_nodes = sorted(list(set(df['Sender_ID']) | set(df['Receiver_ID'])))
  transaction_counts = transaction_counts.reindex(index=all_unique_nodes, columns=all_unique_nodes, fill_value=0).astype(float)

  # Normalize to Probability
  row_sums = transaction_counts.sum(axis=1) # sum = 1
  transition_probability = transaction_counts.div(row_sums.replace(0, 1), axis=0)

  return transition_probability, list(transition_probability.columns)

# 3. Markov Chain Analysis
# =====================
def stationary(P, alpha=0.85, total=1e-12, max_iterator=10000):
  n = P.shape[0]
  P_matrix = P.values

  dangling = (P_matrix.sum(axis=1) == 0).astype(float)

  v = np.ones(n) / n
  pi = np.ones(n) / n

  for _ in range(max_iterator):
    dangling_contribute = (pi * dangling).sum()
    pi_next = alpha * (pi.dot(P_matrix) + dangling_contribute * v) + (1 - alpha) * v

    if np.linalg.norm(pi_next - pi, 1) < total:
      pi = pi_next
      break
    
    pi = pi_next

  pi /= pi.sum()

  return pi

# 4. Plot
# =====================
import matplotlib.pyplot as plt

def make_plot(alphas, matrix, nodes, head_num=10):
  fig, ax = plt.subplots(1, 1, figsize=(16, 8))

  for a in alphas:
    p = stationary(matrix, alpha=a)

    res_df = pd.DataFrame({'Node Name': nodes, 'Probability': p})
    res_df['Influence(%)'] = res_df['Probability'] * 100
    res_df = res_df.sort_values('Influence(%)', ascending=False).reset_index(drop=True)
    res_head = res_df.head(head_num).copy()
    ax.plot(range(1, len(res_head)+1), res_head['Influence(%)'], marker='s', linestyle='-', label=f"alpha={a}")

  ax.set_xlabel("Rank (1 = hightes influence)")
  ax.set_ylabel('Influence(%)')
  ax.set_title(f"Top 10 node influence by alpha")
  ax.legend()
  ax.grid(True)
  plt.tight_layout()

  return fig, ax

# 5. Main Execution
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
  print(f"Only Sender: {len(just_send)}") # I can calculate active users are 781 ppl. Therefore, inactive users are 73 ppl.

  # Step 2: Build Matrix
  matrix, nodes = build_transition_matrix(df)
  print(f"\nMatrix Shape: {matrix.shape}")
  print(f"\n")

  # Step 3: Analysis
  steady_state = stationary(matrix, alpha=0.85)

  print(steady_state.sum())
  print(f"\n")

  # Step 4: Result
  result_df = pd.DataFrame({'Node Name': nodes, 'Probability': steady_state})
  result_df = result_df.sort_values(by='Probability', ascending=False).reset_index(drop=True)

  result_df['Rank'] = result_df.index + 1

  result_df['Influence(%)'] = (result_df['Probability'] * 100).round(4)

  print(result_df[['Rank', 'Node Name', 'Influence(%)']].head(10).to_string(index=False))

  # Step 5: Plot
  fig, ax = make_plot([0.75, 0.85, 0.95], matrix, nodes, head_num=10)
  plt.show()
