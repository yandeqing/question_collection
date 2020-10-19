#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2019/8/9 10:40
'''
import hashlib

# "app_id": "up_fc8ob3tamsmc_anww",
# "app_secret": "0bf5273ebe04d15de68576f35dd39d6b"
# signature = 'HOLLYHOLLY'
import json
import time

import requests

app_id = "up_fc8og54devm1_4r0o"
app_secret = "d1094bb37cc811d2f82f5943150cb41d"
BaseURL = "https://openapi.unionpay.com/upapi/cardbintest"


def create_result(code, result, msg=None):
    return {'code': code, 'result': result, 'msg': msg}


def get_card_info(card_no):
    try:
        get = requests.get("%s/token" % BaseURL,
                           params={"app_id": app_id, "app_secret": app_secret})
        jsonres = get.json()

        if 'token' in jsonres:
            token_ = jsonres['token']
            ts = int(time.time() * 1000)
            body = {"cardNo": card_no}
            dumps = json.dumps(body)
            accessy_str = f"zuber1205{dumps}{ts}"
            sign = hashlib.sha256(accessy_str.encode('utf-8')).hexdigest()
            post = requests.post("%s/cardinfo" % BaseURL,
                                 params={"token": token_, "sign": sign, "ts": ts},
                                 json=body)
            print(post.url)
            info = post.json()
            if info["respCd"] == "0000":
                return create_result(0, info["data"]["issNm"])
            else:
                return create_result(info["respCd"], info["respMsg"])
        else:
            print(f"【get_card_info().jsonres ={jsonres}】")
    except Exception as e:
        print(f"{e}")
        return create_result(-1, f'{e}')


if __name__ == '__main__':
    info = get_card_info("6236682590000237510")
    dumps = json.dumps(info, ensure_ascii=False, indent=4)
    print(f"【main().dumps={dumps}】")
