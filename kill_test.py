import time
import threading
 
def f():
    for x in range(10):
        print "I am alive and running"
        time.sleep(0.1)
 
 
thread = threading.Thread(target=f)
thread.start()
time.sleep(0.5)
print "Stopping the thread"
thread._Thread__stop()
print "Stopped the thread"
time.sleep(1)
