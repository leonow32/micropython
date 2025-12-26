from base16 import *

def test_bytes_to_base16_1():
    decoded = b"\x00"
    encoded = "00" 
    assert bytes_to_base16(decoded, "") == encoded

def test_bytes_to_base16_2():
    decoded = b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F"
    encoded = "000102030405060708090A0B0C0D0E0F"
    assert bytes_to_base16(decoded, "") == encoded

def test_bytes_to_base16_3():
    decoded = b"\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA\xBB\xCC\xDD\xEE\xFF"
    encoded = "00112233445566778899AABBCCDDEEFF"
    assert bytes_to_base16(decoded, "") == encoded
    
def test_bytes_to_base16_4():
    decoded = b"\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA\xBB\xCC\xDD\xEE\xFF"
    encoded = "00 11 22 33 44 55 66 77 88 99 AA BB CC DD EE FF"
    assert bytes_to_base16(decoded, " ") == encoded
