# http://www.saltycrane.com/blog/2010/11/fabric-post-run-processing-python-decorator/
import traceback
import logging
from functools import wraps

from fabric.api import env


# global variable for add_hooks()
parent_task_name = ''

LOG = logging.getLogger("hooks")

def add_post_run_hook(hook, *args, **kwargs):
    '''Run hook after Fabric tasks have completed on all hosts

    Example usage:
        @add_post_run_hook(postrunfunc, 'arg1', 'arg2')
        def mytask():
            # ...

    '''
    def true_decorator(f):
        return add_hooks(post=hook, post_args=args, post_kwargs=kwargs)(f)
    return true_decorator


def add_hooks(pre=None, pre_args=(), pre_kwargs={},
              post=None, post_args=(), post_kwargs={}):
    '''
    Function decorator to be used with Fabric tasks.  Adds pre-run
    and/or post-run hooks to a Fabric task.  Uses env.all_hosts to
    determine when to run the post hook.  Uses the global variable,
    parent_task_name, to check if the task is a subtask (i.e. a
    decorated task called by another decorated task). If it is a
    subtask, do not perform pre or post processing.

    pre: callable to be run before starting Fabric tasks
    pre_args: a tuple of arguments to be passed to "pre"
    pre_kwargs: a dict of keyword arguments to be passed to "pre"
    post: callable to be run after Fabric tasks have completed on all hosts
    post_args: a tuple of arguments to be passed to "post"
    post_kwargs: a dict of keyword arguments to be passed to "post"

    '''

    # create a namespace to save state across hosts and tasks
    class NS(object):
        run_counter = 0

    def true_decorator(f):
        @wraps(f)
        def f_wrapper(*args, **kwargs):
            # set state variables
            global parent_task_name
            if not parent_task_name:
                parent_task_name = f.__name__
            NS.run_counter += 1

            # pre-run processing
            if f.__name__ == parent_task_name and NS.run_counter == 1:
                if pre:
                    pre(*pre_args, **pre_kwargs)

            # run the task
            r = None
            try:
                r = f(*args, **kwargs)
            except SystemExit:
                pass
            except:
                print traceback.format_exc()

            # post-run processing
            if (f.__name__ == parent_task_name and
                NS.run_counter >= len(env.all_hosts)):
                if post:
                    post(*post_args, **post_kwargs)

            return r

        return f_wrapper

    return true_decorator
