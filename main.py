import requests
import yaml
from flask import Flask
from flask import Response

app = Flask(__name__)

@app.route('/metrics')
def smoketestendpoint():
    return Response(run_test_groups(), mimetype='text/plain')

def run_test_groups():
    results = ''
    with open("tests.yml", 'r') as stream:
        try:
            testyaml = yaml.safe_load(stream)
            for tg in testyaml['testgroups']:
                results += run_sub_tests(tg)
        except yaml.YAMLError as exc:
            results = exc
    return results

def run_sub_tests(testyaml):
    localresults = ''
    for x in testyaml['tests']:
        test_name = x['name']
        test_url = x['query']
        test_check = x['result']
        test_name_formed = test_name.lower().replace(" ","_")
        localresults += "# HELP " + test_name_formed + " " + test_name + '\n'
        localresults += "# TYPE " + test_name_formed + " counter" + '\n'
        r = requests.get(url = test_url)
        localresults += test_name_formed + " "
        if test_check in r.content.decode("utf-8"):
            localresults += "1" + '\n'
        else:
            localresults += "0" + '\n'
    return localresults

if __name__ == '__main__':
    app.run()