import requests, json

requests.packages.urllib3.disable_warnings()

subApps = json.loads(
    requests.get("https://127.0.0.1:6327/subApps", verify=False).content
)
address = subApps["subApps"]["sonar"]["metadata"]["webServerAddress"]

print(address.replace("http://", ""))
