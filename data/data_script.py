from csv import DictReader, DictWriter
import re

# votes = list(DictReader(open("tgraves13thcongress.csv", 'r')))
# bills = list(DictReader(open("bills93-113.csv", 'r')))

# labels = {}
# for line in votes:
# 	BoolVote = None
# 	if line['Indiv.Vote'] == 'Yea':
# 		BoolVote = True
# 	if line['Indiv.Vote'] == 'Nay':
# 		BoolVote = False
# 	if BoolVote == None:
# 		continue

# 	BillNum = re.search(r"\d+", line['Bill No.'])

# 	if BillNum:
# 		labels.update({BillNum.group():BoolVote})

# text = {}
# for line in bills:
# 	if line['Cong'] == "113":
# 		text.update({line['BillNum']:line['Title']})

# # Save combined dictionary as CSV
# o = DictWriter(open("train.csv", 'w'), ["No.", "Label", "Text"])
# o.writeheader()
# for BillNum in labels.keys():
# 	if text[BillNum]:
# 		d = {'No.':BillNum , 'Label':labels[BillNum] , 'Text':text[BillNum] }
# 		o.writerow(d)

train = list(DictReader(open("train.csv"),'r'))

target = []
data = []
bill = []

for row in train:
	row_data = []
	row = row[None]

	if row[0] == 'Label':
		continue

	target.append(row[0])

	row_data.append(row[1])
	row_data.append('IdealPointData')

	data.append(row_data)

train_count = len(data)*0.66

target_train = []
data_train = []

target_test = []
data_test = []

for ii in range(len(data)):
	if ii < train_count:
		target_train.append(target[ii])
		data_train.append(data[ii])
	else:
		target_test.append(target[ii])
		data_test.append(data[ii])

o = DictWriter(open("train_multi.csv", 'w'), ["target", "data"])
o.writeheader()

d = {'target':target_train , 'data':data_train }
o.writerow(d)


o = DictWriter(open("test_multi.csv", 'w'), ["target", "data"])
o.writeheader()

d = {'target':target_test , 'data':data_test }
o.writerow(d)

