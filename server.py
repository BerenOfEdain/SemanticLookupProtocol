import chromadb
from flask import Flask, jsonify, request
import os


ROOT_FILE = 'data'

app = Flask(__name__)

chroma_client = chromadb.Client()


collection = chroma_client.create_collection(name="test_collection")
for file_id, file in enumerate(os.listdir(ROOT_FILE)):
    with open(os.path.join(ROOT_FILE, file)) as f:
        file_content = [paragraph for paragraph in f.read().split('\n\n') if paragraph]

    collection.add(
        documents=file_content,
        metadatas=[{"source": file} for _ in range(len(file_content))],
        ids=["%d_%d" % (file_id, j) for j in range(len(file_content))]
    )
    
def query_db(query, max_results, max_cutoff):
    results = collection.query(
        query_texts=[query],
        n_results=max_results
    )
    num_valid = len([num for num in results['distances'][0] if num < max_cutoff])
    return results['documents'][0][:num_valid]


@app.route('/', methods=['GET', 'POST'])
def lookup():
    results = query_db(request.json["query"], request.json["max_results"], request.json["max_cutoff"])
    return jsonify({"output": results})
 
if __name__ == '__main__':
    app.run(debug=True)