#!/usr/bin/python3

from ecdsa import SECP256k1, VerifyingKey
from ecdsa.util import sigdecode_string

import bitstring, binascii
import hashlib, bech32, re

class Bolt11:

    def decode(self, invoice):

        hrp, data = bech32.bech32_decode(str(invoice))

        assert hrp != None or data != None, 'Bad bech32 checksum.'
        assert hrp.startswith('ln'), 'Does not start with ln'

        bitarray = bitstring.BitArray()

        for x in data:
            bitarray += bitstring.pack('uint:5', x)

        assert len(bitarray) > 520, 'Too short to contain signature'

        signature = bitarray[-520:].tobytes()

        data = bitstring.ConstBitStream(bitarray[:-520])

        amount = re.search('[^\d]+', hrp[2:])

        if amount:

            amount = hrp[2 + amount.end():]

            if not amount == '':

                units = {
                    'p' : 10 ** 12, 'n' : 10 ** 9, 'u' : 10 ** 6, 'm' : 10 ** 3
                }

                unit = str(amount)[-1]

                assert re.fullmatch('\d+[pnum]?', str(amount)), f'Invalid amount {amount}'

                amount = str(amount)

                if unit in units:
                    amount = int(int(amount[:-1]) * 100000000000 / units[unit])
                else:
                    amount = int(amount) * 100000000000
        tags = {
            'payment_request' : invoice, 'amount' : amount, 'date' : data.read(35).uint,
            'route_hints' : []
        }

        while data.pos != data.len:

            tag, tag_data, data = self.pull_tagged(data)
            data_length = len(tag_data) / 5

            if tag == 'd':
                tags['description'] = self.trim_to_bytes(tag_data).decode('utf-8')

            elif tag == 'h' and data_length == 52:
                tags['description_hash'] = self.trim_to_bytes(tag_data).hex()

            elif tag == 'p' and data_length == 52:
                tags['payment_hash'] = self.trim_to_bytes(tag_data).hex()

            elif tag == 'x':
                tags['expiry'] = tag_data.uint

            elif tag == 'n':
                tags['payee'] = self.trim_to_bytes(tag_data).hex()

            elif tag == 's':
                tags['secret'] = self.trim_to_bytes(tag_data).hex()

            elif tag == 'r':

                stream = bitstring.ConstBitStream(tag_data)

                while stream.pos + 408 < stream.len:

                    tags['route_hints'].append({
                        'short_channel-id' : self.readable_scid(stream.read(64).intbe),
                        'base_fee_msat' : stream.read(32).intbe,
                        'pubkey' : stream.read(264).tobytes().hex(),
                        'cltv' : stream.read(16).intbe,
                    })

        message = bytearray([ord(x) for x in hrp]) + data.tobytes()

        if 'payee' in tags.keys():

            verify = VerifyingKey.from_string(
                binascii.unhexlify(tags['payee']), curve=SECP256k1
            )

            verify = verify.verify(signature[0:64], message, hashlib.sha256, sigdecode=sigdecode_string)

            assert verify, 'Could not verify public key'

        else:

            tags['payee'] = VerifyingKey.from_public_key_recovery(signature[0:64], message, SECP256k1, hashlib.sha256)[
                int(signature[64])
            ].to_string('compressed').hex()

        return tags

    def pull_tagged(self, stream):

        tag = stream.read(5).uint
        length = stream.read(5).uint * 32 + stream.read(5).uint
        return (bech32.CHARSET[tag], stream.read(length * 5), stream)


    def trim_to_bytes(self, data):

        return (
            data.tobytes()[:-1] if data.len % 8 != 0 else data.tobytes()
        )

    def readable_scid(self, short_channel_id: int):

        return '{0}x{1}x{2}'.format(
            ((short_channel_id >> 40) & 0xFFFFFF),
            ((short_channel_id >> 16) & 0xFFFFFF),
            (short_channel_id & 0xFFFF),
        )
