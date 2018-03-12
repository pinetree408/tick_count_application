import serial
import requests

cur_degree = 10
cur_dir = 1

boundary = 10
baseline = 11
twomode = 12
chunk = 13

with serial.Serial('/dev/tty.usbmodem1411', 115200) as ser:
    ser.write(bytes(str(cur_degree) + ' ' + str(boundary)  + ' ' + str(cur_dir) + '\n'))
    while (True):
        first = ser.read()
        if (first == 'x'):
            if (ser.read() == 'x'):
                if (ser.read() == 'x'):
                    s = ser.readline()
                    data_list = s.split(' ')
                    index_finger = int(data_list[1])
                    middle_finger = int(data_list[2])
                    tick_count = int(data_list[3])
                    is_tap = int(data_list[5])

                    if is_tap == 1:
                        print 'confirm', tick_count
                        requests.get('http://localhost:5000/ars/' + str(tick_count))
