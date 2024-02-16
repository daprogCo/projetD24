from flask import Flask, Response
import json

app = Flask(__name__)


@app.route('/data/<int:file>/<int:line>')
def get_data(file, line):
    try:
        f = open(f'./data/{file}.json', 'r')
        data = json.load(f)
        f.close()
        return Response(json.dumps(data[line]), mimetype='text/plain')
    except:
        return Response("No data", mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)