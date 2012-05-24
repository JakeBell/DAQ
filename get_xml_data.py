from lxml import etree

tree = etree.parse('settings_example.xml')
settings_file = tree.findall('inst')

#extracts the settings from an xml file and puts them in a list of dicts for each instrument
setting_list = []
for el in settings_file:
    settings_dict = {}
    inst = el.getchildren()
    for setting in inst:
        setting_name = setting.tag
        setting_value = setting.text
        settings_dict[setting_name] = setting_value
    setting_list.append(settings_dict)

#this does the same as above but is much nicer but less readable by non-python user
inst_settings_list = [dict((setting.tag, setting.text) for setting in inst) for inst in settings_file]

