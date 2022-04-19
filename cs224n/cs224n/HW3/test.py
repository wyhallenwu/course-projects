l = list([[1, 2], [3, 4]])
x = list([[1, 2], [3, 4], [5, 6]])
x.pop(0)
print(x)
z = zip(l, x)
for (x, y) in z:
    print(x, y)
