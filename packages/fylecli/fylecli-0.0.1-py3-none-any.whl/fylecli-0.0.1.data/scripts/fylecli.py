import argparse
import dataclasses
import logging
import os
import signal
import sys
from typing import Literal

import requests

from fyle_internals.sender import sender
from fyle_internals.receiver import receiver

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 1)

URL = 'wss://mark99.ru/fyle'


def verify_url(url: str, enabled_https: bool):
    url = ('wss' if enabled_https else 'ws') + '://' + (url.split('://')[1] if '://' in url else url)

    responce = requests.get(f'http{url[2:]}')
    if responce.status_code != 426:
        raise RuntimeError(f'responce code on GET {responce.status_code}, expected 426 (Upgrade Required)')

    return url


def verify_file_exists(file, must_exists: bool):
    if not must_exists and os.path.isfile(str(file)):
        raise argparse.ArgumentTypeError('file does not exists')

    if must_exists and not os.path.isfile(str(file)):
        raise argparse.ArgumentTypeError('file must be exists')

    return file


@dataclasses.dataclass
class Arguments:
    debug: bool
    https: bool
    url: str
    mode: Literal['send', 'receive'] | None

    destination_path: str | None = None

    receiver_id: str | None = None
    source_path: str | None = None


parser = argparse.ArgumentParser(
    prog='fyleft',
    description='File transfer program',
    epilog='Fyle CLI client'
)

parser.add_argument('--disable-https', dest='https', help='Disable HTTPS', action='store_false')
parser.add_argument('-d', '--debug', help='Enable debug', dest='debug', action='store_true', default=True)
parser.add_argument('--url', help='Backend websocket server', default='mark99.ru/fyle')

subparsers = parser.add_subparsers(dest='mode', help='cli mode args')

receiver_parser = subparsers.add_parser('receive', help='Receiver mode')
receiver_parser.add_argument('-d', '--destination', help='Path to saving file', dest='destination_path',
                             required=False, type=lambda _: verify_file_exists(_, False))

sender_parser = subparsers.add_parser('send', help='Sender mode')
sender_parser.add_argument('source_path', help='Path to sending file', type=lambda _: verify_file_exists(_, True))
sender_parser.add_argument('receiver_id', help='Receiver ID', type=int)

args = Arguments(**vars(parser.parse_args()))
args.url = verify_url(args.url, args.https)

logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
logging.getLogger('websockets.client').setLevel(logging.WARNING)
logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)
logging.debug(args)

try:

    args.mode = args.mode or (input('Receiver (r) or Sender (s) [r]: ') or 'r').lower()
    args.url = args.url or input(f'Backend URL [{args.url}]: ')

    if args.mode == 's': args.mode = 'send'
    if args.mode == 'r': args.mode = 'receive'

    if args.mode == 'send':
        args.source_path = args.source_path or input('File path: ')
        args.receiver_id = args.receiver_id or int(input('Destination ID: '))

except KeyboardInterrupt:
    sys.exit(0)


def exit_on_signal(*_, **__):
    print('exit_on_signal')
    sys.exit(0)


signal.signal(signal.SIGINT, exit_on_signal)
signal.signal(signal.SIGTERM, exit_on_signal)

try:
    if args.mode == 'send':
        pass
        sender(args.source_path, args.receiver_id, args.url)

    if args.mode == 'receive':
        receiver(args.url, args.destination_path)
        pass

except (Exception, RuntimeError, ImportError, EOFError, OSError, KeyError, AssertionError) as e:
    print()
    print(e, e.args)
    pass
input('Press enter to exit...')
