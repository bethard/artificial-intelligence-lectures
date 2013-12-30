import itertools

"""
1	1.000
2	1.414
3	1.732
4	2.000
5	2.236
6	2.449
7	2.646
8	2.828
9	3.000
...
"""

def newton(x, tolerance=1e-10):
    orig = x
    for i in itertools.count():
        new_x = 0.5 * (x + orig / x)
        if abs(x - new_x) < tolerance:
            return new_x
        x = new_x

for i in xrange(1, 10):
    print i, newton(i)