# -*- mode: python -*-
import PyInstaller.utils.hooks
import PyInstaller.config
from os import path 
import os

script_dir = path.dirname(path.abspath(SPEC))

PyInstaller.config.CONF['workpath'] = "C:\\tmp\\garbage"
PyInstaller.config.CONF['distpath'] = os.path.join(script_dir, 'dist')

block_cipher = None

hiddenimports = ['pysnmp.smi.exval','pysnmp.cache']

a = Analysis(['03.py'],
             pathex=['C:\\repo\\snmpRead'],
             binaries=[],
             datas=PyInstaller.utils.hooks.collect_data_files('pysnmp'),
             hiddenimports=PyInstaller.utils.hooks.collect_submodules('pysmi')+\
             PyInstaller.utils.hooks.collect_submodules('ply') + \
             PyInstaller.utils.hooks.collect_submodules('pyasn1') + \
             PyInstaller.utils.hooks.collect_submodules('pysnmp'),
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
x = Tree('C:\\Python\\Lib\\site-packages\\pysnmp\\smi\\mibs', prefix='pysnmp/smi/mibs')
y = Tree('C:\\Python\\Lib\\site-packages\\pysmi',prefix='pysmi')

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
         a.scripts,
         a.binaries,
         a.zipfiles,
         a.datas,
         x, y,
         name='03x64',
         debug=False,
         strip=False,
         upx=True,
         runtime_tmpdir=None,
         console=True,
         icon=os.path.join(script_dir, '03.ico'))
