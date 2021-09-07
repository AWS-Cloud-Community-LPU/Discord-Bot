from flask import Flask
from threading import Thread
app = Flask('')

@app.route('/')
def home():
	return "Working ......"

def run():
	app.run(host='localhost',port=5555)

def keep_alive():
	t = Thread(target=run)
	t.start()
