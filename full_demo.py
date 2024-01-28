import openai
import os
import requests
import yaml


INTRO = """
Please select an option.
1 - Find similar text.
2 - Talk to chatbot.
3 - Exit.
"""

LLM_PROMPT = """
Please respond to a user query given context.

Context:
%s

Query:
%s
"""

openai.organization = os.environ["OPENAI_ORG_ID"]
openai.api_key = os.environ["OPENAI_API_KEY"]

with open('config.yaml') as f:
    config = yaml.safe_load(f.read())

    
def ask_chatgpt(message, temperature=0):
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": message}
      ],
      temperature=temperature
    )
    return completion.choices[0].message.content

def query_api(query, max_results, max_cutoff):
    response = requests.post('http://127.0.0.1:5000',
                             json={"query": query,
                                   "max_results": max_results,
                                   "max_cutoff": max_cutoff})
    return response.json()['output']


while True:
    option = input(INTRO)
    if option == "1":
        user_input = input("Enter your query: ")
        results = query_api(user_input, config['max_results'], config['max_cutoff'])
        for result in results:
            print(result)
    elif option == "2":
        user_input = input("Enter your query: ")
        results = query_api(user_input, config['max_results'], config['max_cutoff'])
        prompt = LLM_PROMPT % ("\n".join(results), user_input)
        output = ask_chatgpt(prompt, config['temp'])
        print(output)
    elif option == "3":
        break
    else:
        print("Invalid option.")
