#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# query price data from BTCChina.

from urllib import urlopen
from ast import literal_eval
import json
from timeit import Timer
import MySQLdb
import time
import yaml


config = yaml.load(open('config.yaml'))

conn = MySQLdb.connect(host=config['database']['host'],user=config['database']['username'],passwd=config['database']['password'],db =config['database']['databasename'],charset=config['database']['encoding'] )

def write_db(datas):
    try:
        cur_write = conn.cursor()
        sql =  "insert into ticker(sell, buy, last, vol, high, low) values( %s, %s, %s,%s,%s,%s)"
        cur_write.execute(sql,datas)
#{"ticker":{"high":"6989.00","low":"3998.00","buy":"5192.00","sell":"5200.00","last":"5200.00","vol":"91860.10300000"}}
        conn.commit()
        cur_write.close()
    except MySQLdb.Error,e:
        print "Mysql error %d : %s." % (e.args[0], e.args[1])
    except Exception as e:
        print("执行Mysql写入数据: %s 时出错: %s" % (sql, e))


def instance():
    # returns something like {"high":738.88,"low":689.10,"buy":713.50,"sell":717.30,"last":717.41,"vol":4797.32000000}
    remote_file = urlopen(config['btcchina']['ticker_url'])
    remote_data = remote_file.read()
    remote_file.close()
    remote_data = json.loads(str(remote_data))['ticker']
    #remote_data = {key:literal_eval(remote_data[key]) for key in remote_data}
    datas = []
    for key in remote_data:
        datas.append(remote_data[key])
    return datas

while True:
    datas = instance()
    write_db(datas)
