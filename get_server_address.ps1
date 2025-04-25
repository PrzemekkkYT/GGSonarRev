$OutputEncoding = [System.Text.Encoding]::UTF8

# Utwórz obiekt WebClient
$webClient = New-Object System.Net.WebClient

# Ignoruj błędy certyfikatów SSL (tylko do celów testowych, niezalecane w produkcji)
$webClient.Headers.Add("user-agent", "PowerShell-RestMethod")
[System.Net.ServicePointManager]::ServerCertificateValidationCallback = { $true }

# Pobierz dane JSON
try {
    $jsonResponse = $webClient.DownloadString("https://127.0.0.1:6327/subApps") | ConvertFrom-Json
}
catch {
    Write-Host "Błąd podczas pobierania danych: $_"
    exit 1
}

$webServerAddress = $jsonResponse.subApps.sonar.metadata.webServerAddress -replace '^http://'
$ip, $port = $webServerAddress -split ":"

echo $webServerAddress

# Usunięcie istniejącego portproxy
netsh interface portproxy delete v4tov4 listenaddress=0.0.0.0 listenport=6971

# Dodanie nowego portproxy w PowerShell
netsh interface portproxy add v4tov4 listenport=6971 listenaddress=0.0.0.0 connectport=$port connectaddress=$ip