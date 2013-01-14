import libvirt

class F_LibvirtConnect:
	def getConnect(self,name):
		self._conn = libvirt.open(name)
		return self._conn
