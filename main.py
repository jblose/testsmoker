import requests
import yaml
from flask import Flask

app = Flask(__name__)

@app.route('/metrics')
def smoketestendpoint():
    return runtests()

def runtests():
    results = '<pre style-"word-wrap: break-word; white-space: pre-wrap;">'
    with open("tests.yml", 'r') as stream:
        try:
            testyaml = yaml.safe_load(stream)
            for x in testyaml['tests']:
                test_name = x['name']
                test_url = x['query']
                test_check = x['result']
                # results += "# Testing: " + test_name + '\n'
                r = requests.get(url = test_url)
                results += test_name.lower().replace(" ","_") + " "
                if test_check in r.content.decode("utf-8"):
                    results += "1" + '\n'
                else:
                    results += "0" + '\n'
            results += "</pre>"   
        except yaml.YAMLError as exc:
            results = exc
    return results
