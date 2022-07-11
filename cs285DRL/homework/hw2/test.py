import numpy as np

x = np.random.randint(3, 10, [5])
y = np.random.randint(3, 10, [5])
print(x.ndim)
t = np.random.randint(3, 10, [5, 5, 5, 5])
print(t.ndim)
z = (x - np.mean(x)) / np.std(x)
print(np.mean(x), np.std(x))
print(np.mean(z), np.std(z))