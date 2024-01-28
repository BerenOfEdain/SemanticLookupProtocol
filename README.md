# Semantic Lookup Protocol

This a protocol to enable users to offer writings of theirs so that others may search through them for semantically similar text. A typical use case envisioned is the server side implements a vectordb for text lookup, and the client side either returns the results as-is or feeds them into an LLM prompt for a chatbot experience. Strictly speaking though, neither use of a vectordb nor an LLM is required by the protocol.

To use, the client sends the server JSON over HTTP(S) of the form
```
{"query", <user query>,
 "max_results": <max number of results returned>}
```
with additional fields as desired and receives a response of the form
```
{"output": <list of outputs>}.
```

The demos in this repo illustrate using one additional field, **max_cutoff**.

Also while the demos use HTTP for simplicitly, all of this works over HTTPS.

## Full Demo (ChatGPT API required)

This demo allows both looking up text as-is and talking to ChatGPT using similar text as context. This does require access to the ChatGPT API, and one must set environmental variables **OPENAI_ORG_ID** and **OPENAI_API_KEY** according to one's OpenAI account.

In `config.yaml`, there are three parameters that may be tuned as desired (though the default values should be reasonably good for general purpose use):
  * **temp** - The temperature used for querying ChatGPT.
  * **max_results** - The maximum number of similar paragraphs that may be returned.
  * **max_cutoff** - The minimum embedding distance needed for a paragraph to possibly be returned.

In one terminal, run `server.py` to generate a local web server at `127.0.0.1:5000`. When queried via HTTP, this returns as JSON relevant paragraphs from text files in the `data` directory.

In another terminal, run `full_demo.py` to be prompted for instructions.

## Minimal Demo (ChatGPT API not required)

This demo allows for looking up similar text.

Usage is similar to that of the full demo. Set parameters as desired in `config.yaml` (this time **temp** is unused). Run `server.py` to set up the server for querying text in the `data` directory, and run `minimal_demo.py` to start the demo.

## Further Directions

Allowing additional input parameters gives this protocol greater flexibility.

One example not implemented here is instead of just querying top level files in `data`, one can query inside nested subdirectories, and a file path could be sent to restrict to a particular subdirectory.
