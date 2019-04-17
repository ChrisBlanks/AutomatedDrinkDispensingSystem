begin = "/home/pi/PYTHON_PROJECTS/senior_design/AutomatedDrinkDispensingSystem"
end = "/AutomatedDrinkDispensingSystem/resources/system_info"

path = "{}{}/inventory_info.csv".format(begin,end)


class Inventory:
	def __init__(self,name,original_quantity,current_quantity):
		self.name = name
		self.org_quant = original_quantity
		self.cur_quant = current_quantity

	def retrieve(self):
		pass



with open(path,"r+") as inventory_file:
	content = inventory_file.readlines()
	for line in content:
		if "Inventory" in line:
			continue #skip first line
		
		print(line.replace("\n","").split(","))
		line_vals = line.replace("\n","").split(",")
		name = line_vals[0]
		current_quant= line_vals[1]
		original_quant = line_vals[2]
		ratio = float(current_quant)/float(original_quant)
		print("Quantity ratio for {}: {}".format(name,ratio))
		
		if ratio <= 0.5 :
			print("Notification: {} is half-full.".format(name))
		
		if ratio <= 0 :
			print("Notification: {} is empty.".format(name))
		
		
	#inventory_file.seek(0)
