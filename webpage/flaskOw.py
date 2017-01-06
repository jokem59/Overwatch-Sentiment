from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("homepage.html")

@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        # do something
        return render_template("query.html")
    else:
        return render_template("query.html")

if __name__ == "__main__":
    # starts the website on a server
    app.run(debug=True)