# Useful helper script to "clean up" for specific use cases
# %%
import pandas as pd

df = pd.read_csv('data/final_inu_and_neko.csv')

# %%
pid_cols = (
    'Customer Name',
    'Address',
    'State',
    'Zip Code',
    'Email',
    'Phone',
)

df = df.drop(
    columns=list(pid_cols),
)

# %%
# Additional drops
cols_to_drop = (
    'Sales Total',
    'Total Order Amount',
)
    
df = df.drop(
    columns=list(cols_to_drop),
)

# %%
cols_rename = {
    'Order #': 'Order_Number',
    'Total Order Amount': 'Total_Order_Amount',
    'Customer ID': 'Customer_ID',
    'Product Name': 'Product_Name',
    'Sales Total': 'Sales_Total',
    'Product Category': 'Product_Category',
    'Product Line': 'Product_Line',
}

df = df.rename(columns=cols_rename,)

# %% [markdown]
# # Additional "Dirt"

# %%
# Missing "data"
missing_data_cols = dict(
    Product_Name=0.01,
    Product_Category=0.05,
    Product_Line=0.001,
)
col = 'Product_Line'


for col,percent in missing_data_cols.items():
    missing_idx = (
        df[col]
        .sample(
            int(len(df) * percent),
            random_state=27,
        )
        .index
    )
    df.loc[missing_idx, col] = pd.NA

# %% [markdown]
# # Subset of data

# %%
df_subset = df.sample(300, random_state=27)

# %% [markdown]
# # Save data

# %%
df.to_csv('transactions-pet_store.csv', index=False)
df_subset.to_csv('transactions-pet_store-small.csv', index=False)