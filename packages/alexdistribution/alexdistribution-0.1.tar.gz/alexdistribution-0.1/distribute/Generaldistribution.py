class Distribute:
	
	def __init__(self, mu=0, sigma=1):
	
		
		
		self.mean = mu
		self.stdev = sigma
		self.data = []


	def read_data_file(self, file_name):
	
		"""Function to read in data from a txt file. The txt file should have
		one number (float) per line. The numbers are stored in the data attribute.
				
		Args:
			file_name (string): name of a file to read from
		
		Returns:
			None
		
		"""
			
		with open(file_name) as f:
			data_list = []
			line = f.readline()
			while line:
				data_list.append(int(line))
				line = f.readline()
		f.close()
	
		self.data = data_list

