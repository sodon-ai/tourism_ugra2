[app]
# Информация приложения
title = ЮграТур
package.name = ugratour
package.domain = org.tourism.ugra
version = 2.0

# Исходные файлы
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
source.exclude_exts = pyc,pyo,so,dylib,o,obj,exe,spec
source.exclude_dirs = tests,bin,libs,venv,.git

# Зависимости (проверенные версии)
requirements = python3,kivy==2.3.0,kivymd==0.104.1,requests==2.31.0,pillow==10.1.0

# UI и ориентация
orientation = portrait
fullscreen = 0
icon.filename = 
presplash.filename = 

# Разрешения
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION

# Android настройки
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True

# Оптимизация сборки
p4a.source_dir = 
p4a.local_recipes = 
android.skip_update = False
android.enable_proguard = True

# Логирование
log_level = 2
