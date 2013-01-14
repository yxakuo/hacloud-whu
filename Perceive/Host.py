import LibvirtConnect

class F_HostStatus(LibvirtConnect.F_LibvirtConnect):

	Host_StatusDic = {}
	LibvirtConn = LibvirtConnect.F_LibvirtConnect()

	def F_HostStatus(self):		
		Host_StatusDic.clear()
		name = 'qemu+tcp://192.168.1.110/system'
		conn = self.LibvirtConn.getConnect(name)
		if conn == False:
			Host_StatusDic[conn.getHostname()] = 0
		else:
			Host_StatusDic[conn.getHostname()] = 1
		conn.close()
	    conn = libvirt.open('qemu+tcp://192.168.1.103/system')
	    	if conn == False:
	                Host_StatusDic[conn.getHostname()] = 0
	        else:
	                Host_StatusDic[conn.getHostname()] = 1
		conn.close()


