import time
from Lock import Wakeup_Lock
import threading

class test1(threading.Thread):
  def func1():
    print 'In func1\n'
    print 'Falling asleep\n'
    Wakeup_Lock().CloseLock()
    print 'Awaken\n'
  def __init__(self):
    threading.Thread.__init__(self)
  def run(self):
    print 'In func1\n'
    print 'Falling asleep\n'
    Wakeup_Lock().CloseLock()
    time.sleep(5)
    print 'Awaken\n'

class test2(threading.Thread):
  def func2():
    print 'In func2\n'
    while True:
      if Wakeup_Lock().IsLocked():
        print 'Try to wake the other\n'
	Wakeup_Lock().OpenLock()
	break

  def __init__(self):
    threading.Thread.__init__(self)
  def run(self):
    print 'In func2\n'
    while True:
      if Wakeup_Lock().IsLocked():
        print 'Try to wake the other\n'
	Wakeup_Lock().OpenLock()
	break
    print 'have waken the other'

if __name__=='__main__':
  thrd1 = test1()
  thrd2 = test2()
  thrd1.start()
  thrd2.start()
  thrd1.join()
  thrd2.join()
  print 'threads have exited\n'
