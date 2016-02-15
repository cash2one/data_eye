#!/usr/bin/env python
#encoding=utf-8

import sys
import socket

localIP = socket.gethostbyname(socket.gethostname())#这个得到本地ip

if localIP == u'192.168.1.215':
	sys.path.append('/root/yanpengchen/data_eye/common')
	sys.path.append('/data2/yanpengchen/data_eye/common')
	EXECUTABLE_PATH = '/data2/yanpengchen/phantomjs-2.0.0/bin/phantomjs'
else:
	sys.path.append('/home/cyp/data_eye/common')
	EXECUTABLE_PATH = '/home/cyp/phantomjs-2.0.0/bin/phantomjs'

from get_logger import *
from define import *
from model import *

check_date = date.today()+timedelta(-3)

db_conn = new_session()

proxies = [{rc.type: u"%s:%s" % (rc.ip, rc.port)} for rc in db_conn.query(ProxyList).filter(ProxyList.status==0).filter(ProxyList.check_time>=unicode(check_date))]


def set_proxy_invalid(proxy):
	for http_type, v in proxy.iteritems():
		ip, port = v.split(u':')
		ins = db_conn.query(ProxyList).filter(ProxyList.ip==ip).filter(ProxyList.port==port).filter(ProxyList.type==http_type).first()
		if ins is not None:
			ins.status = -1
	db_conn.commit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

def get_page_source_by_phantomjs(url, delay=0.5):
	from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

	user_agent = (
	    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) " +
	    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
	)
	
	dcap = dict(DesiredCapabilities.PHANTOMJS)
	dcap["phantomjs.page.settings.userAgent"] = user_agent

	driver = webdriver.PhantomJS(desired_capabilities=dcap, executable_path=EXECUTABLE_PATH)  #这要可能需要制定phatomjs可执行文件的位置
	driver.get(url)
	sleep(delay)
	pg = driver.page_source
	driver.quit
	return pg
