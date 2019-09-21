import tgapi
import requests


kuma = tgapi.bot(781791363)
dra = tgapi.bot(852069393)

no_proxy = requests.session()
no_proxy.trust_env = False
