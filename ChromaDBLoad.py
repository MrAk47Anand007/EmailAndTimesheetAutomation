import json
import chromadb
import uuid

# Initialize the ChromaDB client
client = chromadb.PersistentClient()

# Create or get an existing collection in ChromaDB
collection = client.get_or_create_collection('status_updates')

# Confirm data insertion count
print("Total documents in collection:", collection.count())

# Example query for "Kubernetes"
query_result = collection.query(
    query_texts=["Kubernetes"],
    n_results=1  # Limit the number of results
)

# Check and print query results
if query_result["documents"][0]:
    print("Query results:", query_result)
else:
    print("No matching documents found.")
