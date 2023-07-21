# simple streamer
from requests import get
def _stream(url: str) -> object:
  return get(url, stream=True).raw.stream() 

def stream_events(url: str) -> bytes:
  for chunks in _stream(url):
    chunk = chunks.split(b'\n\n')
    for event in chunk:
      if event[:4] == b'data':
        yield event[6:] 

# keep it up
from json import loads
from requests.exceptions import ChunkedEncodingError
from logging import basicConfig, error, ERROR, debug
from time import time
basicConfig(level=ERROR)
def parse(event: bytes) -> dict:
  buff = ''
  try:
    buff = loads(event)
  except (TypeError, ValueError, ChunkedEncodingError):
    error(f'[-] Garbage chunk.. discarding\n[>] {event}')
  finally: 
    if not buff:
      buff = loads(b'{"hash": "0x0000000000000000000000000000000000000000000000000000000000000000", "logs": null, "txs": null}')
    return buff

from urllib3.exceptions import ProtocolError
def stream(goerli=False): 
  url = 'https://mev-share-goerli.flashbots.net' if goerli == True else 'https://mev-share.flashbots.net'
  last_timestamp = 0
  try:
    return parse(next(stream_events(url)))
  except (StopIteration, ConnectionError, ProtocolError):
    current_timestamp = round(time())
    if current_timestamp > last_timestamp + 5:
      debug(f'[-] A break in stream has been logged at {time()}')
      last_timestamp = current_timestamp
    pass
  except KeyboardInterrupt:     
    from sys import exit as end_process     
    end_process()

if __name__ == '__main__': 
  while 1:
    print(stream(goerli=0))
