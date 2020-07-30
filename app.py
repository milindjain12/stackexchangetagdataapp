from flask import Flask, render_template, url_for, request, redirect
from util.extract_data import ExtractData
from util.graph import Graph

import sys

app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
def index():
    api_url = "https://api.stackexchange.com/2.2/questions?page=1&pagesize=100&order=desc&sort=activity&site=datascience"
    file_url = ".//resources//"
    extract = ExtractData(api_url, file_url)
    graph = Graph()
    extract.extractData()
    graph.createGraph(extract.stack_exchange_tags)
    if(request.method == 'GET'):
        return render_template('index.html', show_tag=False)
    else:
        query = request.form.to_dict()
        associated_tags = graph.findNeighborsOfaTag(str(query['query']).lower())
        return redirect(url_for('tag_results', tags=associated_tags))


@app.route('/tag_result')
def tag_results():
    tags = request.args.getlist("tags")
    return render_template('index.html', tags=tags, show_tag=True)


if __name__ == "__main__":
    app.run(debug=True)
