import os
import sys
import datetime
import ssl
import asyncio
import logging
import json
import subprocess
from threading import Event
import requests
from slack_sdk.web import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from sqlalchemy.orm import Session
from database import get_db
from models import Friend

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from configuration import conf
from virustotal import virustotal, otx

logging.basicConfig(level=logging.INFO)

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

BOT_TOKEN = conf['bot_token']
SOCKET_TOKEN = conf['bot_socket']
BOTNAME = 'bot'

ALLOW_USERS = ['U05K140HSUQ','']

SLACK_CLIENT = SocketModeClient(
    app_token=SOCKET_TOKEN,
    web_client=WebClient(token=BOT_TOKEN, ssl=ssl_context)
)

def get_friend_info(friend_name: str, db: Session):
    return db.query(Friend).filter(Friend.name == friend_name).first()

def process(client: SocketModeClient, req: SocketModeRequest):
    logging.info(f"Received request: {req.type}")
    
    if req.type == "events_api":
        logging.info(f"Received event: {req.payload['event']}")

        response = SocketModeResponse(envelope_id=req.envelope_id)
        client.send_socket_mode_response(response)
        
        if req.payload["event"]["type"] == "message" and req.payload["event"].get("subtype") is None:
            text = req.payload["event"]["text"].strip()
            logging.info(f"Received message: {text}")
            channel = req.payload["event"]["channel"]
            
            if text.startswith("IoC"):
                try:
                    parts = text.split()
                    if len(parts) >= 3:
                        query_type = parts[1]
                        query_item = parts[2]
                        logging.info(f"Query Type: {query_type}, Query Item: {query_item}")
                        
                        vt_result = virustotal(query_item, query_type)
                        otx_result = otx(query_item, query_type)
                        
                        response_message = (
                            f"*VirusTotal 결과*\n```{json.dumps(vt_result, indent=2)}```\n"
                            f"*OTX 결과*\n```{json.dumps(otx_result, indent=2)}```"
                        )
                        logging.info(f"Sending response: {response_message}")
                        
                        response = client.web_client.chat_postMessage(
                            channel=channel,
                            text=response_message
                        )
                        logging.info(f"Slack API response: {response}")
                    else:
                        logging.error("Invalid IoC message format.")
                except Exception as e:
                    logging.error(f"Error processing IoC query: {e}")
           
            elif text.startswith("BoBWiki"):
                try:
                    friend_name = text.split()[1]
                    db = next(get_db()) 
                    try:
                        friend_info = get_friend_info(friend_name, db)
                        if friend_info:
                            response_message = f"{friend_info.name}: {friend_info.description}"
                        else:
                            response_message = "해당 친구를 찾을 수 없습니다."
                    finally:
                        db.close()
                    
                    client.web_client.chat_postMessage(
                        channel=channel,
                        text=response_message
                    )
                except Exception as e:
                    logging.error(f"Error processing BoBWiki query: {e}")
    else:
        logging.info(f"Unhandled request type: {req.type}")

if __name__ == "__main__":
    try:
        SLACK_CLIENT.socket_mode_request_listeners.append(process)
        logging.info("Bot is starting...")
        SLACK_CLIENT.connect()
        logging.info("Bot connected and running...")
        Event().wait()
    except Exception as main_e:
        logging.error(f"Error in main: {main_e}")
