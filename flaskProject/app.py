from flask import Flask
import gradio as gr

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'



if __name__ == '__main__':
    app.run()
