from ws4py.client.threadedclient import WebSocketClient
from threading import Thread
import json
from adxl345 import ADXL345
import time
import sys

#Connect to websocket server
#Send initial message
#Wait for start message
#When start message has been recieved, start sending data
#Stop when stop message has been received

adxl345 = ADXL345() #Initiate the accelerometer

#Next is our start message which we send to NI Mate, telling it what we will be sending
json_msg = json.loads('{ "type": "device", "value": { "device_id": "rpi_accelerometer", "device_type": "accelerometer", "name": "rpi_acc" , "values": [ { "name": "accelerometer", "type": "vec", "vec_dimension": 3 , "datatype": "float", "count": 1, "min": -20, "max": 20, "flags": "per_user" }]}}')
current_milli_time = lambda: int(round(time.time() * 1000)) #Function that we can call to get the time

cmd = { 'cmd': 0, 'pause': 0, 'started': 0}	#Keep track of when to start / stop

def get_send_data():
    start = True
    while (start):
	print "Message"
        time.sleep(0.00833) 			# delays for 8.333 milliseconds to send aroud 100 messages per second
        axes = adxl345.getAxes(True)	#Poll the accelerometer and save the data to axes
        accelerometer_data_x = (axes['x'])	
        accelerometer_data_y = (axes['y'])
        accelerometer_data_z = (axes['z'])
        json_msg_2 = '{"type": "data", "value" : {"device_id": "rpi_accelerometer", "timestamp_ms": "", "user_1": {"accelerometer" : []}}}' #Create the blank message that will later be sent
        data = json.loads(json_msg_2)	#Parse the blank message to Json so that we can input our data into the blank spots
        data["value"]["timestamp_ms"] = current_milli_time()	#Input the current time
        data["value"]["user_1"]["accelerometer"] = [accelerometer_data_x, accelerometer_data_y, accelerometer_data_z] #Input our accelerometer data
        ws.send(json.dumps(data))		#Send the data message to NI Mate / the websocket server
	while (cmd.get('pause') == 1):
	    time.sleep(1)
        if (cmd.get('cmd') == 1):		#Check to see if the stop command has been received
            start = False				#If it has, we break from the loop
    
class wsClient(WebSocketClient):
    def opened(self):
        self.send(json.dumps(json_msg))	#Send our initial message
        #print json.dumps(json_msg)		#Print the initial message, here for debugging
        
    def closed(self, code, reason=None):
        print "Closed down", code, reason

    def received_message(self, m):
        print m		#Print the message that we received, here for debugging
        if m.is_text:
            rcvd_msg = json.loads(m.data.decode("utf-8"))	#Message is recieved in a "TextMessage" format so it needs to be decoded
            if rcvd_msg['type'] == "start":		#If the message contains the "start" value
		if cmd.get('started') == 0:
			thread.start()					#Start our thread, which sends data to NI Mate
			cmd['started'] = 1
		else:
			cmd['pause'] = 0
	    elif rcvd_msg['type'] == "stop":	#if we get a "stop" message, we just pause the program
		cmd['pause'] = 1
            elif rcvd_msg['type'] == "quit":	#If the message contains the "start" value
                cmd['cmd'] = 1					#Set cmd to 1 so that the thread knows that it's time to stop
                time.sleep(2)
                ws.close()						#Close the websocket connection
                sys.exit("Program was stopped")	#Exit the program

if __name__ == '__main__':
    try:
        ip_addr = raw_input("Input the websocket IP address and port. Example: ws://192.168.1.1:9000/ \n")
        ws = wsClient(ip_addr)					#Create new client to NI Mate / the websocket server
        thread = Thread(target = get_send_data)	#Create a separate thread for sending the data
        ws.connect()							#Connect to NI Mate / the websocket server
        ws.run_forever()  
    except KeyboardInterrupt:
        start = False
        ws.close()
