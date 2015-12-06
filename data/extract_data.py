from csv import DictReader, DictWriter
import re

votes = list(DictReader(open("tgraves13thcongress.csv", 'r')))
bills = list(DictReader(open("bills93-113.csv", 'r')))

labels = {}
for line in votes:
	BoolVote = None
	if line['Indiv.Vote'] == 'Yea':
		BoolVote = True
	if line['Indiv.Vote'] == 'Nay':
		BoolVote = False
	if BoolVote == None:
		continue

	BillNum = re.search(r"\d+", line['Bill No.'])

	if BillNum:
		labels.update({BillNum.group():BoolVote})

billText = {}
billState = {}
billParty = {}
billNameFull = {}

for line in bills:
	if line['Cong'] == "113":
		billText.update({line['BillNum']:line['Title']})
		billState.update({line['BillNum']:line['State']})
		billParty.update({line['BillNum']:line['Party']})
		billNameFull.update({line['BillNum']:line['NameFull']})

# Save combined dictionary as CSV
o = DictWriter(open("train.csv", 'w'), ["No.", "Label", "Text", "State", "Party", "NameFull"])
o.writeheader()
for BillNum in labels.keys():
	if billText[BillNum]:
		d = {'No.':BillNum , 'Label':labels[BillNum] , 'Text':billText[BillNum] , 'State':billState[BillNum] , 'Party':billParty[BillNum] , 'NameFull':billNameFull[BillNum]}
		o.writerow(d)