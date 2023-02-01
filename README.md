# Home Assistant Kiosk
Description:
A small python script that starts a firefox browser in kiosk mode and launches to your homeassistant page.

It will kill the browser and relaunch it automatically if:
  - It is not on the HA page
  - It disconnected and recently reconnected
  - The user is not logged in

Currently the script requires:
  - Selenium for python
  - Python 3.11
  - Linux
  - Firefox
