import PyBindTest as m
import time

print(m._core.meta)

# start = time.perf_counter()
# for i in range(1000000):
#     m.add(10000, 20000,)
# print(f'cost:{time.perf_counter() - start:.6f}')
#
# start = time.perf_counter()
# for i in range(1000000):
#     10000 + 20000
# print(f'cost:{time.perf_counter() - start:.6f}')
