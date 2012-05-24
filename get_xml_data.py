from lxml import etree

def get_settings_list(filename):
	"""
	Takes in an xml filename string and returns a list of dictionaries containing settings for each instrument
	"""
	
	tree = etree.parse(filename)
	settings_file = tree.findall('inst')
	inst_settings_list = [dict((setting.tag, setting.text) for setting in inst) for inst in settings_file]
	return inst_settings_list
