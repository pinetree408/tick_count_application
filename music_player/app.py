import serial
import requests

cur_degree = 10
cur_dir = 1

boundary = 10
baseline = 11
twomode = 12
chunk = 13

song_list_index = 0
artist_list_index = 0

music_list = [
    'uw_HR9jIJww', 
    '0FB2EoKTK_Q',
    'vecSVX1QYbQ',
    'MGos22_JM1U',
    'JQGRg8XBnB4',
    'v6_GwXU1lkg',
    'e3dqgC1HK1k',
    'SkN_hWI6n28',
    '2NlNEj2mCIg',
    'J_CFBjAyPWE',
    'Y2V6yjjPbX0',
]

with serial.Serial('/dev/tty.usbmodem1411', 115200) as ser:
    ser.write(bytes(str(cur_degree) + ' ' + str(twomode)  + ' ' + str(cur_dir) + '\n'))
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

                    if index_finger == 1:
                        song_list_index = tick_count
                    elif middle_finger == 1:
                        artist_list_index =  tick_count

                    if is_tap == 1:
                        print 'confirm', tick_count
                        requests.get('http://localhost:5000/play/' + music_list[tick_count])
