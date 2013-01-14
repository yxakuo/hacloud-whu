import Event
import whu_sched
import time

global scheduler
scheduler = whu_sched.scheduler(time.time,time.sleep)

event = Event.E_Init()
event = event.Gen_Event()
scheduler.enter(*event)
print scheduler.queue
scheduler.run()