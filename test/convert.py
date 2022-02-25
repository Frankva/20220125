t = ((1, 2), (3, 4))
l = ['nombre de a', 'nombre de b']
def convert(t, l):
    rl = list()
    for tuple1 in t:
        rl.append(dict(zip(l, tuple1)))
        


    print(rl)


convert(t, l)
