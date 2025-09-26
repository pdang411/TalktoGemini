from dotenv import load_dotenv
import os
import google.generativeai as genai
import gradio as gr

load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "modular.json"

google_application_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")



# Initialize the model
model = genai.GenerativeModel('gemini-1.5-pro')
prompt = "Enter your message here"
assistant = "assistant"  # Define the "assistant" variable
def generate_response(prompt, state):
    # Use streaming for faster output
    # Ensure state is a list of messages
    if state is None:
        state = []
    # Add user message to state
    state.append({"role": "user", "content": prompt})
    response_stream = model.generate_content(prompt, stream=True)
    partial = ""
    for chunk in response_stream:
        if hasattr(chunk, 'text'):
            partial += chunk.text
            # Prepare full chat history with latest assistant message
            messages = state + [{"role": "assistant", "content": partial}]
            yield (messages, state)



def chat_lm (input,history):
    history = history or []
    s = list(sum(history,()))
    s.append(input)
    inp = ' '.join(s)
    output = chat_lm(inp)
    history.append((input))
    return history, history, output

block = gr.Blocks()
with block:
    gr.Markdown("""<h1><center>Chat with Gemini Pro</center></h1>""")
    chatbot = gr.Chatbot(height=550)
    message = gr.Textbox(placeholder=prompt,type="text",label="Message",)
    submit = gr.Button("SEND")
    state = gr.State()
    submit.click(generate_response,inputs=[message,state],outputs=[chatbot,state])

block.launch(debug=True)


