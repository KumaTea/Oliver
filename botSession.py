import requests
from telegram import Bot
from botTools import query_token


kuma = Bot(query_token(781791363))
dra = Bot(query_token(852069393))

no_proxy = requests.session()
no_proxy.trust_env = False
