from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("")

@app.route("/result")
def result():
    text = request.args.get("ver")
    return html.escape(text)

@app.route("/make", methods=["GET, POST"])
def make():
    if request.method == "GET":
        return render_template("make.html")
    elif 


if __name__ == "__main__":
    app.run(host = "0.0.0.0")