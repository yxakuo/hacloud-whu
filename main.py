import whu_sched
import time
import Event
import sys
import threading
import random

scheduler = whu_sched.scheduler(time.time,time.sleep)

class SimEvent(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
  def run(self):
      #start = time.time()
      #do something here
#      rnd=random.randint(0,99)
#      if rnd<6:
#        event = Event.E_Init().Gen_Event()
#      elif rnd <35:
#        event = Event.E_LoopPerceive().Gen_Event()
#      else :
#        event = Event.E_PerceiveVM().Gen_Event()
      event = Event.E_Init().Gen_Event()

      scheduler.enter(*event)
      while True:
        scheduler.run()
      print 'run out\n'
      #end = time.time()
      #duration = end - start
      #print 'thread execution time is ---',duration,' seconds'

if __name__=="__main__":
  maxThread = 1
  threadList = []

#  for i in range(maxThread):
  threads = SimEvent()
  threadList.append(threads)
  #print '\nStarting threads\n'
  for i in threadList:
    i.start()
    print 'thread ',i,' started\n'
  #print 'All threads started'

  while True:
    cmd = []
    sys.stdin.flush()
    cmd = raw_input('input_command:\n').split()
  #  print cmd
    if cmd:
      time.sleep(3)
    if cmd[0] == 'r' or cmd[0]=='reset':
      if not scheduler.empty(): 
        print 'before reset ,size of queue is ',len(scheduler._queue)
        scheduler.reset()
      else:
        print 'scheduler already empty\n'

    elif cmd[0] == 'c' or cmd[0] =='cancel':
      if not scheduler.cancel(cmd[1]):
	print 'fail to cancel event %s\n',cmd[1]
      time.sleep(3)

    elif cmd[0] == 'u' or cmd[0] == 'urgent':
      if scheduler.urgent(cmd[1]):
        print 'event ',cmd[1],'is elevated to urgent.\n'
      else:
        print 'failed to elevated event ',cmd[1],' to urgent.\n'

    elif cmd[0] == 'p' or cmd[0] == 'print':
	print 'Previous queue status:\n'
	i = 0
	while i < len(scheduler._queue):
	  print scheduler._queue[i]
	  i +=1
    elif cmd [0] == 'test':
      print 'Add a test event to queue\n'
      event = Event.E_Test().Gen_Event()
      scheduler.enter(*event)
    elif cmd[0] == 'q' or cmd[0] == 'quit':
      print 'Quiting......\n'
      scheduler.reset()
      for i in threadList:
        i._Thread__stop()
      break
    elif cmd[0]:
      print 'Unkown command\n'

  for i in threadList:
    i.join()
  print 'All threads waiting for exit\n'
