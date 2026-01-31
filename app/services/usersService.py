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
            user_id = str(user["_id"])

            if name not in users:
                users[name] = {
                    "address": address,
                    "age": user.get("age", "N/A"),
                    "id": user_id,
                    "embeddings": []  
                }

            for embedding in user.get("embeddings", []):
                vector = embedding.get("vector")
                if vector is None:
                    continue
                emb = np.array(vector, dtype=np.float32)
                users[name]["embeddings"].append(emb)

        return users