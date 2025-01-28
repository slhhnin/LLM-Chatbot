import streamlit as st
import cohere

# Initialize Cohere client
co = cohere.Client(api_key="YOUR_API_KEY")

st.title("CohereAI Chat")

model_options = [
    "command-r-08-2024",
    "command",
    "command-light",
    "command-light-nightly",
    "command-r",
    "command-r-plus",
]

# Add a dropdown to select the model
selected_model = st.sidebar.selectbox("Choose the Cohere model:", model_options)
temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.3,
    # step=0.01,
)


# Set a default model
if "cohere_model" not in st.session_state:
    st.session_state["cohere_model"] = selected_model  # "command-r-08-2024"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["message"])

# Accept User input
if prompt := st.chat_input("What is up?"):
    print("prompt", prompt)
    # Add User message to chat history
    st.session_state.messages.append({"role": "User", "message": prompt})
    # Display User message in chat message container
    with st.chat_message("User"):
        st.markdown(prompt)

    # Display Chatbot response in chat message container
    with st.chat_message("assistant"):
        response_text = ""
        # Call Cohere's chat stream API
        stream = co.chat_stream(
            model=st.session_state["cohere_model"],
            message=prompt,
            temperature=temperature,
            chat_history=[
                {
                    "role": "Chatbot" if m["role"] == "assistant" else m["role"],
                    "message": m["message"],
                }
                for m in st.session_state.messages
            ],
            prompt_truncation="AUTO",
            connectors=[{"id": "web-search"}],
        )
        # Collect the stream's output
        for event in stream:
            if event.event_type == "text-generation":
                response_text += event.text
        st.markdown(response_text)  # Display streamed text incrementally

        # Add Chatbot response to chat history
        st.session_state.messages.append(
            {"role": "assistant", "message": response_text}
        )
