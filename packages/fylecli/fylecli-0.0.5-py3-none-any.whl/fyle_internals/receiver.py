import json
import math
import os.path

from websockets.sync.client import connect


def receiver(url: str = 'ws://localhost:8000', dest_path: str = None):
    with connect(url, max_size=1000 * 1024 * 1024) as ws:
        data: dict = json.loads(ws.recv(timeout=10000.0))
        print(data)
        my_id = data['result']['clientId']

        print()
        print(f'My ID: {my_id}')
        print()
        print('waiting sender')

        data: dict = json.loads(ws.recv(timeout=10000.0))
        print(data)

        session: dict = data['result']['session']
        print()
        print(f'Receiving {session["fileName"]}: {round(session["fileSize"] / 1024 / 1024, 2)} MBytes, {session["blockCount"]} blocks')

        if os.path.exists(session["fileName"]):
            if not (input('File exists, overwrite? (y/[n]) ').lower() or 'n') == 'y':
                return

        f = open(dest_path or session["fileName"], 'wb')

        blockSaved = 0

        while True:
            data: dict | bytes = ws.recv()
            if isinstance(data, bytes):
                session_id = int.from_bytes(data[:4], byteorder='big')
                block_id = int.from_bytes(data[4:8], byteorder='big')
                block = data[8:]

                f.write(block)

                percent = math.floor(block_id / session['blockCount'] * 100)
                print(f'saved block [{block_id}] [{percent}%]', block[:15].hex(' '), len(block))
                blockSaved += 1

                if blockSaved - session['blockTransmittedAck'] >= session['blockWindow'] / 2 or blockSaved == session['blockCount']:
                    print(f'sended ACK for block ID {block_id}')
                    ws.send(json.dumps({
                        'id': 100,
                        'method': 'blockReceived',
                        'params': {
                            'sessionId': session['id'],
                            'blockId': block_id
                        }
                    }))
                    session['blockTransmittedAck'] = blockSaved

                if blockSaved == session['blockCount']:
                    print('all blocks received')
                    break

        print('sync data...')
        f.close()


if __name__ == "__main__":
    receiver()
