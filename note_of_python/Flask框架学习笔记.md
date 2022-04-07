## Flask - python web programming

Installation
----
```shell
sudo apt-get install python-pip
sudo pip install virtualenv
sudo pip install setuptools
sudo pip install flask
```

Example - Hello, World
----
Make project directory
```
$ mkdir helloWorld
$ cd helloWorld
$ virtualenv venv
```

How to active and deactive virtualenv?
```
$ . env/bin/active  # for active
$ deactive  # for deactive
```

Code of hello.py
```python
#!/usr/bin/env python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello_world():
    return 'Hello, Wolrld!'
```

How to run?
```
$ export FLASK_APP=hello.py
$ flask run
 * Running on http://127.0.0.1:5000/
```
