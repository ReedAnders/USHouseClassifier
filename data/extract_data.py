from csv import DictReader, DictWriter
import csv
import re

# votes = list(DictReader(open("../VotingData/ALABAMA1BONNER200.csv", 'r')))
# bills = list(DictReader(open("bills93-113.csv", 'r')))

votes = list(open("../VotingData/ALABAMA1BONNER200.csv", 'r'))

labels = {}
billText = {}

for line in votes:
	temp = line.split('\t')
	BoolVote = None
	# import pdb; pdb.set_trace()
	if temp[4] == 'Yea' or 'Co-sponsor':
		BoolVote = True
	if temp[4] == 'Nay':
		BoolVote = False

	if temp[1]:
		labels.update({temp[1]:BoolVote})
		billText.update({temp[1]:temp[2]})


# Save combined dictionary as CSV
o = DictWriter(open("train.csv", 'w'), ["No.", "Label", "Text"])
o.writeheader()
for key in labels:
	d = {'No.':key , 'Label':labels[key] , 'Text':billText[key]}
	o.writerow(d)