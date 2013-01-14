import threading
import time

class SimEvent(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
  def run(self):
    for i in range(100):
      start = time.time()
      #do something here
      time.sleep(0.1)
      end = time.time()
      duration = end - start
      #print 'thread execution time is ---',duration,' seconds'

if __name__=="__main__":
  maxThread = 200
  threadList = []
  for i in range(maxThread):
    threads = SimEvent()
    threadList.append(threads)
  print '\nStarting threads'
  for i in threadList:
    i.start()
  print 'All threads started'
  for i in threadList:
    i.join()
  print 'All threads waiting for exit'
