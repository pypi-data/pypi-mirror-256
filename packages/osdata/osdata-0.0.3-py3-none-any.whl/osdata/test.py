from module import Datasets


ds = Datasets()

df = ds.load("public/logistics/c2k_data_comma.csv")

print(df.dtypes)
