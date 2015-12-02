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
summary_text = []
bill = []

for row in train:
	row = row[None]

	if row[0] == 'Label':
		continue
	target.append(row[0])
	summary_text.append(row[1])


o = DictWriter(open("train_multi.csv", 'w'), ["Target", "Summary_Text"])
o.writeheader()

d = {'Target':target , 'Summary_Text':summary_text }
o.writerow(d)

