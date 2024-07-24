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
    response = model.generate_content(prompt)
    return [("ASSISTANT", response.text)], state



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

