from operator import methodcaller
from django.db.models.manager import Manager

def _assign_to_obj(obj, **kwargs):
    for k, v in kwargs.items():
        if v is not None:
            setattr(obj, k, v)


class SimpleManagerMetaclass(type):
    def __new__(cls, name, bases, attrs, method=None, method_args=(), method_kwargs={}):
        if method is not None:
            def get_queryset(self, *args, **kwargs):
                return getattr(super(newcls, self).get_queryset(*args, **kwargs), method)(*(getattr(self, v) for v in method_args), **{k: getattr(self, v) for k, v in method_kwargs.items()})
            get_queryset.__qualname__ = f'{name}.get_queryset'
            attrs['get_queryset'] = get_queryset
        newcls = super().__new__(cls, name, bases, attrs)
        return newcls


class UsingManagerMixin(metaclass=SimpleManagerMetaclass, method='using', method_kwargs={'alias': 'using_table'}):
    using_table = None


class UsingManager(UsingManagerMixin, Manager):
    pass
