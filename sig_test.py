import threading
import signal
import time
class Sim2(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
  def run(self):
    while True:
      print 'awake ',__name__
      time.sleep(5)

if __name__=='__main__':
  maxThread = 5
  threadList = []
  for i in range(maxThread):
    threads = Sim2()
    threadList.append(threads)
  print 'All threads started\n'
  for i in threadList:
    i.start()
    print 'thread ',i,'started\n'
  while True:
    cmd = raw_input('in the loop--->')
    print cmd
    if cmd == 'k':
      print 'killing threads\n'
      for i in threadList:
        i._Thread__stop()
      break
    elif cmd == 'p':
      print 'pausing thread\n'
    elif cmd == 'q':
      print 'quiting'
      break
    time.sleep(10)
  
  for i in threadList:
    i.join()
