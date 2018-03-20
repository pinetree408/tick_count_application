import serial
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

cur_degree = 10
cur_dir = 1

boundary = 10
baseline = 11
twomode = 12
chunk = 13

driver = webdriver.Chrome(executable_path=r"./chromedriver")
driver.set_window_position(0, 0)
driver.set_window_size(375, 667)

driver.get('http://localhost:5000/')

driver.switch_to.frame('player')
slider = driver.find_element_by_class_name("ytp-progress-bar")
slider_width = slider.size['width']

marker = driver.find_element_by_class_name("ytp-scrubber-container")

start_flag = False

init_position = 0
prev_tick = -1;

with serial.Serial('/dev/tty.usbmodem1411', 115200) as ser:
    ser.write(bytes(str(cur_degree) + ' ' + str(chunk)  + ' ' + str(cur_dir) + '\n'))
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
                        if tick_count == 0:
                            if start_flag == False:
                                start_flag = True
                                init_position = marker.location['x']
                                ActionChains(driver).click_and_hold(marker).perform()
                        else:
                            if start_flag == True:
                                if prev_tick != tick_count:
                                    new_position = init_position + (tick_count * 3) - marker.location['x']
                                    ActionChains(driver).move_by_offset(new_position, 0).perform()
                                prev_tick = tick_count
                    if is_tap == 1:
                        if start_flag == True:
                            start_flag = False
                            init_poisition = 0
                            prev_tick = -1
                            ActionChains(driver).release(marker).perform()

driver.switch_to.default_content()
driver.close()
