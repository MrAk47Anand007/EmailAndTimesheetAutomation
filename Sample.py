import json
import chromadb
import uuid

# Initialize the ChromaDB client
client = chromadb.PersistentClient()

# Create or get an existing collection in ChromaDB
collection = client.get_or_create_collection('status_updates')


# Define a function to process JSON data
def load_json_to_chromadb(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        for record in data:
            tasks = record.get('tasks', [])
            for task_group in tasks:
                task_date = task_group.get("date")
                for task in task_group.get("tasks", []):
                    # Generate unique ID and prepare document string
                    document_id = str(uuid.uuid4())
                    document_text = f"{task.get('task_name')}: {task.get('description')} (Time spent: {task.get('time_spent')} hours)"

                    # Metadata for additional fields
                    metadata = {
                        "subject": record.get("subject"),
                        "date": task_date,
                        "task_name": task.get("task_name"),
                        "description": task.get("description"),
                        "time_spent": task.get("time_spent"),
                    }

                    # Add to collection with document text as a string
                    collection.add(
                        documents=[document_text],
                        ids=[document_id],
                        metadatas=[metadata]
                    )


# Load each JSON file into ChromaDB
load_json_to_chromadb('structured_emailsFeburary.json')
load_json_to_chromadb('structured_emailsMarch.json')
load_json_to_chromadb('structured_emailsApril.json')
load_json_to_chromadb('structured_emailsMay.json')
load_json_to_chromadb('structured_emailsJune.json')
load_json_to_chromadb('structured_emailsJuly.json')
load_json_to_chromadb('structured_emailsAugust.json')
load_json_to_chromadb('structured_emailsSeptember.json')
load_json_to_chromadb('structured_emailsOctober.json')
load_json_to_chromadb('structured_emails.json')

# Verify documents in collection
print("Total documents in collection:", collection.count())
