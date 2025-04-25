import pystray
import PIL.Image
import requests
import json

#################################################
# This script is a system tray application that interacts with the Sonar software.
# It retrieves a list of audio devices from the Sonar server and allows the user to select
# a device to redirect audio to. The script uses the pystray library to create a system tray icon
# and menu, and the requests library to communicate with the Sonar server.
# The script also includes functions to restart the application and exit the system tray icon.
#################################################
# Depricated, because of GGSysTray csharp project
#################################################


def get_devices():
    return [
        {"name": dev["friendlyName"], "id": dev["id"]}
        for dev in json.loads(
            requests.get("http://127.0.0.1:6971/audioDevices").content
        )
        if dev["dataFlow"] == "render" and dev["role"] == "none"
    ]


devices = get_devices()


class Device(pystray.MenuItem):
    def __init__(
        self,
        text,
        action,
        checked=None,
        radio=False,
        default=False,
        visible=True,
        enabled=True,
        device_id="",
    ):
        super().__init__(text, action, checked, radio, default, visible, enabled)
        self._device_id = device_id

    @property
    def device_id(self):
        return self._device_id

    @property
    def device_id_http(self):
        return self._device_id.replace("{", "%7B").replace("}", "%7D")


def generate_menu():
    return pystray.Menu(
        pystray.MenuItem(
            "devices",
            pystray.Menu(
                *(
                    Device(dev["name"], test, radio=True, device_id=dev["id"])
                    for dev in devices
                )
            ),
        ),
        pystray.MenuItem("restart", restart),
        pystray.MenuItem("exit", shutdown),
    )


def test(icon, item: Device):
    requests.put(
        f"http://127.0.0.1:6971/streamRedirections/monitoring/deviceId/{item.device_id}"
    )


def restart(icon: pystray.Icon, item: pystray.MenuItem):
    global devices
    devices = get_devices()
    icon.menu = generate_menu()


def shutdown(icon: pystray.Icon, item):
    icon.stop()


icon = pystray.Icon(
    "Sonar Controller",
    PIL.Image.open("E:\programowańsko\GGsonarRev\sonar.ico"),
    menu=generate_menu(),
)
icon.run()
