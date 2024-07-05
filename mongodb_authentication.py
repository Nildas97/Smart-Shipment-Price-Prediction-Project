from pymongo import MongoClient

uri = "mongodb+srv://DN56palsuit:9QX0yLYA8STzMRa3@cluster0.17pa9ai.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)

try:
    # This forces a call to the server and should raise an error if the connection is not successful
    client.server_info()
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")