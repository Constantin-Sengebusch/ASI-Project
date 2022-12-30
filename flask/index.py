from flask import Flask, render_template, request

import asi_script.mainScript as ms

#Flask initialization
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get", methods=["GET","POST"])
def chatbot_response():
    msg = request.form["msg"]
    response = ms.mainScript(msg)
    return str(response)

if __name__ == "__main__":
    app.run()