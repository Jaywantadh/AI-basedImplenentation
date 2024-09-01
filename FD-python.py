from pymongo import MongoClient
import pandas as pd
import numpy as np


client = MongoClient('mongodb://your_mongo_uri')#yeh example uri hai tum apna daalo
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

df['amount'] = scaler(df['amount']) #ye sirf example hai it can be any data. 

df = pd.get_dummies(df, columns=['location'])

def detect_fraud_zscore(df, threshold=3):
    # Calculate Z-Score for the 'amount' column
    df['zscore'] = (df['amount'] - df['amount'].mean()) / df['amount'].std()

    # Flag transactions with a Z-Score above the threshold as fraudulent
    df['fraud'] = np.where(df['zscore'].abs() > threshold, 1, 0)
    
    return df

df = detect_fraud_zscore(df)


print(df[['amount', 'zscore', 'fraud']].head())
print(df[df['fraud'] == 1])  # View all flagged fraudulent transactions

# Save the results back to MongoDB if needed
collection.update_many({}, {"$set": {"fraud": 0}})  # Reset fraud flag
for index, row in df.iterrows():
    collection.update_one({"_id": row["_id"]}, {"$set": {"fraud": int(row['fraud'])}})

print("Fraud detection completed and results updated in MongoDB.")



