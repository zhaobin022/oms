#encoding: utf-8
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.shortcuts import render,HttpResponse

import logging
logger = logging.getLogger('web_apps')

def permission_decorator(group_str):
    """ 
    第二种写法：带参数的装饰器 
    第二种方法可以解决 got an unexpected keyword argument 错误。 
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger.info('%s %s():' % (group_str, func.__name__))
            req = args[0]
            if group_str == 'all':
                # return render(args[0],'403.html')
                # raise PermissionDenied
                return func(*args, **kwargs)
            else:
                group_list = group_str.split('|')
                current_group = req.user.group.group_name
                if current_group in group_list:
                    return func(*args, **kwargs)
                else:
                    return render(args[0],'403.html')
        return wrapper
    return decorator
        # def decorator(func):
    #     @wraps(func)
    #     def returned_wrapper(request, *args, **kwargs):
    #         try:
    #             return func(request, *args, **kwargs)
    #         except ObjectDoesNotExist:
    #             if redirect:
    #                 return HttpResponseRedirect(redirect)
    #             else:
    #                 raise Http404()
    #     return returned_wrapper
    #
    # if not func:
    #     def foo(func):
    #         return decorator(func)
    #     return foo
    #
    # else:
    #     return decorator(func)