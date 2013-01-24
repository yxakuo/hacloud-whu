import logging
logger = logging.getLogger('test')
hdlr = logging.FileHandler('/var/tmp/test.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

def myfunc(args):
  print args
if __name__=='__main__':
  args = 'test args'
  func = myfunc
  logger.info("%s called with args: %s",func,args)
