import serial
import pynmea2

port = "/dev/serial0"

def parseGPS(str):
	if str.find('GGA') > 0:
		msg = pynmea2.parse(str)
		print "Timestamp: %s -- Lat: %s %s -- Lon: %s %s -- Altitude: %s %s -- Fix: %s --  Satellites: %s" % (msg.timestamp, msg.lat, msg.lat_dir, msg.lon, msg.lon_dir, msg.altitude, msg.altitude_units, msg.gps_qual,msg.num_sats)

serialPort = serial.Serial(port, baudrate = 9600, timeout = 0.5)
while True:
	str = serialPort.readline()
	parseGPS(str)
