import mem_used
import micropython

# @micropython.native
@micropython.viper
def test(a: int, b: int) -> int:
# def test(a, b):
    print(f"a = {a}, type(a) = {type(a)}")
    print(f"b = {b}, type(b) = {type(b)}")
    c = a + b
    return c

output = test(1, 2)
print(output)
# output = test("1", "2")
# print(output)

mem_used.print_ram_used()