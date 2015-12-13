from csv import DictReader, DictWriter
import csv, sys
import re

csv.field_size_limit(sys.maxsize)

train = list(DictReader(open("train.csv"),'r'))

target = []
data = []

for row in train:
	row_data = []
	row = row[None]

	if row[0] == 'Label':
		continue

	target.append(row[0])

	row_data.append(row[1])
	row_data.append(row[2])
	row_data.append(row[3])
	row_data.append(row[4])

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

