import pygal
from flask import Flask, redirect, url_for, request
import main


app = Flask(__name__)


@app.route('/success/<query>')
def success(query):
    if query == 'Error Empty query':
        return "<h1>Error Empty query<h1>"
    cos_sim = "Cos sim : "
    auth = "Authority :"
    hub = "Hub :"
    result = main.HITS_algo(
        query, ["1.txt", "2.txt", "3.txt", "4.txt", "5.txt"])
    for i in result[0]:
        cos_sim += i + " : " + str(result[0][i]) + "\n"
    for i in result[1]:
        auth += i + " : " + str(result[1][i]) + "\n"
    for i in result[2]:
        hub += i + " : " + str(result[2][i]) + "\n"
    print(result[1])
    return "<h1>{0}<h1><h1>{1}<h1><h1>{2}<h1>".format(cos_sim, auth, hub)


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        query = request.form['query']
        return redirect(url_for('success', query=query))
    elif request.method == 'GET':
        with open("home.html") as file:
            return file.read()


app.debug = True
app.run()
