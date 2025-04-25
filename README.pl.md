[![en](https://img.shields.io/badge/lang-en-red.svg)](README.md)

# SteelSeries GG - Sonar Api reverse engineering ![Sonar](sonar.ico)

Pozdrowienia dla [Wexa](https://github.com/wex) za pomysł i dokładne wytłumaczenie jak zacząć temat.

Jeśli chcesz dołożyć coś od siebie, stwórz pulla albo do mnie napisz :)

## **Krótka historia**

Przeszukiwałem internet w celu znalazienia sposobu na kontrolowanie sonaru za pomocą zewnętrznego programu.  
Znalazłem [Sonar API reverse engineering](https://github.com/wex/sonar-rev) na githubie i spróbowałem coś z tym zrobić

## Moje podejście do tematu

Podobnie jak Wex użyłem Wiresharka, żeby zbadać ruch na porcie wziętym z wyniku <br>
`curl https://127.0.0.1:6327/subApps -k`  
Zauważyłem, że port sonara zmienia się po pełnym zrestartowaniu programu, więc za każdym razem jest inny.

Zrobiłem prosty [skrypt powershella](get_server_address.ps1), który podpina automatycznie port 6971 pod zmienny port sonara

Stworzyłem także prosty program [GGSysTray](https://github.com/PrzemekkkYT/GGSysTray) do łatwej zmiany urządzenia do którego sonar przesyła dźwięk (słuchawki, głośniki, itp.)

## **Endpointy**

### **API używa protokołu `HTTP`**

Do każdego endpointu wykorzystywany jest ten sam zmienny port.

<h3>Legenda</h3>
Tu są opisane wszystkie skróty myślowe z ich możliwymi wartościami oddzielonymi znakiem " | "

- kanał
  - master | game | chat | media | aux | chatCapture (mic)
- boolean
  - true | false

<br>
<br>
<br>

- ### GET

  - /configs - możliwe konfiguracje wszystkich kanałów dźwiękowych
  - /configs/selected - wybrane konfiguracje
  - /audioDevices - informacje o wszystkich dostępnych urządzeniach dźwiękowych
  - /onboarding - [wymaga analizy]
  - /chatMix - poziom ustawienia suwaka 'CHATMIX' między grą a chatem
  - /mode - jaki jest ustawiony tryb sonaru. Stream lub Classic
  - /volumeSettings/classic - ustawienia głośności każdego ze sprzętowych urządzeń wyjściowych. Zwraca tylko ustawienia trybu classic
  - /volumeSettings/streamer - ustawienia głośności każdego ze sprzętowych urządzeń wyjściowych. Daje informacje z trybu streamera oraz classic.
  - /audioSamples - zarządzanie próbkami dźwięków
    - /audioSamples/samples?role=\<kategoria> - Wczytuje próbki dźwięku możliwe do odsłuchania podczas konfiguracji
    - /audioSamples/isRecording - [wymaga analizy]
  - /features - [wymaga analizy]
  - /classicRedirections - możliwe, że przekierowania kanałów dźwiękowych na urządzenia wyjściowe w trybie klasycznym
  - /streamRedirections - przekierowania kanałów dźwiękowych na urządzenia wyjściowe (streaming, monitoring i mikrofon)

- ### PUT
  - /audioSamples - zarządzanie próbkami dźwięków
    - /audioSamples/stopRecord - [wymaga analizy]
  - /streamRedirections
    - /streamRedirections/isStreamMonitoringEnabled/false - wywołuje się wraz każdą interakcją z kanałami w panelu sonaru
    - /streamRedirections/streaming/redirections/\<kanał>/isEnabled/\<boolean> - przełączenie przekierowania na stream mix dla kanałów w trybie streamera
  - /volumeSettings/streamer/monitoring/master/volume/<0.00 - 1.00>
    - /monitoring | /streaming
  - /configs/\<id_konfiguracji>/select - ustawia aktualną konfigurację ścieżki audio (program sam wie, które id należy do której ścieżki)
