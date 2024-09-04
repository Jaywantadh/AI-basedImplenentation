import pymongo
import numpy as np
from sklearn.neighbors import NearestNeighbors

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['freelance_platform']
users_collection = db['users']
jobs_collection = db['jobs']

def fetch_user_data():
    users = users_collection.find({})
    user_data = []
    user_ids = []
    
    for user in users:
        # Example features (jaise ki job views, applications, skills) 
        features = {
            'viewed_jobs': len(user['behavior']['viewed_jobs']),
            'applied_jobs': len(user['behavior']['applied_jobs']),
            'skills_count': len(user['skills']),
            # Add more features as needed
        }
        user_data.append(list(features.values()))
        user_ids.append(user['_id'])
    
    return np.array(user_data), user_ids

user_data, user_ids = fetch_user_data()

# Train KNN model
def train_knn_model(user_data, n_neighbors=5):
    knn = NearestNeighbors(n_neighbors=n_neighbors)
    knn.fit(user_data)
    return knn

knn_model = train_knn_model(user_data)

def recommend_jobs(user_id):
    
    user_index = user_ids.index(user_id)
    user_vector = user_data[user_index].reshape(1, -1)
    
   
    distances, indices = knn_model.kneighbors(user_vector)
    
    
    recommended_jobs = set()
    
    for idx in indices.flatten():
        neighbor_id = user_ids[idx]
        neighbor_data = users_collection.find_one({"_id": neighbor_id})
        recommended_jobs.update(neighbor_data['behavior']['viewed_jobs'])
    
    
    return list(recommended_jobs)

# Example usage
user_id = "some_user_id"  # Replace with an actual user ID
recommended_jobs = recommend_jobs(user_id)
print(f"Recommended jobs for user {user_id}: {recommended_jobs}")
