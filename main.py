import whu_sched
import time
import Event
scheduler = whu_sched.scheduler(time.time,time.sleep)

#event = Event.E_Init().Gen_Event()
#scheduler.enter(*event)
#scheduler.run()

import threading
import random

class SimEvent(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
  def run(self):
      #start = time.time()
      #do something here
      rnd=random.randint(0,99)
      if rnd<6:
        event = Event.E_Init().Gen_Event()
#      elif rnd <35:
#        event = Event.E_RescueVM().Gen_Event()
      else :
        event = Event.E_PerceiveVM().Gen_Event()

      scheduler.enter(*event)
      scheduler.run()
      #end = time.time()
      #duration = end - start
      #print 'thread execution time is ---',duration,' seconds'

if __name__=="__main__":
  maxThread = 360
  threadList = []
  for i in range(maxThread):
    threads = SimEvent()
    threadList.append(threads)
  print '\nStarting threads\n'
  for i in threadList:
    i.start()
    print 'thread ',i,' started\n'
  print 'All threads started'
  for i in threadList:
    i.join()
  print 'All threads waiting for exit\n'
