[app]
title = ЮграТур
package.name = ugratour
package.domain = org.tourism.ugra
version = 2.0

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
source.exclude_exts = pyc,pyo,so,dylib,o,obj,exe,spec
source.exclude_dirs = tests,bin,libs,venv,.git

requirements = python3,kivy==2.2.1,requests,pillow

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION
android.api = 30
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True

log_level = 2
