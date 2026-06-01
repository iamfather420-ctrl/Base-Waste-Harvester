[app]

# (str) Title of your application
title = Agate Node

# (str) Package name
package.name = agatenode

# (str) Package domain (needed for android package identifier)
package.domain = org.agate

# (str) Source code directory (tells buildozer to compile the files right here)
source.dir = .

# (list) Source files to include (letting it read python files and assets)
source.include_exts = py,png,jpg,kv,json,txt

# (str) Application version
version = 1.0.0

# (list) Application requirements
# Add any extra pip packages your code needs here (separated by commas)
requirements = python3,kivy

# (int) Orientation (1 = portrait, 2 = landscape, 3 = all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# ===============================================================
# NOTE: The rest of your Android API, NDK, and Architecture keys 
# are automatically handled and inserted by your custom GitHub action!
# ===============================================================

