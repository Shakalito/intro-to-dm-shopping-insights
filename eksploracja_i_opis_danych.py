import pandas as pd

arkusze = pd.read_excel('zakupy-online.xlsx', sheet_name=None, engine='openpyxl')
for nazwa, df_sheet in arkusze.items():
    print(f"Arkusz '{nazwa}': {df_sheet.shape[0]} wierszy, {df_sheet.shape[1]} kolumn")

df = pd.concat(arkusze.values(), ignore_index=True)

duplikaty = df[df.duplicated()]
print(f"Liczba powtarzających się rekordów: {duplikaty.shape[0]}")

df_clean = df[
    ~df['Invoice'].astype(str).str.startswith('C') &
    (df['Quantity'] > 0)
].copy()

df_clean['TotalPrice'] = df_clean['Quantity'] * df_clean['Price']

min_date = df_clean['InvoiceDate'].min()
max_date = df_clean['InvoiceDate'].max()
print(f"Zakres dat: {min_date} → {max_date}")

num_countries = df_clean['Country'].nunique()
countries = df_clean['Country'].unique()
print(f"Liczba krajów i wykrytych regionów: {num_countries}")
print(f"Lista krajów i wykrytych regionów: {countries}")

daily = (
    df_clean
    .set_index('InvoiceDate')
    .resample('D')
    .agg(
      LiczbaTransakcji=('Invoice','count'),
      Sprzedaz=('TotalPrice','sum')
    )
)
print("Sprzedaż dzienna (pierwsze dni):")
print(daily.head())

top_qty = (
    df_clean
    .groupby('Description')['Quantity']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
print("Najpopularniejsze produkty:")
print(top_qty)

top_rev = (
    df_clean
    .groupby('Description')['TotalPrice']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
print("Najbardziej dochodowe produkty:")
print(top_rev)
