# -*- mode: python -*-

block_cipher = None

added_files = [
         ('.\\templates', 'templates'),
         ('.\\static', 'static')
         ]
a = Analysis(['run.py'],
             pathex=['c:\\Users\\esiwegu\\panBaiduCom\\CloudStation\\project2017\\tool_7_parser_comparing\\flaskHandler'],
             binaries=[],
             datas=[],
             hiddenimports=['flask', 'pywebview', 'difflib', 'dictdiffer', 'werkzeug', 'email' , 'email.mime.message', 'email.mime.image' , 'email.mime.text' , 'email.mime.multipart', 'email.mime.audio'],
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
          name='run',
          debug=False,
          strip=False,
          upx=False,
          console=True , icon='static\\favicon-gui.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='run')
