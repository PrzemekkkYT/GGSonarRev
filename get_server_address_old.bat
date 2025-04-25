@echo off
@chcp 1250



FOR /F "tokens=2,3 delims=:" %%i IN ('curl -s -k "https://127.0.0.1:6327/subApps" ^| py -c "import sys, json; print(json.load(sys.stdin)['subApps']['sonar']['metadata']['webServerAddress'])"') DO (
    SET IP=%%i
    SET PORT=%%j
)

netsh interface portproxy delete v4tov4 listenaddress=0.0.0.0 listenport=6971

netsh interface portproxy add v4tov4 listenport=6971 listenaddress=0.0.0.0 connectport=%PORT% connectaddress=%IP://=%