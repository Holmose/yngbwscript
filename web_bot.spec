# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['web_bot.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/hostedtoolcache/windows/Python/3.9.13/x64//Lib/site-packages/onnxruntime/capi/onnxruntime_providers_shared.dll','onnxruntime\\capi'), ('C:/hostedtoolcache/windows/Python/3.9.13/x64//Lib/site-packages/ddddocr/common.onnx', 'ddddocr'),('C:/hostedtoolcache/windows/Python/3.9.13/x64//Lib/site-packages/ddddocr/common_old.onnx', 'ddddocr'),('C:/hostedtoolcache/windows/Python/3.9.13/x64//Lib/site-packages/ddddocr/common_det.onnx', 'ddddocr')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='web_bot',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
