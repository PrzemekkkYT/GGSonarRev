[![pl](https://img.shields.io/badge/lang-pl-red.svg)](README.pl.md)

# SteelSeries GG - Sonar Api reverse engineering ![Sonar](sonar.ico)

Shout-out to [Wex](https://github.com/wex) for idea and detailed explanation on how to commence on topic.

If you want to add something from yourself, create a pull or write to me :)

## **Backstory**

I was searching through the internet for a way to control sonar using external program.  
I found [Sonar API reverse engineering](https://github.com/wex/sonar-rev) on github and tried to do something with it.

## My approach to the subject

Like Wex I used Wireshark to examine the traffic on the port taken from the result <br>
`curl https://127.0.0.1:6327/subApps -k`
I noticed that the sonar port changes after a full restart of the program, so it is different every time.

I made a simple [powershell script](get_server_address.ps1) that automatically connects port 6971 to the variable sonar port

I also created a simple SysTray program to easily change the device to which the sonar transmits the sound (headphones, speakers, etc.)

## **Endpoints**

### **API uses `HTTP` protocol**

The same variable port is used for each endpoint

<h3>Legend</h3>
Here are described all mental shortcuts with their possible values ​​separated by the character " | "

- channel
  - master | game | chat | media | aux | chatCapture (mic)
- boolean
  - true | false

<br>
<br>
<br>

- ### GET

  - /configs - available configurations of all sound channels
  - /configs/selected - selected configurations
  - /audioDevices - info about all available sound devices
  - /onboarding - [requires analysis]
  - /chatMix - level of 'CHATMIX' slider between game and chat
  - /mode - selected sonar mode. Either Stream or Classic
  - /volumeSettings/classic - volume settings of all virtual audio devices. Returns only settings of classic mode
  - /volumeSettings/streamer - volume settings of all virtual audio devices. Returns settings from both streamer and classic mode
  - /audioSamples/\* - sound sample management
    - /audioSamples/samples?role=\<category> - Loads audio samples that can be listened to during configuration
    - /audioSamples/isRecording - [requires analysis]
  - /features - [requires analysis]
  - /classicRedirections - redirecting sound channels to output devices in classic mode
  - /streamRedirections - redirecting sound channels to output devices (streaming, monitoring and microphone)

- ### PUT
  - /audioSamples/\* - sound sample management
    - /audioSamples/stopRecord - [requires analysis]
  - /streamRedirections
    - /streamRedirections/isStreamMonitoringEnabled/false - is called with every interaction with channels in the sonar panel
    - /streamRedirections/streaming/redirections/\<channel>/isEnabled/\<boolean> - switch redirection to stream mix for channels in streamer mode
  - /volumeSettings/streamer/monitoring/master/volume/<0.00 - 1.00>
    - /monitoring | /streaming
  - /configs/\<config_id>/select - sets the current audio track configuration (the program itself knows which id belongs to which track)
