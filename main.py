import requests
import yaml
from flask import Flask
from flask import Response

app = Flask(__name__)

@app.route('/metrics')
def smoketestendpoint():
    return Response(runtests(), mimetype='text/plain')

def runtests():
    results = ''
    with open("tests.yml", 'r') as stream:
        try:
            testyaml = yaml.safe_load(stream)
            for x in testyaml['tests']:
                test_name = x['name']
                test_url = x['query']
                test_check = x['result']
                test_name_formed = test_name.lower().replace(" ","_")
                results += "# HELP " + test_name_formed + " " + test_name_formed + '\n'
                results += "# TYPE " + test_name_formed + " counter" + '\n'
                r = requests.get(url = test_url)
                results += test_name_formed + " "
                if test_check in r.content.decode("utf-8"):
                    results += "1" + '\n'
                else:
                    results += "0" + '\n'
        except yaml.YAMLError as exc:
            results = exc
    return results