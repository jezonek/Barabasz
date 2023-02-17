# Barabasz Signal Bot

## What is Barabasz?

This is a bot that uses the SIGNAL REST API (specifically, websocket JSON-RPC) to receive and analyze messages from Signal messenger and send queries to OpenAI language models. 
Once configured, the bot redirects messages to the selected language model and returns a response from the network.
At this point, OpenAI does not provide a GPT Chat API, so the bot does not understand and store the context of the utterance and the entire query must be contained in a single prompt. 

## Features

- Support for direct messages 
- Support for group messages, (you need to add a Signal user to a group and then mention
 him in the message)
- Open to modification- you can easily add other logic to process messages

## Configuration

### Configure your own Signal Backend:


> Important note: Configure your API in [JSON-RPC mode](https://github.com/bbernhard/signal-cli-rest-api#execution-modes)



[More info about SIGNAL REST CLI](https://github.com/bbernhard/signal-cli-rest-api) 

### Clone the repository

```Bash
git clone xxx
```

### Configure your own env variables
```Bash
cd barabasz

cp .env_example .env
```
Complete the .env file with the data. Add your OpenAI API key, your Signal account number, and the endpoints of your Signal Rest API

### Install pipenv dependencies
```Bash
pipenv install
```

### Start the bot

```bash
pipenv run python src/barabasz.py
```

Bot will connect to your configured secure websocket (wss) endpoint SIGNAL_WEBSOCKET_RX_ENDPOINT and start to listen for incoming messages.

Sending a response is done by executing a post request to the URI specified in SIGNAL_HTTPS_ENDPOINT

### Deployment

I deploy my bot as a service on linux, using systemd. The sample .service file is in the deploy folder. In place of USERNAME, insert the name of the user who is running the service. I upload the files to the server to the user's root directory via scp.
