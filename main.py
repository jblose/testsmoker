import requests
import yaml
from flask import Flask
from flask import Response

app = Flask(__name__)

# Route for execution
@app.route('/metrics')
def smoketestendpoint():
    return Response(run_test_groups(), mimetype='text/plain')

def run_test_groups():
    results = ''
    # Open YML file
    with open("tests.yml", 'r') as stream:
        try:
            # safe_load due to vulnerabilities
            testyaml = yaml.safe_load(stream)
            # Iterate on testgroups
            for tg in testyaml['testgroups']:
                group_name = tg['name']
                group_name_formed = group_name.lower().replace(" ","_")
                passed_cnt = 0
                total_cnt = 0      
                # Iterate on tests inside testgroups          
                for x in tg['tests']:
                    total_cnt += 1
                    test_name = x['name']
                    test_url = x['query']
                    test_check = x['result']
                    test_name_formed = test_name.lower().replace(" ","_")
                    results += "# HELP " + test_name_formed + " " + test_name + '\n'
                    results += "# TYPE " + test_name_formed + " counter" + '\n'
                    r = requests.get(url = test_url)
                    results += test_name_formed + " "
                    # Passed tests are "true/1, failures our "false/0"
                    if test_check in r.content.decode("utf-8"):
                        passed_cnt += 1
                        results += "1" + '\n'
                    else:
                        results += "0" + '\n'       

                # Total tests executed for a group
                results += "# HELP " + group_name_formed + "_total " + group_name + " Total" + '\n'
                results += "# TYPE " + group_name_formed + "_total counter" + '\n'
                results += group_name_formed + "_total " + str(total_cnt) + '\n'
                
                # Total Passed tests executed for the group
                results += "# HELP " + group_name_formed + "_passed_total " + group_name + " Total" + '\n'
                results += "# TYPE " + group_name_formed + "_passed_total counter" + '\n'
                results += group_name_formed + "_passed_total " + str(passed_cnt) + '\n'
                
                # Total Failed tests executed for the group
                failed_cnt = total_cnt - passed_cnt
                results += "# HELP " + group_name_formed + "_failed_total " + group_name + " Total" + '\n'
                results += "# TYPE " + group_name_formed + "_failed_total counter" + '\n'
                results += group_name_formed + "_failed_total " + str(failed_cnt)  + '\n'
        except yaml.YAMLError as exc:
            results = exc
    return results

if __name__ == '__main__':
    app.run()