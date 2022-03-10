d = dict()
d['a'] = 0
d['b'] = 1
d['c'] = 2
d['d'] = 3

name_list = list()
name_list.append('b') 
name_list.append('d') 
print(d.items(), type(d.items()))
print(dict(filter(lambda element: element[0] in name_list, d.items())))