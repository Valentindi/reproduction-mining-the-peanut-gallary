import json
import pandas as pd
import random as rd
data_src = "data/amazon_preprocessed.csv"
data_sink = "data/amazon_sample.csv"

n_product = [ 50, 50, 201, 169, 100, 100, 100]
n_reviews = [ 110+29, 979+411, 842+173, 1410+251, 578+120,210+7, 719+81]
df = pd.read_csv(data_src)

print(len(df))
df = df.drop_duplicates(subset=["review_body", "review_headline"])
print(len(df))
dfs = []

for it, category in enumerate(df.product_category.unique()):
    df_category = pd.DataFrame()
    df_all_categorie =  df[df.product_category == category]
    product_ids = []
    print("======", it, "===", category, "======")
    while len(df_category) < n_reviews[it] or len(df_category) == len(df_all_categorie):
        product_id = rd.choice(df_all_categorie.product_id.to_list())
        if product_id in product_ids:
            continue

        df_product = df[df.product_id == product_id]
        df_category = pd.concat([df_category, df_product])
        print("category:", category, df_category.shape,  n_reviews[it])
    dfs.append(df_category)
df = pd.concat(dfs)
print("ready, shape", df.shape)

df.to_csv(data_sink)

print("ready")
