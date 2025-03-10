from machine import Pin, I2C

class Mem24():
    
    def __init__(self, i2c, device_address, memory_size, page_size, addr_size=16):
        self.i2c = i2c
        self.device_address = device_address
        self.memory_size = memory_size
        self.page_size = page_size
        self.addr_size = addr_size
    
    def wait_for_ready(self):
        while True:
            try:
                print(".", end="")
                self.i2c.readfrom(self.device_address, 1)
                break
            except:
                pass
    
    def read(self, memory_address, length):
        self.wait_for_ready()
        return self.i2c.readfrom_mem(self.device_address, memory_address, length, addrsize=self.addr_size)
    
    def write(self, memory_address, data):
        self.wait_for_ready()
        self.i2c.writeto_mem(self.device_address, memory_address, data, addrsize=16)
    
    def write_new(self, memory_address, data):
        address_end         = memory_address + len(data) + 1    # Adres ostatniego bajtu do zapisania
        page_start_num      = memory_address // self.page_size  # Numer pierwszej strony do zapisania
        page_end_num        = address_end // self.page_size     # Numer ostatniej strony do zapisania
        page_actual_num     = page_start_num                    # Numer aktualnie zapisywanej strony
        page_actual_adr_end = None                              # Adres ostatniego bajtu w obrębie aktualnie zapisywanej strony
        actual_start        = memory_address                    # Adres pierwszego bajtu do zapisania w bieżącej transakcji
        actual_end          = None                              # Adres ostatniego bajtu do zapisania w bieżącej transakcji
        actual_length       = None                              # Liczba bajtów do zapisania w bieżącej transakcji
        
        while page_actual_num <= page_end_num:
            
            # Ustal adres ostatniego bajtu w obrębie bieżącej strony
            page_actual_adr_end = self.page_size * (page_actual_num + 1) - 1
            
            # Jeżeli adres ostatniego bajtu do zapisania jest mniejszy niż adres ostatniego bajtu strony
            # tzn. jeżeli koniec zapisu leży w obrębie strony
            if address_end <= page_actual_adr_end:
                actual_end = address_end
            else:
                actual_end = page_actual_adr_end
                
            actual_length = actual_end - actual_start + 1
            
            print(f"")
            
            """
            // Send buffer
			for(uint8 i = 0; i < ActualLength; i++) {
				if(I2C::Write(Buffer[i])) {
					I2C::Stop();
					return Error;
				}
			}
			
			// Finish transmission
			I2C::Stop();
			
			Buffer = Buffer + ActualLength;
			"""
            
            page_actual_num += 1
            actual_start = actual_end + 1
            
            
            
    
    def write_new_old(self, memory_address, data):
        
        def page_num(address):
            return address // self.page_size
        
        def page_address_begin(page_num):
            return page_num * self.page_size
        
        def page_address_end(page_num):
            return (page_num + 1) * self.page_size - 1
        
        bytes_left = len(data)
        page_now = page_num(memory_address)
        page_end = page_num(memory_address + len(data) - 1)
        data_now = 0
        data_end = len(data)
        
        print(f"Pages from {page_now} to {page_end}, data len = {len(data)}")
        
        
        while page_now <= page_end:
            
            # Ile zostało bajtów do końca bieżąceh strony
            print(f"----------")
            print(f"page_now = {page_now}")
            print(f"page_address_end(page_now) = {page_address_end(page_now)}")
            print(f"memory_address = {memory_address:04X}")
            margin = page_address_end(page_now) - memory_address + 1
            print(f"margin = {margin}")
            
            if memory_address + bytes_left - 1<= page_address_end(page_now):
                print("Zapis zmieści się w obrębie strony")
                i2c.writeto_mem(self.device_address, memory_address, data[data_now:data_now+bytes_left], addrsize=self.addr_size)
                print(f"i2c.writeto_mem({memory_address}, data[{data_now}:{data_now+bytes_left}]")
            else:
                
                
            
            data_begin = 0
            data_end   = 0
            
            i2c.writeto_mem(self.device_address, memory_address, data[data_now:data_end], addrsize=self.addr_size)
            
            # Do zapisu kolejnej strony
            page_now += 1
        
        

    
    def erase_chip(self):
        buffer = bytes(self.page_size * [0x00])
        memory_address = 0
        
        while memory_address < self.memory_size:
            self.wait_for_ready()
            self.write(memory_address, buffer)
            memory_address += self.page_size
    
    def dump(self):
        buffer = bytearray(16)
        memory_address = 0
        print("           0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F")
        
        while memory_address < self.memory_size:
            self.i2c.readfrom_mem_into(self.device_address, memory_address, buffer, addrsize=self.addr_size)
            print(f"{memory_address:08X}: ", end = "")
            for byte in buffer:
                print(f"{byte:02X} ", end="")
            for byte in buffer:
                if byte >= 32 and byte <= 127:
                    print(chr(byte), end="")
                else:
                    print(" ", end="")
            print()
            memory_address += 16
    
if __name__ == "__main__":
    i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
#   mem = Mem24(i2c, device_address=0x50, memory_size=4096, page_size=32, addr_size=16)
    mem = Mem24(i2c, device_address=0x3C, memory_size=4096, page_size=32, addr_size=16)
    
#   mem.dump()
    
    
    # zapis w obrębie jednej strony
    mem.write_new(0x0000, b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef')
    
    # zapis w obrębie dwóch stron
    
    # zapis w obrębie trzech stron
    