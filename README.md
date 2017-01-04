# auto_busy
Automatically pulls up a specified window when a person is detected on camera for a specified period of time

## To install requirements type the following in the CMD
pip install -r requirements.txt


## You'll also need to change the Camera URL, App Name, and Window Name as needed. 
## To do this open object_movement.py and focus on lines 29-31

* The Camera URL will only change part of the field. 

  * By default it is "self.camera_url = 'rtsp://admin:admin@10.10.50.33:8554/CH001.sdp". 

  * So, for example, if your camera's URL is 10.10.26.50 the camera url will now be rtsp://admin:admin@10.10.26.50:8554/CH001.sdp

* The self.app_name is going to be found when right clicking an App within Task Manager. 

  * The app name will be the editable field with the type of file added on. 

  * Example notepad is the name and it is an exe, so the app name is notepad.exe.

* The Window name is the name when hovering over the app. 

  * For example, when you create a new notepad doc and hover over the notepad icon it will say "Untitled - Notepad". 

## NOTES:
### DO NOT MINIMIZE THE APP YOU WANT TO POP UP. It should stay up but in the background of whatever you're currently doing. Minimizing will break the app!
### To see video go into the conf.json file and set show_video to true


