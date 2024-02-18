from gevent import monkey,spawn,sleep, wait
monkey.patch_all()
from hyload.stats import Stats
from hyload.logger import TestLogger
from hyload.httpclient import HttpClient


__all__ = [
    'sleep', 'Stats', 'TestLogger', 'HttpClient',
    'run_task', 'wait_for_tasks_done'
]


_task_list =[]

def run_task(target, *args, **kwargs):
    global _task_list
    _task_list.append(spawn(target, *args, **kwargs))


# def run_tasks(target, number, interval, argsList=None, kwargsList=None):
#     emptyList = []

#     if argsList and len(argsList!=number):
#         raise Exception('length of argsList not equals number')
#     if kwargsList and len(kwargsList!=number):
#         raise Exception('length of kwargsList not equals number')

#     for i in range(number):   
#         args   = argsList[i] if argsList else emptyList
#         kwargs = kwargsList[i] if kwargsList else emptyList

#         run_task(target, *args, **kwargs)
#         if i < number-1: 
#             sleep(interval) 



def wait_for_tasks_done():
    global _task_list
    wait(_task_list)
    print('\n==== all tasks end ====\n')

def wait_for_ever():
    wait()


# _task_counter = 0
# def run_task(target, *args, **kwargs):
#     """run user defined task

#     Parameters
#     ----------
#     taskFunc : _type_
#         _description_
#     number : int
#         _description_
#     interval : int or float
#         _description_
#     """

#     def wrapper(*args, **kwargs):
#         global _task_counter
#         _task_counter += 1
#         try:
#             target(*args, **kwargs)
#         finally:
#             _task_counter -=1

#     spawn(wrapper, *args, **kwargs) 


# def runTasks(taskFunc:callable, number:int, interval:float, *args, **kwargs):
#     """run user defined task

#     Parameters
#     ----------
#     taskFunc : _type_
#         _description_
#     number : int
#         _description_
#     interval : int or float
#         _description_
#     """

#     def taskWrapper(*args, **kwargs):
#         global _task_counter
#         _task_counter += 1
#         try:
#             taskFunc(*args, **kwargs)
#         finally:
#             _task_counter -=1

#     def runRoutine():

#         for i in range(number): 
#             spawn(taskWrapper,*args, **kwargs)
#             if i < number-1: # not the last one
#                 sleep(interval) 

#     if not Stats.runFlag:
#         Stats.start() 

#     # run in gevent routine, in cases client code call multiple run_task.
#     spawn(runRoutine) 


# def waitTasksDone():
#     """
#     Wait until all tasks end.

#     Here we don't use gevent.wait because I'm afraid 
#     if we have very large greenlet list to wait, that will cause performance issue
#     """
#     global _task_counter

#     # wait 1 seconds first in case first task not started, so _task_counter is still 0
#     sleep(1)

#     while _task_counter > 0:
#         sleep(1)

#     # wait 1 second for independent_check routine to send stats of last second 
#     sleep(1) 

#     print('\n==== tasks done ====')
