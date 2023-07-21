# scrap logger

from simple_streamer import stream
from time import time
def log(_stream: object, to_console=False, filename='events.csv'):
  while 1:
    event = _stream()
    if event:
      with open(filename, 'a') as csv_file:
        csv_file.write(f'{round(time())}; {event["hash"]}; {event["logs"]}; {event["txs"]}\n')
      if to_console:
        print(event)

if __name__ == '__main__':
  log(stream, to_console=1)
