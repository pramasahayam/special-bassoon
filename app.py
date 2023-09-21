import sys
import subprocess
from package_installer import install_dependencies

try:
    import flask
    import numpy

except ImportError:
    print("Dependencies are missing. Installing...")
    install_dependencies()

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()