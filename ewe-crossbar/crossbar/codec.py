from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession

import struct
import binascii, json

# binary payload format we use in this example:
# unsigned short + signed int + 8 bytes (all big endian)
FORMAT = '>Hl8s'


class MyCodec(ApplicationSession):


    
    @inlineCallbacks
    def onJoin(self, details):
        
        self.log.info("Started my codec")
        
        def binary_to_dict(the_binary):
            jsn = ''.join(chr(int(x, 2)) for x in the_binary.split())
            d = json.loads(jsn)  
            return d

        def decode(mapped_topic, topic, payload):
#            pid, seq, ran = struct.unpack(FORMAT, payload)
#            optionsStr = binascii.a2b_hex(payload)
            options = binary_to_dict(payload)
#            self.log.info('decode {mapped_topic}: {from_mqtt} -> {to_wamp}', mapped_topic=mapped_topic, from_mqtt=payload, to_wamp=options)

            return options

        def encode(mapped_topic, topic, args, kwargs):
            pid, seq, ran = args
            payload = struct.pack(FORMAT, pid, seq, ran)
            self.log.info('encode {mapped_topic}: {from_wamp} -> {to_mqtt}', mapped_topic=mapped_topic, from_wamp={u'args': args}, to_mqtt=payload)
            return payload

        prefix = u'com.example.mqtt'

        yield self.register(decode, u'{}.decode'.format(prefix))
        yield self.register(encode, u'{}.encode'.format(prefix))

        self.log.info("MyCodec ready!")