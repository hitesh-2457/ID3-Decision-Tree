def test1(a):
    """

    Args:
        a:
    """
    a.pop(0)
    # return a


def ref_demo(x):
    """

    Args:
        x:
    """
    print "x=", x, " id=", id(x)
    x += [42]
    print "x=", x, " id=", id(x)


a1 = [1, 2, 3, 4]
test1(a1)
print(a1)

print('---------------------------------------------------------------------------------------------------')
x = [41, 42, 43, 42, 41, 123, 234, 12, 21, 41]
print "x=", x, " id=", id(x)
ref_demo([xi for xi in x if xi < 43])
print "x=", x, " id=", id(x)
