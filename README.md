##Sending accelerometer data from Raspberry Pi to NI Mate using Python implementing websockets

###Project goal
Create a simple program in Python which gets accelerometer data from a ADXL-345 accelerometer and sends it to [NI Mate](https://ni-mate.com/) (or any other websocket server) using websockets. Was created to, in the simplest way, show how data can be sent to [NI Mate](https://ni-mate.com/) using websockets.

#####Devices used
- Raspberry Pi 3
- ADXL-345 Accelerometer

#### Software / Libraries needed
- Raspbian GNU / Linux 8 (Jessie)
- Python (2.7.9)
- ws4py
- git
- smbus

####Initial configuration
Start with connecting the accelerometer to the Raspberry Pi:

- VCC -> 5V (Pin 04) (or 3V depending on your accelerometer)
- GND -> Ground (Pin 06)
- SDA -> SDA (Pin 03, GPIO 2, SDA1, I2C)
- SCL -> SDL (Pin 05, GPIO 3, SCL1, I2C)

Next we need to enable I2C on the Raspberry Pi:

- Open Raspberry Pi configuration and under the **_Interfaces_** tab, Enable I2C and press **_"Ok"_**

Add the I2C modules to the Raspberry Pi's configuration:

- `sudo nano /etc/modules`

Add the following lines to the file, if they are not already there:

- `i2c-bcm2708`
- `i2c-dev`

After that, check that I2C is not blacklisted:

- `sudo nano /etc/modprobe.d/raspi-blacklist.conf`
- `blacklist i2c-bcm2708``` should be ```#blacklist i2c-bcm2708`

After this we can download and install the necessary libraries:

- [ws4py](http://ws4py.readthedocs.io/en/latest/sources/install/), follow the instructions
- `sudo apt-get install python-smbus i2c-tools git-core`
- [The ADXL345 module](https://github.com/pimoroni/adxl345-python), download repository

To test that the accelerometer is detected you can run:

- `sudo i2cdetect -y 1`
- The accelerometer should show up on address 53

To test that the accelerometer is working correctly we can run the program that comes with the ADXL345 module:

- `cd Download/adxl-python`
- `python adxl345.py`
- The program should run without errors and output the accelerometer data, if you shake the accelerometer while the program runs, it should print out some values either greater or less than 0.

Once we know that the accelerometer is working, we can download the project code:

- `git clone git://github.com/Pete-22/Websocket_Accelerometer/`

After this we only need to move the `adxl345.py` file from the adxl345 module folder that we downloaded earlier, to our project folder

####Using the program
- Super simple, run the python file `python websocket_accelerometer.py`
- You will then be asked to input the IP address and port number of NI Mate (or websocket server)
- Input the IP and port number according to the exaple on-screen and then press **_enter_**
- The program will wait for NI Mate to send the start message and after that it will start to send the accelerometer data
- When you want to stop sending data and the program, just stop the device from within NI Mate