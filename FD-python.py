from pymongo import MongoClient
import pandas as pd


client = MongoClient('mongodb://your_mongo_uri')
db = client['your_database_name']
collection = db['your_collection_name']


data = list(collection.find({}))

df = pd.DataFrame(data)

print(df.head())
print(df.info())

df.fillna(method='ffill', inplace=True)  

def scaler(data):
    data_min = data.min()
    data_max = data.max()

    if data_max == data_min:
        return [1.0] * len(data)

    scaled_series = (data - data_min) / (data_max - data_min)
    return scaled_series

df['amount'] = scaler(df['amount'])

df = pd.get_dummies(df, columns=['location'])



