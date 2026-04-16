[app]

title = ЮграТур
package.name = ugratour
package.domain = org.tourism.ugra

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf

version = 2.0

requirements = python3,kivy,kivymd,requests,pillow

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION

android.api = 30
android.minapi = 21
android.ndk = 25b
android.sdk = 30

android.archs = arm64-v8a

android.accept_sdk_license = True

icon.filename = 
presplash.filename = 

source.exclude_exts = pyc,pyo,so,dylib,o,obj,exe,spec
source.exclude_dirs = tests,bin,libs

log_level = 2
