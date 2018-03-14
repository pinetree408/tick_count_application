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


second_unit = 616.0 / 252 

driver = webdriver.Chrome(executable_path=r"./chromedriver")
driver.get('http://localhost:5000/')

driver.switch_to.frame('player')
marker = driver.find_element_by_class_name("ytp-scrubber-container")

start_flag = False
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

                    print index_finger, middle_finger, tick_count
                    if index_finger == 1:
                        if tick_count == 0:
                            if start_flag == False:
                                start_flag = True
                                ActionChains(driver).click_and_hold(marker).perform()
                        else:
                            if start_flag == True:
                                if prev_tick != tick_count:
                                    ActionChains(driver).move_by_offset(tick_count * second_unit, 0).perform()
                                prev_tick = tick_count
                    else:
                        if start_flag == True:
                            start_flag = False
                            ActionChains(driver).release(marker).perform()

driver.switch_to.default_content()
driver.close()
