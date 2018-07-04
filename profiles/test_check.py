################ MORE ABOUT PYTHON 3.7 https://realpython.com/python37-new-features/#the-breakpoint-built-in
# def divide(e, f):
#   import pdb; pdb.set_trace()
#   # breakpoint()
#   return f / e
# a, b = 0, 1
# print(divide(b, b))


a = 1+2
print(a)

var = "real" + "python"
print(var)

var = 3 * 2
print(var)

var = "python" * 3
print(var)

var = 6 % 2
print(var)

var = ("python" * 4)

print(var)

# ITERNAL OPERATIONS LIKE len()  and  []

a = 'real python'
b = [ 'Real',  'Python']

print(len(a))            ----> 11
print(a.__len__())       ----> 11
print(b[0])              ----> Real
print(b.__getitem__(0))  ----> Real
print(dir(a))
