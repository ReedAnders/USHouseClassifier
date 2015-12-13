import json
from csv import DictReader, DictWriter

train = list(DictReader(open("train.csv"),'r'))

billText = open('spider/billText_data.json','r')
billText = json.load(billText)

for ii in train:
	if ii['r'] == 'No.':
		continue

	bill = ii['r']

	for jj in billText:
		if jj.keys()[0] == bill:
			ii[None][1] = jj.values()


o = DictWriter(open("train.csv", 'w'), ["No.", "Label", "Text", "State", "Party", "NameFull"])
o.writeheader()
for index in train:
	if index['r'] == 'No.':
		continue
	_index = index[None]

	import pdb; pdb.set_trace()
	d = {'No.':index['r'] , 'Label':_index[0] , 'Text':_index[1] , 'State':_index[2] , 'Party':_index[3] , 'NameFull':_index[4]}
	o.writerow(d)

