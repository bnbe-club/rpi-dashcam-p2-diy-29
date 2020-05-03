import picamera
import os
import psutil
import serial
import pynmea2
import time
from picamera import Color

MAX_FILES = 999
DURATION = 20
SPACE_LIMIT = 80
TIME_STATUS_OK = 0.5

file_root = "/home/pi/videos/"
port = "/dev/serial0"

def parseGPS(str):
	if str.find('GGA') > 0:
	   msg = pynmea2.parse(str)
	   print "Timestamp: %s -- Lat: %s %s -- Lon: %s %s -- Altitude: %s %s -- Fix: %s --  Satellites: %s" % (msg.timestamp, msg.lat, msg.lat_dir, msg.lon, msg.lon_dir, msg.altitude, msg.altitude_units, msg.gps_qual,msg.num_sats)

if(psutil.disk_usage(".").percent > SPACE_LIMIT):
	print('WARNING: Low space!')
	exit()

serialPort = serial.Serial(port, baudrate = 9600, timeout = 0.5)

with picamera.PiCamera() as camera:
	camera.resolution = (1920,1080)
	camera.framerate = 30

	print('Searching files...')
	for i in range(1, MAX_FILES):
		file_number = i
		file_name = file_root + "video" + str(i).zfill(3) + ".h264"
		exists = os.path.isfile(file_name)
		if not exists:
			print "Search complete"
			break

	for file_name in camera.record_sequence(file_root + "video%03d.h264" % i for i in range(file_number, MAX_FILES)):
		timeout = time.time() + DURATION
		print('Recording to %s' % file_name)

		while(time.time() < timeout):
			gps_str = serialPort.readline()
			if gps_str.find('GGA') > 0:
				msg = pynmea2.parse(gps_str)
				camera.annotate_background = Color('black')
				camera.annotate_text = "TME:%s LAT:%s %s LON:%s %s ALT:%s %s SAT:%s CPU:%s" % (msg.timestamp, msg.lat, msg.lat_dir, msg.lon, msg.lon_dir, msg.altitude, msg.altitude_units, msg.num_sats, psutil.cpu_percent())
			
			time.sleep(TIME_STATUS_OK)
			if(psutil.disk_usage(".").percent > SPACE_LIMIT):
				print('WARNING: Low space!')
				break;
