import requests
import yaml
from flask import Flask

app = Flask(__name__)

@app.route('/')
def smoketestendpoint():
    return runtests()

def runtests():
    results = ''
    with open("tests.yml", 'r') as stream:
        try:
            testyaml = yaml.safe_load(stream)
            for x in testyaml['tests']:
                test_name = x['name']
                test_url = x['query']
                test_check = x['result']
                results += "# Testing: " + test_name + " \n"
                r = requests.get(url = test_url)
                results += test_name.lower().replace(" ","_")
                if test_check in r.content.decode("utf-8"):
                    results += "PASSED" + " \n"
                else:
                    results += "FAIL" + " \n"
        except yaml.YAMLError as exc:
            results = exc
    return results
