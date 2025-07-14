
def t():
    print("t")


a: callable = None

if not a:
    print("not a")

a = t

a()