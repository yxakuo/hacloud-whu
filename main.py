import whu_sched
import time
import Event
import sys
import threading
import random

scheduler = whu_sched.scheduler(time.time,time.sleep)

def InitFunction(args=[]):
  event = Event.E_Init().Gen_Event()
  scheduler.enter(*event)
  while True:
    scheduler.run()
#  print 'impossibly run out\n'

def InsertFunction(args=[]):
  while True:
    rnd=random.randint(0,99)
    if rnd<40:
      print 'Random insert Test event\n'
      event = Event.E_Test().Gen_Event()
    elif rnd <55:
      print 'Random insert OffAVT event\n'
      event = Event.E_Worker().Gen_Event()
    else :
      print 'Random insert PerceiveVM event\n'
      event = Event.E_PerceiveVM().Gen_Event()
#add events only,no need to scheduler.run().
#might need to consider the asynchronous conflict between threads adding events and handling events
    scheduler.enter(*event)
    time.sleep(10)
  print 'run out\n'

class SimEvent(threading.Thread):
  def __init__(self,args):
    threading.Thread.__init__(self,target=args)
#  def run(self):
      #start = time.time()
      #do something here
      #end = time.time()
      #duration = end - start
      #print 'thread execution time is ---',duration,' seconds'

if __name__=="__main__":
  maxThread = 2
  threadList = []

#  for i in range(maxThread):
# add an init event thread
  threads = SimEvent(InitFunction)
  threadList.append(threads)
# random events insert,e.g: OffAV task,Perceive series
  threads = SimEvent(InsertFunction)
  threadList.append(threads)
  print '\nStarting threads\n'
  for i in threadList:
    i.start()
    print 'thread ',i,' started\n'
  print 'All threads started'

  while True:
    cmd = []
    sys.stdin.flush()
    cmd = raw_input('input_command:\n').split()
  #  print cmd
    if cmd:
      time.sleep(3)
#reset the queue to empty
    if cmd[0] == 'r' or cmd[0]=='reset':
      if not scheduler.empty(): 
        print 'before reset ,size of queue is ',len(scheduler._queue)
        scheduler.reset()
      else:
        print 'scheduler already empty\n'
#cancel an event with a given event_id
    elif cmd[0] == 'c' or cmd[0] =='cancel':
      if not scheduler.cancel(cmd[1]):
	print 'fail to cancel event %s\n',cmd[1]
      time.sleep(3)
#elevate an event to urgent status
    elif cmd[0] == 'u' or cmd[0] == 'urgent':
      if scheduler.urgent(cmd[1]):
        print 'event ',cmd[1],'is elevated to urgent.\n'
      else:
        print 'failed to elevated event ',cmd[1],' to urgent.\n'
#print the queue status
    elif cmd[0] == 'p' or cmd[0] == 'print':
	print 'Previous queue status:\n'
        scheduler.print_queue()
#add a test event to queue
    elif cmd [0] == 'test':
      print 'Add a test event to queue\n'
      event = Event.E_Test().Gen_Event()
      scheduler.enter(*event)
#quit
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
