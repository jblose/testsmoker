import requests
import yaml

with open("tests.yml", 'r') as stream:
    try:
        testyaml = yaml.safe_load(stream)
        for x in testyaml['tests']:
            test_name = x['name']
            test_url = x['query']
            test_check = x['result']
            print('Testing: '+test_name)
            r = requests.get(url = test_url)
            if test_check in r.content.decode("utf-8"):
                print("PASSED")
            else:
                print("FAIL")
    except yaml.YAMLError as exc:
        print(exc)
