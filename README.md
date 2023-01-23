# Long-Term Memory for Conversational Agents Demo

This serves as an example of the ConversationEntityMemory module in Langchain.

Talk to the bot & see the entities mentioned in conversation appear on the left-hand side as the bot understands them.

Click Refresh Chat (make sure the text input is clear first) to clear the conversation context and see that the bot still "remembers" what you told it.

## Run locally

Run `streamlit run main.py` in your terminal (make sure your OpenAI API key is set as an environment variable OPENAI_API_KEY first).

## Deploy on Streamlit

This is easily deployable on the Streamlit platform.
Note that when setting up your StreamLit app you should make sure to add `OPENAI_API_KEY` as a secret environment variable.
