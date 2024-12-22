from collections import OrderedDict


def caching_decorator(cache_size=None):
    def decorator(func):
        cache = OrderedDict()#словарь для хранения кэша

        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))

            if key in cache:
                return f"Из кэша {cache[key]}\n"#если результат уже есть в кэше, возвращаем его
            result = func(*args, **kwargs)#если нет - выполняем функцию
            cache[key] = result#сохраняем в кэш

            if cache_size is not None and len(cache) > cache_size:
                cache.popitem(last=False)  # удаляем самый старый кэш, если переполнение

            return result

        return wrapper

    return decorator


@caching_decorator(cache_size=2)
def func1(a):
    print("Выполняется функция func1")
    return f"{a}^2 = {a*a}\n"


@caching_decorator(cache_size=2)
def func2(a, b):
    print("Выполняется функция func2")
    return f"{a} * {b} = {a*b}\n"

#Пример использования
def testing():
    print(func1(4))#Ожидаем, что функция будет выполняться, так как кэш еще пустой
    print(func1(5))#Ожидаем, что функция будет выполняться, так как с таким параметром еще не выполнялась
    print(func1(4))#Ожидаем, что результат будет взят из кэша
    print(func1(6))#Ожидаем, что функция будет выполняться, так как с таким параметром еще не выполнялась
    print(func1(4))#Ожидаем, что функция будет выполняться, так как предыдущей записью кэш переполнился и удалилось значение для этого параметра

    print(func2(2,4))#Ожидаем, что функция будет выполняться, так как кэш еще пустой
    print(func2(2,4))#Ожидаем, что результат будет взят из кэша
    print(func2(1,4))#Ожидаем, что функция будет выполняться, так как с таким параметром еще не выполнялась
    print(func2(1,6))#Ожидаем, что функция будет выполняться, так как с таким параметром еще не выполнялась
    print(func2(2,4))#Ожидаем, что функция будет выполняться, так как предыдущей записью кэш переполнился и удалилось значение для этого параметра

if __name__ == "__main__":
    testing()