import LibvirtConnect

class F_VMStatus(LibvirtConnect.F_LibvirtConnect):

	VM_StatusDic = {}
	LibvirtConn = LibvirtConnect.F_LibvirtConnect()
	
	def F_GetVMStatus(self):
		self.VM_StatusDic.clear()
		name = 'qemu+tcp://192.168.1.110/system'
		conn = self.LibvirtConn.getConnect(name)
		if conn != False:
			VM_sumOfDomains = conn.numOfDomains()
			VM_listDefinedDomains = conn.listDefinedDomains()
			VM_number = conn.listDomainsID()
			for number in range(VM_sumOfDomains):
				dom = conn.lookupByID(VM_number[number])
				name = dom.name()
				self.F_InsertStatus(name,dom.isActive(),self.VM_StatusDic)
			for name in VM_listDefinedDomains:
				dom = conn.lookupByName(name)
				self.F_InsertStatus(name,dom.isActive(),self.VM_StatusDic)
			conn.close()

		name = 'qemu+tcp://192.168.1.103/system'
		conn = self.LibvirtConn.getConnect(name)
		if conn != False:
			VM_sumOfDomains = conn.numOfDomains()
			VM_listDefinedDomains = conn.listDefinedDomains()
			VM_number = conn.listDomainsID()
			for number in range(VM_sumOfDomains):
				dom = conn.lookupByID(VM_number[number])
				name = dom.name()
				self.F_InsertStatus(name,dom.isActive(),self.VM_StatusDic)
			for name in VM_listDefinedDomains:
				dom = conn.lookupByName(name)
				self.F_InsertStatus(name,dom.isActive(),self.VM_StatusDic)
			conn.close()

	def F_InsertStatus(self,name,status,VM_Status):
		Status = {}
		Status['isActive'] = status
		VM_Status[name] = Status

#F_VMStatus().F_GetVMStatus()
#print F_VMStatus.VM_StatusDic
