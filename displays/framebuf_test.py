from gc import mem_free, mem_alloc
import framebuf

# WIDTH = 32
# HEIGHT = 16
WIDTH = 128
HEIGHT = 64

def simulate(array):
    for y in range(HEIGHT):
        print(f"{y}\t", end="")
        for x in range(WIDTH):
            bit  = 1 << (y % 8)
            byte = array[(y // 8) * WIDTH + x]
            pixel = "#" if byte & bit else "."
            print(pixel, end="")
        print("")
    

array = bytearray(WIDTH * HEIGHT // 8)
fbuf = framebuf.FrameBuffer(array, WIDTH, HEIGHT, framebuf.MONO_VLSB)

fbuf.pixel(0, 15, 1)
fbuf.rect(0,0,128,64,1)
fbuf.text('abcdefghijklm', 1, 2, 1)
fbuf.text('nopqrstuvwxyz', 1, 10, 1)
fbuf.text('ABCDEFGHIJKLM', 1, 18, 1)
fbuf.text('NOPQRSTUVWXYZ', 1, 26, 1)
fbuf.text('0123456789+-*/', 1, 34, 1)
fbuf.text('!@#$%^&*(),.<>?', 1, 42, 1)

simulate(array)

print(f'RAM: {mem_alloc()} / {mem_free() + mem_alloc()}')
