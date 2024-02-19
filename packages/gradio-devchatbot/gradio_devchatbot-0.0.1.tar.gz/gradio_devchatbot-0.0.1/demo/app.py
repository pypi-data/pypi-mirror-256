
import gradio as gr
from gradio_devchatbot import Devchatbot
from random import random
import re 


is_secure_chatbot=False

def add(num1, num2):
        return num1 + num2




my_code =''
def get_python_code(text):
    match = re.search(r"```\n([\s\S]*?)\n```", text)
    if match:
        return match.group(1)
    else:
        return None

def execute_py_code():
    try:
        exec(my_code)
    except Exception as e:
        print(f"Error executing code: {e}")

def on_select(evt: gr.SelectData):  # SelectData is a subclass of EventData
    return f"You selected {evt.value} at {evt.index} from {evt.target}"


js_function = "() => { \
  const event = new CustomEvent('secUpdated',{detail:{isSecure:Boolean(Math.round(Math.random()))}}); \
  document.dispatchEvent(event); \
}"


with gr.Blocks() as demo:
    
    
    chatbot = Devchatbot(show_copy_button=True, likeable=True, runnable=True, enable_security=False)
    msg = gr.Textbox()
    is_secure= gr.Button("is_secure")
    is_secure.click(None,[],[],js=js_function)
    
    chatbot.play(execute_py_code,[],[])
    def respond(message, chat_history):
        bot_message = "How are you?\n im good thanks \n```\nprint(\"Hello World\")\nprint(\"Hello World\") \nprint(\"Hello World\")\n```" if random() > 0.5 else "How are you?\n im good thanks \n```\nprint(\"Hello\")\nprint(\"Hello\")\nprint(\"Hello\")\n```" if random() > 0.5 else "How are you?\n im good thanks"
        code = get_python_code(bot_message)
        if code:
            global my_code
            my_code = code
        chat_history.append((message, bot_message))
        return  chat_history
    
    msg.submit(respond, [msg,chatbot], [chatbot])

if __name__ == "__main__":
    demo.launch()