import pandas as pd
from joblib import Memory
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

memory = Memory(location='cache_dir', verbose=0)

arkusze = pd.read_excel('zakupy-online.xlsx', sheet_name=None, engine='openpyxl')
df = pd.concat(arkusze.values(), ignore_index=True).head(2500)

df_clean = df[
    ~df['Invoice'].astype(str).str.startswith('C') &
    (df['Quantity'] > 0)
].copy()

@memory.cache
def przygotuj_transakcje(df):
    grouped = df.groupby('Invoice')['Description'].apply(list)
    return grouped.tolist()

transactions = przygotuj_transakcje(df_clean)

te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
df_trans = pd.DataFrame(te_ary, columns=te.columns_)

item_support = df_trans.mean().sort_values(ascending=False)
threshold_idx = int(len(item_support) * 0.2)
min_support = item_support.iloc[threshold_idx]
print(f"min_support (20% najpopularniejszych): {min_support:.4f}")

frequent_itemsets = apriori(
    df_trans,
    min_support=min_support,
    use_colnames=True
)
print("Zbiory częste (pierwsze 5):")
print(frequent_itemsets.sort_values('support', ascending=False).head())

rules = association_rules(
    frequent_itemsets,
    metric='confidence',
    min_threshold=0.7
)
print("Reguły asocjacyjne (pierwsze 5 wg lift):")
print(rules.sort_values('lift', ascending=False).head())
