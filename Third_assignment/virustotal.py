import virustotal3.core
import requests
import json
import os
import sys
import logging

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from configuration import conf 

VIRUS_API = conf["VIRUS_API"]
OTX_API = conf["OTX_API"]

def virustotal(query_item, query_type):
    """ virustotal api """
    result = {}
    if query_type == 'ip':
        virus_total = virustotal3.core.IP(VIRUS_API)
        result = virus_total.info_ip(query_item)
    elif query_type == 'domain':
        virus_total = virustotal3.core.Domains(VIRUS_API)
        result = virus_total.info_domain(query_item)
    elif query_type == 'url':
        virus_total = virustotal3.core.URL(VIRUS_API)
        result = virus_total.info_url(query_item)
    elif query_type == 'hash':
        virus_total = virustotal3.core.Files(VIRUS_API)
        result = virus_total.info_file(query_item)
    if 'data' in result and 'attributes' in result['data']:
        return result['data']['attributes']['last_analysis_stats']
    else:
        return result

def otx(query_item, query_type):
    """ OTX API """
    url = None

    if query_type == 'ip':
        url = f"https://otx.alienvault.com/api/v1/indicator/IPv4/{query_item}/general"
    elif query_type == 'domain':
        url = f"https://otx.alienvault.com/api/v1/indicator/hostname/{query_item}/general"
    elif query_type == 'url':
        url = f"https://otx.alienvault.com/api/v1/indicator/url/{query_item}/general"
    elif query_type == 'hash':
        url = f"https://otx.alienvault.com/api/v1/indicator/file/{query_item}/general"

    headers = {
        "X-OTX-API-KEY": OTX_API
    }

    if url:
        logging.info(f"OTX Request URL: {url}")
        response = requests.get(url, headers=headers)

        logging.info(f"OTX Response: {response.status_code}, {response.text}")

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return {"error": response.status_code, "message": "OTX 데이터베이스에서 항목을 찾을 수 없습니다."}
        else:
            return {"error": response.status_code, "message": "OTX 조회 실패"}
    else:
        return {"error": "Invalid query_type", "message": "지원되지 않는 query_type입니다."}
