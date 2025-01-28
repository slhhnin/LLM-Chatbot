# CohereAI Chat
<img src="img/chat.png">

## Installation
```shell
pip install cohere streamlit
```

## API Key
Please add `<YOUR API KEY>` in chatbot.py line 5
```shell
# Initialize Cohere client
co = cohere.Client(api_key="YOUR_API_KEY")
```
## Run Streamlit APP
```shell
streamlit run chatbot.py
```