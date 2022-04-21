x = [[1, 2], [3, 4, 5], [1, 2, 3, 4, 5]]
l = max([len(i) for i in x])
print(l)
s = [
    "str",
]
t = []
t += s
print(t + s * 10)