import subprocess
import sys

# List the names of the modules you want to install
modules_to_install = [
    're',
    'configparser',
    'mysql',
    'tkinter',
    'ttkthemes',

]

# Iterate through the list of modules and install them using pip
for module in modules_to_install:
    try:
        # Use subprocess to call pip and install the module
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing {module}: {e}")
