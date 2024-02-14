# hamlib rotctld for infrared rotator control

* A python implementation of rotctld that by drefault listens on port 65432 and accepts rotctl commands
* Can be used with tools such as [GPredict](http://gpredict.oz9aec.net/) 
* TV rotators like the [Sharman AR 600](https://moonrakeronline.com/sharman-ar-600-vhf-uhf-antenna-rotator) 
* Threshold for rotation should be set to > 15 degrees
* Invokes a script 'sendir' to interface with IRC such as the [Flirc USB](https://flirc.com/more/flirc-usb). Assumes Flirc binaries (irtools or Flirc_utils.exe) are added to the system PATH environment. Modify this script to output alternative commands.
* <a href="https://github.com/stevendodd/rotctlpy/releases">v0.3</a> or greater contains lots of updates for Windows users
* <a href="https://github.com/stevendodd/rotctlpy/releases">v0.4</a> Refactor to remove WebGUI submodule and include by default. Use -g option to connect the WebGUI to the rotctldpy server.
* WebGUI originally written by Mark Jessop [rotctld-web-gui](https://github.com/darksidelemm/rotctld-web-gui); upgraded and modified 

### Block Diagram

<img src="./static/images/BlockDiagram.png" width=400>

### Example GPredict Integration

<img src="./static/images/RotatorConfig.png" width=400>
<p> 
<img src="./static/images/Rotator.png" width=600>

### Optional Web GUI for testing 

Connect UI with -g flag on startup. Default address `http://localhost:5001`

> [!CAUTION] 
> Do not connect if controlling rotator via other software in parallel.

<img src="./static/images/WebGUI.png" width=200>

### Installing

Requires python3

```
pip install -r requirements.txt
```

### Running rotctlpy

```
python rotator.py
```

By default this will start the rotctldpy server on `localhost:65432` and listen for rotctl commands from other software, see the Gpredict example above.

In addition a webserver is started and available at `http://localhost:5001` This is used to host the WebGUI but will also accept http requests to invoke the sendir script, regardless of if the WebGUI is connected or not. For example `http://localhost:5001/A` will send the command linked to button A.

```
192.168.1.10: $ python rotator.py --help
usage: rotator.py [-h] [-l LISTEN_PORT] [-g] [--host HOST] [--port PORT]

optional arguments:
  -h, --help            show this help message and exit
  -l LISTEN_PORT, --listen_port LISTEN_PORT
                        Port to run Web Server on. (Default: 5001)
  -g, --GUI             Connect WebGUI - warning do not use in parallel with other software to control rotator
  --host HOST           Rotctld server host. (Default: localhost)
  --port PORT           Rotctld server port. (Default: 65432)
  ```
  
### Home Assistant Integration

Can be integrated with Home Assistant using REST commands - see the examples in the home-assistant directory.

<img src="./static/images/HomeAssistant.png" width=200>