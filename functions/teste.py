# -*- coding: utf-8 -*-
import binascii
TAG_hex = '454530323630'
tag_bin = 'EE0260'
print binascii.hexlify(tag_bin).decode()
print binascii.unhexlify(TAG_hex).decode()
