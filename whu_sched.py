"""A generally useful event scheduler class.

Each instance of this class manages its own queue.
No multi-threading is implied; you are supposed to hack that
yourself, or use a single instance per application.

Each instance is parametrized with two functions, one that is
supposed to return the current time, one that is supposed to
implement a delay.  You can implement real-time scheduling by
substituting time and sleep from built-in module time, or you can
implement simulated time by writing your own functions.  This can
also be used to integrate scheduling with STDWIN events; the delay
function is allowed to modify the queue.  Time can be expressed as
integers or floating point numbers, as long as it is consistent.

Events are specified by tuples (time, priority, action, argument).
As in UNIX, lower priority numbers mean higher priority; in this
way the queue can be maintained as a priority queue.  Execution of the
event means calling the action function, passing it the argument
sequence in "argument" (remember that in Python, multiple function
arguments are be packed in a sequence).
The action function may be an instance method so it
has another way to reference private data (besides global variables).
"""

# XXX The timefunc and delayfunc should have been defined as methods
# XXX so you can define new kinds of schedulers using subclassing
# XXX instead of having to define a module or class just to hold
# XXX the global state of your particular time and delay functions.

import heapq
from collections import namedtuple
from Lock import Wakeup_Lock
import Event
import Handle
import time
__all__ = ["scheduler"]

import logging
logger = logging.getLogger('whu_sched')
hdlr = logging.FileHandler('/var/tmp/whu_sched.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

Event = namedtuple('Event', 'time, priority, handle, argument, uid, description')

class scheduler:
    _queue = []
    
    def __init__(self, timefunc, delayfunc):
        """Initialize a new instance, passing the time and delay
        functions"""
        
        self.timefunc = timefunc
        self.delayfunc = delayfunc

    def enterabs(self, time, priority, action, argument, uid,description):
        """Enter a new event in the queue at an absolute time.

        Returns an ID for the event which can be used to remove it,
        if necessary.

        """
        event = Event(time, priority, action, argument, uid,description)
        heapq.heappush(scheduler._queue, event)
        return event # The ID

    def enter(self, delay, priority, action, argument, uid,description):
        """A variant that specifies the time as a relative time.

        This is actually the more commonly used interface.

        """
        time = self.timefunc() + delay
        return self.enterabs(time, priority, action, argument, uid,description)

    def cancel(self, event_id):
        """Remove an event from the queue.

        This must be presented the ID as returned by enter().
        If the event is not in the queue, this raises ValueError.

        """
        i=0
	deleted = False
	print 'event %s', event_id,' to be canceled\n'
        while i < len(scheduler._queue):
	  print i,'th event in queue is',scheduler._queue[i][4]
	  if scheduler._queue[i][4]==int(event_id):
	    print 'event ',event_id,' is queuing\n'
	    time.sleep(3)
            scheduler._queue.remove(scheduler._queue[i]) 
	    deleted = True
            break
          i = i+1
	if deleted:
	  i = 0
          while i < len(scheduler._queue):
	    print i,'th event in queue is',scheduler._queue[i][4]
	    i +=1
          heapq.heapify(scheduler._queue)
	else:
	  msg = 'fail to cancel event %s'
	  #logger.error(msg,event_id)
	  print msg %event_id

    def empty(self):
        """Check whether the queue is empty."""
        return not scheduler._queue

    def run(self):
        """Execute events until the queue is empty.

        When there is a positive delay until the first event, the
        delay function is called and the event is left in the queue;
        otherwise, the event is removed from the queue and executed
        (its action function is called, passing it the argument).  If
        the delay function returns prematurely, it is simply
        restarted.

        It is legal for both the delay function and the action
        function to modify the queue or to raise an exception;
        exceptions are not caught but the scheduler's state remains
        well-defined so run() may be called again.

        A questionable hack is added to allow other threads to run:
        just after an event is executed, a delay of 0 is executed, to
        avoid monopolizing the CPU when other threads are also
        runnable.

        """
        # localize variable access to minimize overhead
        # and to improve thread safety
        q = scheduler._queue
        delayfunc = self.delayfunc
        timefunc = self.timefunc
        pop = heapq.heappop
        def print_empty():
            print 'empty'
        
        while q:
	    i = 0
            while i < len(q):
	      print i,'th event in queue is',q[i][4]
	      i +=1
            if len(q)==0:
		print 'Empty queue\n'
                self.enter(1,10,print_empty,(),99999,'kkk')
	    checked_event = q[0]
            time, priority, action, argument,uid,description = checked_event
            now = timefunc()
	    if time > now:
	      Wakeup_Lock().CloseLock()
            while time > now and Wakeup_Lock().IsLocked():
	      now = timefunc()
              delayfunc(1)
	      print 'event %s handle %s description %s Sleeping\n' %(uid,action,description)
            else:
		if Wakeup_Lock().IsLocked():
		  Wakeup_Lock().OpenLock()
                event = pop(q)
                # Verify that the event was not removed or altered
                # by another thread after we last looked at q[0].
                if event is not checked_event and event[5] == 'URG':
		  msg = 'Urgent event %s  arrived'
		  logger.debug(msg,event[4])
		  logger.info("event %s %s called with args: %s",event[4],event[2],event[3])
                  event[2](*event[3])
                  delayfunc(0)   # Let other threads run
		elif event is checked_event:
		  logger.info("event %s %s called with args: %s",uid,action,argument)
                  action(*argument)
                  delayfunc(0)   # Let other threads run
                else:
                  heapq.heappush(q, event)
	print 'Empty Queue'

    def reset(self):
      event =Event(1,0,Handle.H_Init().handle,(),0,'NEWINIT')
      scheduler._queue = [event]
      print 'Queue reset\n'
      #E_Base._Event_Uid = 0

    def urgent(self,event_id):
      msg = "Try to elevate event %s to urgent"
      i = 0
      while i<len(scheduler._queue): 
        if scheduler._queue[i][4] == int(event_id):
          break;
	else:
	  i += 1
      if i == len(scheduler._queue):
	err = 'Can not find event %s'
        #logger.error(err,event_id)
	print err %event_id
	return False 
      else:  
        (tmp,tmp,handle,argument,uid,tmp) = scheduler._queue[i]
        scheduler._queue.remove(scheduler._queue[i]) 
	event = Event(0,0,handle,argument,uid,'URG')
	heapq.heappush(scheduler._queue,event)
	if Wakeup_Lock().IsLocked():
	  Wakeup_Lock().OpenLock()
	print 'after urgent insert\n'
	i = 0
        while i < len(scheduler._queue):
	  print i,'th event in queue is',scheduler._queue[i][4]
	  i +=1
	time.sleep(5)
        logger.debug(msg,event_id)
        print msg %event_id
	return True

    @property
    def queue(self):
        """An ordered list of upcoming events.

        Events are named tuples with fields for:
            time, priority, action, arguments

        """
        # Use heapq to sort the queue rather than using 'sorted(self._queue)'.
        # With heapq, two events scheduled at the same time will show in
        # the actual order they would be retrieved.
        events = scheduler._queue[:]
        return map(heapq.heappop, [events]*len(events))
    
    def wakeup(self,event):
        """This function is used to wakeup an event,
         Events are named tuples with fields for:
            time, priority, action, arguments
        """
        self.cancel(event)
        priority,action,argument = event[1:]
        self.enter(0,priority,action,argument)
