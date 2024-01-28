import requests
import yaml


with open('config.yaml') as f:
    config = yaml.safe_load(f.read())
for key in ["max_results", "max_cutoff"]:
    if key not in config:
        print("Error: %s missing from config." % key)
        exit()

    
def query_api(query, max_results, max_cutoff):
    response = requests.post('http://127.0.0.1:5000',
                             json={"query": query,
                                   "max_results": max_results,
                                   "max_cutoff": max_cutoff})
    return response.json()['output']


user_input = input("Enter your query: ")
results = query_api(user_input, config['max_results'], config['max_cutoff'])
for result in results:
    print(result)

