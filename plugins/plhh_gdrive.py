import requests
import json
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import re

def plhh_gdrive(gdrv_lk):
    gdrv_id = gdrv_lk.split('/')[5]
    js_web = 'https://geolocation.zindex.eu.org/api.js'
    headers = {
      'accept': '*/*',
      'accept-encoding' : 'utf-8',
      'accept-language' : 'en-US,en;q=0.9',
      'content-type' : 'application/json',
      #'origin': 'https://publiclinks.hashhackers.com',
      'referer': 'https://publiclinks.hashhackers.com/',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62'
    }
    req = requests.get(js_web, headers=headers)
    dl_tm = re.findall('[0-9]+',re.findall('downloadtime = "[0-9]+"', req.content.decode('utf-8'))[0])[0]
    dl_wrkr = re.findall('[^"]*',re.findall('".*"',re.findall('arrayofworkers = \[[^\]]*]', req.content.decode('utf-8'))[0])[0])[1]
    headers = {
      'accept': '*/*',
      'accept-encoding' : 'utf-8',
      'accept-language' : 'en-US,en;q=0.9',
      'origin': 'https://publiclinks.hashhackers.com',
      'referer': 'https://publiclinks.hashhackers.com/',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62'
    }
    plr_web = 'https://api.{}.workers.dev/info/{}?_={}'.format(dl_wrkr, gdrv_id, dl_tm)
    req = requests.get(plr_web,headers=headers)
    #print(req.content.decode('utf-8'))
    response = json.loads(req.content.decode('utf-8'))
    url = 'https://api.{}.workers.dev/download/{}'.format(dl_wrkr, gdrv_id)
    if response['name'] is not None:
        return url#response['url']
#gdrv_lk = 'https://drive.google.com/file/d/1kAT4BdsylhdPcPK4neP40IxzKrHKZ83M/view?usp=share_link'   
#print(plhh_gdrive(gdrv_lk))
