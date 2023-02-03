from requestCountApp.models import RequestCounter
from django.core.signals import request_finished
from django.dispatch import receiver


def retry(times, exceptions):
    def decorator(func):
        def fn(*args, **kwargs):
            retry_times = 0
            while retry_times < times:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    print(exceptions)
                    print(
                        'Exception thrown when attempting to run %s, retry_times '
                        '%d of %d' % (func, retry_times, times)
                    )
                    retry_times += 1
            return func(*args, **kwargs)
        return fn
    return decorator


@receiver(request_finished)
def add_request_counter(*args, **kwargs):
    obj = RequestCounter.objects.get(id=1)
    if obj:
        obj.request_count += 1
        obj.save()
    else:
        RequestCounter.objects.create(request_count=1)
