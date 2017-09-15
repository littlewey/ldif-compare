..\env\Scripts\pyinstaller.exe --onefile --windowed  --hidden-import=pywebview  --hidden-import=difflib  --hidden-import=dictdiffer  --hidden-import=werkzeug  --hidden-import=email.mime.message  --hidden-import=email.mime.image  --hidden-import=email.mime.text  --hidden-import=email.mime.audio  --hidden-import=email.mime.multipart   --icon=static\favicon-gui.ico  guiApp.py

xcopy templates dist\templates
xcopy static dist\static