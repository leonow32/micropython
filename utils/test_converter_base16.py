from converter_base16 import *

def test_bytes_to_base16_1():
    data_in  = b"\x00"
    data_out = b"00" 
    assert bytes_to_base16(data_in, "") == data_out

def test_bytes_to_base16_2():
    data_in  = b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F"
    data_out = b"000102030405060708090A0B0C0D0E0F"
    assert bytes_to_base16(data_in, "") == data_out

def test_bytes_to_base16_3():
    data_in  = b"\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA\xBB\xCC\xDD\xEE\xFF"
    data_out = b"00112233445566778899AABBCCDDEEFF"
    assert bytes_to_base16(data_in, "") == data_out
    
def test_bytes_to_base16_4():
    data_in  = b"\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA\xBB\xCC\xDD\xEE\xFF"
    data_out = b"00 11 22 33 44 55 66 77 88 99 AA BB CC DD EE FF"
    assert bytes_to_base16(data_in, " ") == data_out

def test_bytes_to_base16_5():
    data_in  = "abcd"
    data_out = b"61 62 63 64"
    assert bytes_to_base16(data_in, " ") == data_out

def test_base16_to_bytes_1():
    data_in  = "00010203040506"
    data_out = b'\x00\x01\x02\x03\x04\x05\x06'
    assert base16_to_bytes(data_in) == data_out
    
def test_base16_to_bytes_2():
    data_in  = " 00 01:02:03_04/05.06 "
    data_out = b'\x00\x01\x02\x03\x04\x05\x06'
    assert base16_to_bytes(data_in) == data_out

if __name__ == "__main__":
    import pytest
    pytest.main()
    