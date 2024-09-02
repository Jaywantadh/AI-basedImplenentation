from sklearn.neighbors import NearestNeighbors
import numpy as np

# Sample data: Freelancers' skills (1: Python, 2: React, etc.)
freelancers = np.array([[1, 0, 0], [0, 1, 0], [1, 1, 0]])
jobs = np.array([[1, 0, 0], [0, 1, 0]])

# Model
model = NearestNeighbors(n_neighbors=1)
model.fit(freelancers)

# Recommend job for the first freelancer
recommendations = model.kneighbors([freelancers[0]])
print("Recommended job index:", recommendations[1][0])
