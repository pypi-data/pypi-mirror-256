import json
import math
import os
import time

from websockets.sync.client import connect


def sender(fp: str, dst_id: int, url: str = 'ws://localhost:8000'):
    fp = fp.strip("'").strip('"')

    fs = os.path.getsize(fp)

    sep = '\\' if os.name == 'nt' else '/'
    fn = fp[fp.rfind(sep) + 1:] if sep in fp else fp

    fd = open(fp, 'rb')

    with connect(url, max_size=1000 * 1024 * 1024) as ws:
        data: dict = json.loads(ws.recv(timeout=1000.0))
        print(data)

        ws.send(json.dumps({
            'id': 100,
            'method': 'createSession',
            'params': {
                'fileName': fn,
                'fileSize': fs,
                'destination': dst_id,
            },
        }))
        data: dict = json.loads(ws.recv(timeout=1000.0))
        print(data)

        session: dict = data['result']['session']

        def check_apply_message(_session):
            try:
                _msg = json.loads(ws.recv(timeout=0))
            except TimeoutError:
                return

            if _msg['method'] == '_sessionChanged':
                _session |= _msg['result']['session']
                print(f'Session updated: {_session}, {blockTransmit}')

        blockTransmit = 0

        while blockTransmit < session['blockCount']:
            check_apply_message(session)

            # передано больше блоков без подтверждения чем окно
            overload = blockTransmit - session['blockReceivedAck'] > session['blockWindow']

            if not session['pauseReceiving'] and not overload:
                session_id = session['id']
                block_num = blockTransmit
                block = fd.read(session['blockSize'])
                block_s = bytes([*session_id.to_bytes(4, byteorder='big'), *block_num.to_bytes(4, byteorder='big'), *block])

                percent = math.floor(blockTransmit / session['blockCount'] * 100)

                print(f'sended [{blockTransmit}] [{percent}%]', block[:15].hex(' '), len(block_s))
                ws.send(block_s)
                blockTransmit += 1
            else:
                time.sleep(0.05)
                print('|', end='')

        print('waiting acks')

        while session['blockReceivedAck'] != (session['blockCount'] - 1):
            check_apply_message(session)
            time.sleep(0.05)
            print('|', end='')
        print()
        print('all blocks send, check receiver side')


if __name__ == "__main__":
    _fp = input('file path: ') or r"E:\Downloads\xiaomi.eu_multi_HOUJI_OS1.0.24.1.22.DEV_os1-14.zip"
    _dst_id = int(input('dst id: '))
    sender(_fp, _dst_id)
