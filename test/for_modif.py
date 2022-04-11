a = list()
a.append(2)
a.append(5)
a.append(8)
a.append(0)
a.append(10)
a.append(3)
a.append(4)
a.append(11)
print(a)
for i in a:
    i += 1
print(a)
# for index in range(len(a)):
#     a[index] += 1
a = list(map(lambda x: x + 1, a))
print(a)