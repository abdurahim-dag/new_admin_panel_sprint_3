from functools import wraps
print('start')


def wait_expo(cur_sleep, max_sleep, factor,  jitter):
    """Generator for exponential decay.
     Args:
         base: The mathematical base of the exponentiation operation
         factor: Factor to multiply the exponentiation by.
         max_value: The maximum value to yield. Once the value in the
              true exponential sequence exceeds this, the value
              of max_value will forever after be yielded.
     """
    # Advance past initial .send() call
    yield  # type: ignore[misc]
    if jitter:
        value + random.random()
    n = 0
    while True:
        a = factor * base ** n
        if max_value is None or a < max_value:
            yield a
            n += 1
        else:
            yield max_value
def on_exception(
        exception,
        # base_sleep,
        # max_tries,
        # logger,
    ):
    # Декорируем с помощью wraps,
    # чтобы не потерять описание декорируемой функции.
    def retry_exception(target):
        @wraps(target)
        def retry(*args, **kwargs):
            while True:
                try:
                    ret = target(*args, **kwargs)
                except exception as e:
                    print(e)

        return retry
    return retry_exception

@on_exception(Exception)
def func():
    while True:
        print('do')
        raise Exception('excep')
func()
