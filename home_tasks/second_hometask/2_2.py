    #         A
    #      /     \
    #     B       C
    #   /  |     /    \
    # D    |   F       G
    #   \  |   |      /
    #     E    |     /
    #       \  |    /
    #         H----
class MetaMRO(type):
    def mro(cls):
        return (cls, E,F,G,D,B,C,A, object)
class A:
    pass
class B(A):
    pass
class D(B):
    pass
class E(D,B ):
    pass
class C(A):
    pass
class F(C):
    pass
class G(C):
    pass
class H(F,E,G, metaclass=MetaMRO):
    pass

print(H.__mro__)
