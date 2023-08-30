import rospy
import serial
import time
import utm
import sys
from gps_lab.msg import gps_msg
if __name__ == '__main__':
    serial_port = str(sys.argv[1])
    print(serial_port.split(","))
    SENSOR_NAME = "GPS_SENSOR"
    pub= rospy.Publisher("gps",gps_msg,queue_size=10)
    rospy.init_node('GPS_SENSOR')
    serial_baud = rospy.get_param('~baudrate',4800)
    sampling_rate = rospy.get_param('~sampling_rate',5.0)
    port = serial.Serial(serial_port, serial_baud, timeout=3.)
    rospy.sleep(0.2)        
    msg_gps=gps_msg()
    i=1
    try:
        while not rospy.is_shutdown():
            msg_gps.header.seq=i
            line = port.readline()
            line2=line.decode('latin-1')
            if line == '':
                rospy.logwarn("DEPTH: No data")
            else:
                if line2.startswith("$GPGGA") :
                    s =line2.split(",")
                    lat = s[2]
                    lon = s[4]
                    dir_lat = s[3]
                    dir_lon = s[5]
                    utc_time = s[1]
                    alt = s[9]

                    degrees_lat=int(float(lat)/100)
                    minutes_lat=float(lat)-(degrees_lat*100)
                    degrees_lon=int(float(lon)/100)
                    minutes_lon=float(lon)-(degrees_lon*100)
                    dd_lat= float(degrees_lat) + float(minutes_lat)/60
                    dd_lon= float(degrees_lon) + float(minutes_lon)/60 
                    if dir_lon == 'W':
                        dd_lon *= -1
                    if dir_lat == 'S':
                        dd_lat *= -1
 
                    utm_data=utm.from_latlon(dd_lat,dd_lon)
                    print(utm_data)
                    msg_gps.header.seq+=1
                    msg_gps.header.stamp=rospy.Time.now()
                    msg_gps.header.frame_id="GPS_MSG"
                    msg_gps.latitude=dd_lat
                    msg_gps.longitude=dd_lon
                    msg_gps.altitude=float(alt)
                    msg_gps.utm_easting=utm_data[0]
                    msg_gps.utm_northing=utm_data[1]
                    msg_gps.zone=float(utm_data[2])
                    msg_gps.letter_field=utm_data[3]
                    rospy.loginfo(msg)
                    pub.publish(msg)
    except rospy.ROSInterruptException:
        port.close()
    
    except serial.serialutil.SerialException:
        pass
