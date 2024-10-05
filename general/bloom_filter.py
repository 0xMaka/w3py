# py port of an example I found here: https://ethereum.stackexchange.com/questions/142703/how-can-i-parse-an-ethereum-block-level-logsbloom
from net import con; w3 = con('MAINNET')
from hexbytes import HexBytes
keccak256 = w3.solidity_keccak

def get_num(hex_str: str, index: int, bytes_count: int = 1) -> int:
  hex_str = HexBytes(hex_str).hex()[2:]
  ost = index * 2
  return int(hex_str[ost:ost + 2 * bytes_count], 16)

def fetch_mask(topic: str) -> list:
  buf = keccak256(['bytes'], [topic])
  mask_1 = 1 << (get_num(buf, 1) & 0x7)
  mask_2 = 1 << (get_num(buf, 3) & 0x7)
  mask_3 = 1 << (get_num(buf, 5) & 0x7)

  bloom_len = 256
  pos_1 = bloom_len - ((get_num(buf, 0, 2) & 0x7FF) >> 3) - 1
  pos_2 = bloom_len - ((get_num(buf, 2, 2) & 0x7FF) >> 3) - 1
  pos_3 = bloom_len - ((get_num(buf, 4, 2) & 0x7FF) >> 3) - 1

  return [
    { 'index': pos_1, 'mask': mask_1 },
    { 'index': pos_2, 'mask': mask_2 },
    { 'index': pos_3, 'mask': mask_3 },
  ]

def maybe_topic(bloom: str, masks: list) -> bool:

  def aux(x) -> bool:
    b = get_num(bloom, x['index'])
    return (b | x['mask'] == b)

  bits_set = list(filter(lambda b : b == True, map(lambda x: aux(x), masks) ))
  return len(bits_set) == 3

if __name__ == '__main__' :
  topic = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
  logsBloom = '0x0100000000000004000000000000100000000000000000000000000000200000000000000000000000000000000001000000000000000000080008000000000040000000002000000000040800000000000000000000200000000000004800000040000002000000000000000000081000000000000040000000001080020000200001000000000000000000040000004000000000000000000000000010000000008000000000000800008000000800000000008000000200000800000000000000200a000000200000000000100002004000000000000000000000000020000000000080000020000000800000000000004000000000000000080000004000'

  print(maybe_topic(logsBloom, fetch_mask(topic)))
