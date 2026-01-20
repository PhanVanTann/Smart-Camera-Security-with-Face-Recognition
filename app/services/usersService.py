from core.mongodb import residents_collection
import numpy as np
class usersService:
    def __init__(self):
        self.users_collection = residents_collection
    def getListUsers(self):
        users = {}
        for user in self.users_collection.find({}):
            name = user.get("last_name", "N/A") + " " + user.get("first_name", "N/A")
            address = user.get("address", "N/A")
            user['id'] = str(user['_id'])
            for embedding in user.get("embeddings", []):
                vector = embedding.get("vector", [])
                if vector is None:
                    continue
                emb = np.array(vector, dtype=np.float32)
                users[name] = {
                    "address": address,
                    "age":user['age'],
                    "id": user['id'],
                    "embedding_vector": emb
                }
        return users