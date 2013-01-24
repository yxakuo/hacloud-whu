import logging

#log initialization
logger = logging.getLogger('whu_sched')
hdlr = logging.FileHandler('/var/tmp/whu_sched.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)
