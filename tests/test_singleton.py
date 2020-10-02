
def test_singleton():
    from so_magic.utils import Singleton

    class ObjectRegistry(Singleton):
        def __new__(cls, *args, **kwargs):
            x = super().__new__(cls)
            if not getattr(x, 'objects', None):
                x.objects = {}
            return x

    reg1 = ObjectRegistry()
    reg1.objects['a'] = 1
    reg2 = ObjectRegistry()
    assert reg2.objects == {'a': 1}
    reg2.objects['b'] = 2
    reg3 = ObjectRegistry()

    rs = [reg1, reg2, reg3]

    assert id(reg1) == id(reg2) == id(reg3)
    for i in rs:
        print(i.objects)
        assert i.objects == {'a': 1, 'b': 2}
    assert all(x.objects == {'a': 1,
                             'b': 2} for x in rs)
    del reg3.objects['a']
    assert all(x.objects == {'b': 2} for x in rs)
    for i in rs:
        print(i.objects)
        assert i.objects == {'b': 2}
