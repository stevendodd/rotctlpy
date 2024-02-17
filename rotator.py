import json
import flask
from flask_socketio import SocketIO
import time
import socket
import sys
import datetime
import sys
from datetime import datetime
import os
import subprocess
import threading
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

# Define Flask Application, and allow automatic reloading of templates for dev
app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True

# SocketIO instance
socketio = SocketIO(app)

# Rotator singleton objects.
rotator = None
rotctldpy = None
args = None

# Global setpoint and position variables
current_position = {'azimuth': 0.0, 'elevation': 0.0}
current_setpoint = {'azimuth': 0.0, 'elevation': 0.0}

# Home position azimuth , elevation
HOME_POS = [0.0, 15.0]

# The number of degrees of rotation per second
rot_speed = 6

# Assumes rotator has 12 memory buttons labeled A-L
# Assumes rotator button A represents 30°, B 60° etc; 
# Each setting is made up of (min degrees, max degrees, direction)
# L Has two list elements as it resets the degrees back to 0
rot_pos = [
      ("L",   0,     15,  0),
      ("A",  15.001, 45, 30),
      ("B",  45.001, 75, 60),
      ("C",  75.001,105, 90),
      ("D", 105.001,135,120),
      ("E", 135.001,165,150),
      ("F", 165.001,195,180),
      ("G", 195.001,225,210),
      ("H", 225.001,255,240),
      ("I", 255.001,285,270),
      ("J", 285.001,315,300),
      ("U", 315.001,345,330),
      ("L", 345.001,361,  0)
      ]

# The shell script to send IR commands
dirname = os.path.dirname(os.path.abspath(__file__))
sendir = os.path.join(dirname, 'sendir.sh')


class ROTCTLD(object):
    """ rotctld (hamlib) server class """ 
    
    def __init__(self, host="0.0.0.0", port=65432):
        self.host = host
        self.port = port
        self.stop_thread = False
        self.rotctldpyThread = threading.Thread(target=self._run, args=(lambda: self.stop_thread,))
        self.rotctldpyThread.start()


    def send_command(self,command):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((self.host,self.port))
            sock.sendall(bytes(command+'\n', 'utf-8'))            
            resp = self.sock.recv(1024)
            sock.close()
            return(resp.decode("utf-8"))
        except:
            return None
        
        
    def get_heading(self):
        return([self.target_pos,self.current_pos])


    def _run(self,stop):
        start_time = datetime.now()
        self.target_pos = self.current_pos = start_pos = 0.00
        direction = 0
        app.logger.info(">>>>>> Press button Home")
        
        if os.name == "nt":
            subprocess.run(["sendir.bat", "L"])
        else:
            subprocess.run(["/bin/sh", sendir, "L"]) 
        
        while True:
            if stop():
                break
            
            try:
                # Create a TCP/IP socket
                sockRotctldpy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
                # Bind the socket to the address given on the command line
                server_address = (self.host, self.port)
                sockRotctldpy.bind(server_address)
                sockRotctldpy.listen(1)
        
                connRotctldpy, client_address = sockRotctldpy.accept()
                #connRotctldpy.settimeout(1)
                app.logger.info('waiting for a connection')
                
                while True:
                    data = connRotctldpy.recv(16)
                    
                    if data:    
                        # If we have asked the rotator to move calculate the current position
                        if self.current_pos != self.target_pos:
                            # How far has the rotator moved since we started
                            t_diff = datetime.now() - start_time
                            movement = t_diff.seconds * rot_speed
                            diff = self.target_pos - start_pos
                            
                            # Update the current position
                            if diff >= 0:
                                self.current_pos = round(start_pos + movement, 2)
                            else:
                                self.current_pos = round(start_pos - movement, 2)
                            
                            # Has the rotator has arrived at the target position
                            if direction == 0 and self.current_pos - self.target_pos <= 0:
                                self.current_pos = self.target_pos
                            elif direction == 1 and self.target_pos - self.current_pos <= 0:
                                self.current_pos = self.target_pos
                                
                        # Read data from antenna control
                        cmd = data.decode("utf-8").strip().split(" ")
                        
                        # Received updated coordinates
                        if cmd[0] == "P":
                          app.logger.info("Setting Az: {} El: {}".format(cmd[1],cmd[2]) )
        
                          for i, p in enumerate(rot_pos):
                              if p[1] <= float(cmd[1]) <= p[2]:
                                app.logger.info(">>>>>> Press button {}".format(p[0]))
                                if os.name == "nt":
                                    subprocess.run(["sendir.bat", p[0]])
                                else:
                                    subprocess.run(["/bin/sh", sendir, p[0]])
                                
                                # Start movement countdown
                                if self.target_pos != float(p[3]):
                                    start_time = datetime.now() 
                                    start_pos = self.current_pos
                                    self.target_pos = float(p[3])
                                    direction = 0
                                    if start_pos < self.target_pos:
                                        direction = 1
                                      
                          # Send OK
                          connRotctldpy.sendall(b"RPRT 0\n")
                        
                        # Received updated coordinates
                        if cmd[0] == "INIT":
                            app.logger.info("Received Initialise Request")
        
                            # Start movement countdown
                            if self.target_pos != float(0.0):
                                start_time = datetime.now() 
                                start_pos = self.current_pos
                                self.target_pos = float(0.0)
                                          
                            # Send OK
                            connRotctldpy.sendall(b"RPRT 0\n")
                          
                        # Received get_pos request
                        if cmd[0] == "p":
                          resp = "{}\n15.000000".format(self.current_pos)
                          app.logger.debug("Sending position: {}".format(self.current_pos))
                          
                          # Send current position
                          connRotctldpy.sendall(resp.encode('utf-8'))
                          
                        # Received stop request
                        if cmd[0] == "S":
                          # Send OK
                          connRotctldpy.sendall(b"RPRT 0\n")
    
                        if cmd[0] == "_":
                          connRotctldpy.sendall(b"rotctrld by steve\n")
                                                
                        if stop():
                            connRotctldpy.close()
     
                    else:
                        if stop():
                            connRotctldpy.close()
                            
                        break
                            
            except OSError:
                app.logger.warning("rotctldpy server not available; retry")
                time.sleep(1)
           
            finally:
                if connRotctldpy is not None:
                    connRotctldpy.close()
            
            sockRotctldpy.close()


    def close(self):
        self.stop_thread = True
        self.send_command('exit')
        self.rotctldpyThread.join()
    

class ROTCTL(object):
    """ rotctl (hamlib) communication class """
    # Note: This is a massive hack. 

    def __init__(self, hostname, port=4533, poll_rate=5, timeout=5, az_180 = False):
        """ Open a connection to rotctld, and test it for validity """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(timeout)

        self.hostname = hostname
        self.port = port
        


    def connect(self):
        """ Connect to rotctld instance """
        self.sock.connect((self.hostname,self.port))
        model = self.get_model()
        if model == None:
            # Timeout!
            self.close()
            raise Exception("Timeout!")
        else:
            return model.decode("utf-8")


    def close(self):
        self.sock.close()


    def send_command(self, command):
        """ Send a command to the connected rotctld instance,
            and return the return value.
        """
        try:
            self.sock.sendall(bytes(command+'\n', 'utf-8'))
            return self.sock.recv(1024)
        except:
            return None

    def initialise(self):
        """ Initialise rotctld """
        self.send_command('INIT')

    def get_model(self):
        """ Get the rotator model from rotctld """
        model = self.send_command('_')
        return model


    def set_azel(self,azimuth,elevation):
        """ Command rotator to a particular azimuth/elevation """
        # Sanity check inputs.
        if elevation > 90.0:
            elevation = 90.0
        elif elevation < 0.0:
            elevation = 0.0

        if azimuth > 360:
            azimuth = azimuth % 360.0


        command = "P %3.1f %2.1f" % (azimuth,elevation)
        response = self.send_command(command)
        if response is not None:
            if "RPRT 0" in response.decode("utf-8"):
                return True

        return False


    def get_azel(self):
        """ Poll rotctld for azimuth and elevation """
        # Send poll command and read in response.
        response = self.send_command('p')

        # Attempt to split response by \n (az and el are on separate lines)
        try:
            response_split = response.decode("utf-8").split('\n')
            _current_azimuth = float(response_split[0])
            _current_elevation = float(response_split[1])
            return (_current_azimuth, _current_elevation)
        except:
            app.logger.warning("Could not parse position: %s" % response)
            return (None,None)


    def halt(self):
    	""" Immediately halt rotator movement, if it support it """
    	self.send_command('S')



def createRotctl():
    global rotctldpyThread, rotator, stop_thread
    try:
        time.sleep(3)
        rotator = ROTCTL(hostname=args.host, port=args.port)
        _rot_model = rotator.connect()
        app.logger.info("Connected to rotctld - Rotator Model: " + str(_rot_model))

    except Exception as e:
        app.logger.error("Could not connect to rotctld server- %s" % str(e))
        sys.exit(1)
        
    return(rotator)
#
#   Flask Routes
#

@app.route("/")
def flask_index():
    """ Render main index page """
    connected = False
    if rotator is not None:
        connected = True
    
    return flask.render_template('index.html', connected=connected)


@app.route("/<heading>",methods = ['GET'])
def set_heading(heading):
    for p in rot_pos:
        if heading == p[0]:
            if rotator is None:
                if os.name == "nt":
                    subprocess.run(["sendir.bat", heading])
                else:
                    subprocess.run(["/bin/sh", sendir, heading])                
            else:
                current_setpoint['azimuth'] = p[3]
                current_setpoint['elevation'] = HOME_POS[1]
                rotator.set_azel(current_setpoint['azimuth'], current_setpoint['elevation'])
                update_client_display({})
            
            position = rotctldpy.get_heading()
            return("Target Heading: {}\nCurrent Heading: {}\nOK".format(position[0], position[1]))
    return("Unknown Heading")


def flask_emit_event(event_name="none", data={}):
    """ Emit a socketio event to any clients. """
    socketio.emit(event_name, data, namespace='/update_status') 


# SocketIO Handlers

@socketio.on('client_connected', namespace='/update_status')
def update_client_display(data):
    if rotator is not None:
        flask_emit_event('position_event', current_position)
        flask_emit_event('setpoint_event', current_setpoint)


@socketio.on('update_setpoint', namespace='/update_status')
def update_azimuth_setpoint(data):
    if rotator is not None:
    	_var = data['motor']
    	if _var == 'azimuth':
            if 'delta' in data:
                app.logger.info("Azimuth Setpoint:" + str(data['delta']))
                current_setpoint['azimuth'] = (current_setpoint['azimuth'] + data['delta'])%360.0
            else:
                app.logger.info("Azimuth Setpoint Fixed:" + str(data['fixed']))
                current_setpoint['azimuth'] = data['fixed']
    	elif _var == 'elevation':
            if 'delta' in data:
                app.logger.info("Elevation Setpoint:" + str(data['delta']))
                if (current_setpoint['elevation'] + data['delta']) > 90.0:
                	current_setpoint['elevation'] = 90.0
                elif (current_setpoint['elevation'] + data['delta']) < 0.0:
                	current_setpoint['elevation'] = 0.0
                else:
                	current_setpoint['elevation'] += data['delta']
            else:
                app.logger.info("Elevation Setpoint Fixed:" + str(data['fixed']))
                current_setpoint['elevation'] = data['fixed']
    	else:
    		app.logger.info("Unknown!")
    
    	rotator.set_azel(current_setpoint['azimuth'], current_setpoint['elevation'])
    	update_client_display({})


@socketio.on('home_rotator', namespace='/update_status')
def home_rotator(data):
    if rotator is not None:
    	current_setpoint['azimuth'] = HOME_POS[0]
    	current_setpoint['elevation'] = HOME_POS[1]
    	rotator.set_azel(current_setpoint['azimuth'], current_setpoint['elevation'])
    	update_client_display({})


@socketio.on('disconnect_rotator', namespace='/update_status')
def disconnect_rotator(data):
    global rotator
    rotator.close()
    rotator = None


@socketio.on('connect_rotator', namespace='/update_status')
def connect_rotator(data):
    global rotator
    rotator = createRotctl()
    
    
@socketio.on('initial_rotator', namespace='/update_status')
def initial_rotator(data):
    global rotctldpyThread, rotator, stop_thread
    if rotator is not None:
        current_setpoint['azimuth'] = HOME_POS[0]
        current_setpoint['elevation'] = HOME_POS[1]
        rotator.initialise()
        update_client_display({})
        
        if os.name == "nt":
            subprocess.run(["sendir.bat", "INITIAL"])
        else:
            subprocess.run(["/bin/sh", sendir, "INITIAL"])       
        

@socketio.on('get_connection', namespace='/update_status')
def read_connection(data):
    if rotator is not None:
        flask_emit_event('connection_event', 'connected')
    else:
        flask_emit_event('connection_event', 'disconnected')
        
        
@socketio.on('get_position', namespace='/update_status')
def read_position(data):
    if rotator is not None:
    	(_az, _el) = rotator.get_azel()
    
    	if (_az == None):
    		return
    	else:
    		current_position['azimuth'] = _az
    		current_position['elevation'] = _el
    		update_client_display({})


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--listen_port",default=5001,help="Port to run Web Server on. (Default: 5001)")
    parser.add_argument("-g", "--gui", action='store_true',help="Connect WebGUI - warning do not use in parallel with other software to control rotator")
    parser.add_argument('--host', type=str, default='localhost', help="Rotctld server host. (Default: localhost)")
    parser.add_argument('--port', type=int, default=65432, help="Rotctld server port. (Default: 65432)")
    args = parser.parse_args()

    try:
        # Start the rotctld server
        rotctldpy = ROTCTLD(host=args.host, port=args.port)
    
        # Try and connect to the rotator.
        if args.gui:
            rotator = createRotctl()
    
        # Run the Flask app, which will block until CTRL-C'd.
        socketio.run(app, host='0.0.0.0', port=args.listen_port)
    
    finally:
        # Close the rotator connection.
        if rotator is not None:
            rotator.close()
            
        rotctldpy.close()
