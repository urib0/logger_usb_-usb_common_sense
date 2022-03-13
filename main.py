#!/usr/bin/env python3
# python3.7で動作確認済み

import serial
import time
import json
import datetime
import os
import time

DEBUG = True

def logging(path, name, data):
    timestamp = datetime.datetime.now()
    filename = name + "_" + timestamp.strftime("%Y-%m-%d") + ".csv"
    write_str = timestamp.strftime("%Y/%m/%d %H:%M:%S") + "," + data
    path = path + "/" + name + "/"

    os.makedirs(path, exist_ok=True)
    f = open(path + filename, mode="a")
    f.write(write_str + "\n")
    f.close()

# 設定値読み込み
f = open("./config.json", "r")
conf = json.loads(f.read())
f.close()

path = conf["basedir"] + "/" + conf["logdir_name"]

while True:
    for device in conf["devices"]:
        readSer = serial.Serial(
            device["serial_port"], device["serial_rate"], timeout=3)
        raw = readSer.readline().decode().replace('\n', '')
        print(raw)
        readSer.close()
        logging(path, device["sensor_name"], raw)
    if not conf["interval"]:
        break
    time.sleep(conf["interval"])
