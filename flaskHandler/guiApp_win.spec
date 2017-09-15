# -*- mode: python -*-

block_cipher = None

added_files = [
         ('.\\templates', 'templates'),
         ('.\\static', 'static')
         ]

a = Analysis(['guiApp.py'],
             pathex=['c:\\Users\\esiwegu\\panBaiduCom\\CloudStation\\project2017\\tool_7_parser_comparing\\flaskHandler'],
             binaries=[],
             datas=[],
             hiddenimports=['flask', 'pywebview', 'difflib', 'dictdiffer', 'werkzeug', 'email.mime.message', 'email.mime.image', 'email.mime.text', 'email.mime.audio', 'email.mime.multipart'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='guiApp',
          debug=False,
          strip=False,
          upx=False,
          console=False , icon='static\\favicon-gui.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='guiApp')
