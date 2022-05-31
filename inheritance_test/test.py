class A(object):
    def fn(self):
        return "A"
        # super().fn(self)

class B(object):
    def fn(self):
        return "B"
        # super().fn(self)

class C(A, B):
    pass

class D(B, A):
    pass

print(C.__mro__)
print(D.__mro__)
assert C().fn() == "A"
assert D().fn() == "B"