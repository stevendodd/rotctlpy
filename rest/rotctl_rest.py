from flask import Flask
from flask import request
import paramiko
import json
import os.path
import os
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

def setHeading(heading):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(server, username=username, password=password)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("/bin/sh " + scriptPath + " " + heading)
    app.logger.info(ssh_stdout.readlines())
    app.logger.info(ssh_stderr.readlines())
    return("OK")


configFile = "./config.json"
server = username = password = scriptPath = ""
if os.path.exists(configFile):
    f = open(configFile)
    c = json.load(f)
    server = c["server"]
    username = c["username"]
    password = c["password"]
    scriptPath = c["scriptPath"]

    
app = Flask(__name__)

@app.route("/",methods = ['GET'])
def hello():
    return('stevendodd/RotCtrl')

@app.route("/<heading>",methods = ['GET'])
def set_heading(heading):
    return setHeading(heading)
