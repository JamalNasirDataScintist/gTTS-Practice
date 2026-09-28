import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")
st.title("🤖 Gemini Chatbot By Soumya")

# Input API Key
api_key = st.text_input("Gemini API key", type="password")

if api_key:
    genai.configure(api_key=api_key)

    # Fetch models that support generateContent
    st.info("Fetching available models...")
    try:
        models = genai.list_models()
        gen_models = [m.name for m in models if "generateContent" in m.supported_generation_methods]

        if gen_models:
            model_name = st.selectbox("Select a model:", gen_models)

            # Initialize chat history
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []

            # User input
            user_msg = st.text_input("Ask anything...")

            if st.button("Send"):
                if user_msg:
                    # Save user message
                    st.session_state.chat_history.append(("You", user_msg))

                    # Generate response
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(user_msg)
                    bot_reply = response.text

                    # Save bot reply
                    st.session_state.chat_history.append(("Bot", bot_reply))

            # Display chat
            for sender, msg in st.session_state.chat_history:
                if sender == "You":
                    st.markdown(f"🧑 You:** {msg}")
                else:
                    st.markdown(f"🤖 Bot:** {msg}")
        else:
            st.error("No models supporting generateContent found.")

    except Exception as e:
        st.error(f"Error fetching models: {e}")

else:
    st.info("🔑 Please enter your Gemini API Key to start chatting.")
