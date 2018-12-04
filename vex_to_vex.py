#! /usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import sys
import os

#------------------------------------------#
# default parameter
#------------------------------------------#

#---------- set start observation time ----------#
#---------- set any time(Set time JST) ----------#
start_time_flag = "any_time_vex"
any_time = "2016y136d14h12m00s"

#---------- set after time ----------#
#start_time_flag = "after_time"
after_day = 10
after_hour = 0
after_minute = 0

#---------- time of Move antenna ----------#
TIME_MOVE_ANTENNA = 1200

#---------- vex file name ----------#
vex_file_name = "a18075a_r1.vex"
write_vex_file_name = "sample.vex"


#-------------------------------------------#


def str_time_to_time(str_time):
	month = str(datetime.date(int(str_time[0:4]), 1, 1) + datetime.timedelta(days=int(str_time[5:8])-1))[5:7]
	day = str(datetime.date(int(str_time[0:4]), 1, 1) + datetime.timedelta(days=int(str_time[5:8])-1))[8:10]
	time_list = [str_time[0:4], month, day, str_time[9:11], str_time[12:14], str_time[15:17]]
	return time_list


def time_plus_or_minus(str_time1, str_time2):
	ye = (int(str_time1.year) - int(str_time2.year))
	mo = (int(str_time1.month) - int(str_time2.month))
	da = (int(str_time1.day) - int(str_time2.day))
	ho = (int(str_time1.hour) - int(str_time2.hour))
	mi = (int(str_time1.minute) - int(str_time2.minute))
	se = (int(str_time1.second) - int(str_time2.second))
	porm = int((str_time1-str_time2).days)

	#porm = ye + mo + da + ho + mi +se

	if porm >= 0:
		return 1
		"""
		ptmp = 3600*ho + 60*mi +se
		if ptmp > 0:
			return 1
		else:
			return -1
		"""
	else:
		return -1


args = sys.argv
#param_data = open("param.txt", "r")
param_data = open(args[1], "r")
data_list = param_data.readlines()
for data in data_list:
	if "#" != data[0]:
		if "USER_NAME" == data.strip()[0:9]:
			# USER_NAME = data.split('=')[1][:-1]
			USER_NAME = data.split('=')[1].split()[0]
		if "PROJECT_NAME" == data.strip()[0:12]:
			PROJECT_NAME = data.split('=')[1].split()[0]
		if "Station_Name" == data.strip()[0:12]:
			Station_Name = data.split('=')[1].split()[0]
		if "start_time_flag" == data.strip()[0:15]:
			start_time_flag = data.split('=')[1].split()[0]
		if "any_time" == data.strip()[0:8]:
			any_time = data.split('=')[1].split()[0]
		if "after_day" == data.strip()[0:9]:
			after_day = int(data.split('=')[1].split()[0])
		if "after_hour" == data.strip()[0:10]:
			after_hour = int(data.split('=')[1].split()[0])
		if "after_minute" == data.strip()[0:12]:
			after_minute = int(data.split('=')[1].split()[0])
		if "TIME_MOVE_ANTENNA" == data.strip()[0:17]:
			TIME_MOVE_ANTENNA = int(data.split('=')[1].split()[0])
		if "vex_file_name" == data.strip()[0:13]:
			vex_file_name = data.split('=')[1].split()[0]
		if "write_vex_file_name" == data.strip()[0:19]:
			write_vex_file_name = data.split('=')[1].split()[0]
		if "after_mmc" == data.strip()[0:9]:
			after_mmc = int(data.split('=')[1].split()[0])
		if "before_observation" == data.strip()[0:18]:
			before_observation = int(data.split('=')[1].split()[0])
		if "time_of_second_move" == data.strip()[0:19]:
			time_of_second_move = int(data.split('=')[1].split()[0])
		if "start_file_flag" == data.strip()[0:15]:
			start_file_flag  = data.split('=')[1].split()[0]
		if "start_file_name" == data.strip()[0:15]:
			start_file_name  = data.split('=')[1].split()[0]
		if "error_flag" == data.strip()[0:10]:
			error_flag  = data.split('=')[1].split()[0]

	else:
		pass


#data_listにvexデータを抜き出した。
#vex_data = open("a18075a_r1.vex", "r")
#vex_data = open("k18hi01d_180507_kvn.vex", "r")
vex_data = open(vex_file_name, "r")
data_list = vex_data.readlines()



#各$のindexを抜き出す。
title_list = ["$GLOBAL;", "$EXPER;", "$MODE;", "$STATION;", "$PROCEDURES;", "$SITE;", "$ANTENNA;", "$DAS;", "$SOURCE;", "$FREQ;", "$IF;", "$BBC;", "$PHASE_CAL_DETECT;", "$SCHED;"]
title_index = [len(data_list)]
#$を見つけて、indexをtitle_indexに収納、
for data in data_list:
	if data.strip() in title_list:
		title_index.append(data_list.index(data))
title_index.sort()



#-------------------------------------------------#
#  GLOBAL
#-------------------------------------------------#
#$GLOBALを分解する。
GLOBAL_INDEX_START = 0
GLOBAL_INDEX_END = 0
for data in data_list:
	if data.strip() in "$GLOBAL;":
		GLOBAL_INDEX_START = data_list.index(data)
		GLOBAL_INDEX_END = title_index[title_index.index(GLOBAL_INDEX_START)+1]
#print GLOBAL_INDEX_START, GLOBAL_INDEX_END

GLOBAL_DATA = data_list[GLOBAL_INDEX_START:GLOBAL_INDEX_END]
#print GLOBAL_DATA  #この中に$GLOBAL;の中身が書いてある。


Observation_Name = ""
#何に入れるかは別として、ここに$EXPERの観測ネームがある。
for data in GLOBAL_DATA:
	if "$EXPER" in data.split():
		Observation_Name = data.split()[-1]
		#print Observation_Name


#-------------------------------------------------#
#  EXPER
#-------------------------------------------------#
#$EXPERを分解する。
OBSERVATION_START_TIME = 0
EXPER_INDEX_START = 0
EXPER_INDEX_END = 0
for data in data_list:
	if data.strip() in "$EXPER;":
		EXPER_INDEX_START = data_list.index(data)
		EXPER_INDEX_END = title_index[title_index.index(EXPER_INDEX_START)+1]
#print EXPER_INDEX_START, EXPER_INDEX_END

EXPER_DATA = data_list[EXPER_INDEX_START:EXPER_INDEX_END]
#print EXPER_DATA  #この中に$EXPER;の中身が書いてある。



#何に入れるかは別として、ここに$EXPERの観測ネームがある。
for data in EXPER_DATA:
	if  "exper_nominal_start" in data[5:24]:
		OBSERVATION_START_TIME = data[25:-1]
		#print OBSERVATION_START_TIME
	if  "exper_nominal_stop" in data[5:23]:
		OBSERVATION_STOP_TIME = data[24:-1]



#-------------------------------------------------#
#  SOURCE
#-------------------------------------------------#
#$SOURCEを分解する。
SOURCE_INDEX_START = 0
SOURCE_INDEX_END = 0
for data in data_list:
	if data.strip() in "$SOURCE;":
		SOURCE_INDEX_START = data_list.index(data)
		SOURCE_INDEX_END = title_index[title_index.index(SOURCE_INDEX_START)+1]
#print SOURCE_INDEX_START, SOURCE_INDEX_END

SOURCE_DATA = data_list[SOURCE_INDEX_START+1:SOURCE_INDEX_END]
#print SOURCE_DATA

count = 0
SOURCE_Start_index = []
SOURCE_End_index = []
for data in SOURCE_DATA:
	if "def" == data.strip()[0:3]:
		SOURCE_Start_index.append(count)
	elif "enddef" == data.strip()[0:6]:
		SOURCE_End_index.append(count)
	count += 1
SOURCE_Start_index.sort()
SOURCE_End_index.sort()


SOURCE_LIST = []

for i in range(len(SOURCE_Start_index)):
	SOURCE_TEXT = ""
	tmpSOURCE = SOURCE_DATA[SOURCE_Start_index[i]:SOURCE_End_index[i]]
	for data in tmpSOURCE:
		if "*" != data[0]:
			SOURCE_TEXT = SOURCE_TEXT + data

	tmpSOURCE = SOURCE_TEXT.split(';')
	for data in tmpSOURCE:
		#観測天体名
		if "source_name=" in ''.join(data.split()):
			SOURCE_LIST.append([])
			SOURCE_LIST[i].append(''.join(data.split())[12:])
			#print ''.join(data.split()).strip('source_name=')
		if "ra=" in ''.join(data.split()):
			SOURCE_LIST[i].append(''.join(data.split())[3:])
			#print ''.join(data.split()).strip('ra=')
		if "dec=" in ''.join(data.split()):
			SOURCE_LIST[i].append(''.join(data.split())[4:])
			#print ''.join(data.split()).strip('ra=')
		if "ref_coord_frame=" in ''.join(data.split()):
			SOURCE_LIST[i].append(''.join(data.split())[16:])




#-------------------------------------------------#
#  FREQ
#-------------------------------------------------#
#$FREQを分解する。
FREQ_INDEX_START = 0
FREQ_INDEX_END = 0
for data in data_list:
	if data.strip() in "$FREQ;":
		FREQ_INDEX_START = data_list.index(data)
		FREQ_INDEX_END = title_index[title_index.index(FREQ_INDEX_START)+1]
#print FREQ_INDEX_START, FREQ_INDEX_END

FREQ_DATA = data_list[FREQ_INDEX_START:FREQ_INDEX_END]
#print FREQ_DATA  #この中に$FREQ;の中身が書いてある。

for data in FREQ_DATA:
	#周波数
	if "chan_def" in data.split():
		#print data.split()[2], "=", data.split()[3], "MHz"
		#print data.split()[5], "=", data.split()[6], "MHz"
		#print data.split()[8], "=", data.split()[10], data.split()[12], data.split()[13]
		pass


#-------------------------------------------------#
#  SCHED
#-------------------------------------------------#
#$SCHEDを分解する。
SCHED_INDEX_START = 0
SCHED_INDEX_END = 0
for data in data_list:
	if data.strip() in "$SCHED;":
		SCHED_INDEX_START = data_list.index(data)
		SCHED_INDEX_END = title_index[title_index.index(SCHED_INDEX_START)+1]


SCHED_DATA = data_list[SCHED_INDEX_START:SCHED_INDEX_END]
#print SCHED_DATA  #この中に$SCHED;の中身が書いてある。
count = 0
SCHED_Start_index = []
SCHED_End_index = []
for data in SCHED_DATA:
	if "scan" == data.strip()[0:4]:
		SCHED_Start_index.append(count)
	elif "endscan" == data.strip()[0:7]:
		SCHED_End_index.append(count)
	count += 1
SCHED_Start_index.sort()
SCHED_End_index.sort()



Station_Name_ANT = ""
SCHED_LIST = []
for i in range(len(SCHED_Start_index)):
	SCHED_TEXT = ""
	tmpSCHED = SCHED_DATA[SCHED_Start_index[i]:SCHED_End_index[i]]
	for data in tmpSCHED:
		if "*" != data[0]:
			SCHED_TEXT = SCHED_TEXT + data


	Station_Name_ANT = "station=" + Station_Name
	tmpSCHED = SCHED_TEXT.split(';')
	for data in tmpSCHED:
		if "scan" in ''.join(data.split())[0:5]:
			SCHED_LIST.append([0, 0, 0, 0])
		if "start=" in ''.join(data.split()):
			#SCHED_LIST.append([])
			SCHED_LIST[i][0] = ''.join(data.split())[6:]
			#print ''.join(data.split()).strip('start=')
		if "mode=" in ''.join(data.split()):
			SCHED_LIST[i][1] = ''.join(data.split())[5:]
			#print ''.join(data.split()).strip('mode=')
		if "source=" in ''.join(data.split()):
			SCHED_LIST[i][2] = ''.join(data.split())[7:]
			#print ''.join(data.split()).strip('source=')
		if "source1=" in ''.join(data.split()):
			SCHED_LIST[i][2] = ''.join(data.split())[8:]
			#print ''.join(data.split()).strip('source1=')
		if Station_Name_ANT in ''.join(data.split()):
			SCHED_LIST[i][3] = ''.join(data.split())[8:]
			#print ''.join(data.split()).strip('station=Vm')


#-------------------------------------------------#
#  MODE
#-------------------------------------------------#
#$MDOEを分解する。
MODE_INDEX_START = 0
MODE_INDEX_END = 0
for data in data_list:
	if data.strip() in "$MODE;":
		MODE_INDEX_START = data_list.index(data)
		MODE_INDEX_END = title_index[title_index.index(MODE_INDEX_START)+1]
#print MODE_INDEX_START, MODE_INDEX_END

MODE_DATA = data_list[MODE_INDEX_START+1:MODE_INDEX_END]
#print MODE_DATA

count = 0
MODE_Start_index = []
MODE_End_index = []
for data in MODE_DATA:
	if "def" == data.strip()[0:3]:
		MODE_Start_index.append(count)
	elif "enddef" == data.strip()[0:6]:
		MODE_End_index.append(count)
	count += 1
MODE_Start_index.sort()
MODE_End_index.sort()


MODE_LIST = []

for i in range(len(MODE_Start_index)):
	MODE_TEXT = ""
	tmpMODE = MODE_DATA[MODE_Start_index[i]:MODE_End_index[i]]
	for data in tmpMODE:
		if "*" != data[0]:
			MODE_TEXT = MODE_TEXT + data

	tmpMODE = MODE_TEXT.split(';')
	for data in tmpMODE:
		if "def" in ''.join(data.split()):
			MODE_LIST.append([])
			MODE_LIST[i].append(data.split()[1])
		if "PROCEDURES=" in ''.join(data.split()):
			MODE_LIST[i].append(''.join(data.split()).replace('=', ':').split(':')[1])


#-------------------------------------------------#
#  PROCEDURES
#-------------------------------------------------#
#$PROCEDURESを分解する。
PROCEDURES_INDEX_START = 0
PROCEDURES_INDEX_END = 0
for data in data_list:
	if data.strip() in "$PROCEDURES;":
		PROCEDURES_INDEX_START = data_list.index(data)
		PROCEDURES_INDEX_END = title_index[title_index.index(PROCEDURES_INDEX_START)+1]
#print PROCEDURES_INDEX_START, PROCEDURES_INDEX_END

PROCEDURES_DATA = data_list[PROCEDURES_INDEX_START+1:PROCEDURES_INDEX_END]
#print PROCEDURES_DATA

count = 0
PROCEDURES_Start_index = []
PROCEDURES_End_index = []
for data in PROCEDURES_DATA:
	if "def" == data.strip()[0:3]:
		PROCEDURES_Start_index.append(count)
	elif "enddef" == data.strip()[0:6]:
		PROCEDURES_End_index.append(count)
	count += 1
PROCEDURES_Start_index.sort()
PROCEDURES_End_index.sort()


PROCEDURES_LIST = []

for i in range(len(PROCEDURES_Start_index)):
	PROCEDURES_TEXT = ""
	tmpPROCEDURES = PROCEDURES_DATA[PROCEDURES_Start_index[i]:PROCEDURES_End_index[i]]
	for data in tmpPROCEDURES:
		if "*" != data[0]:
			PROCEDURES_TEXT = PROCEDURES_TEXT + data

	tmpPROCEDURES = PROCEDURES_TEXT.split(';')
	count = 0
	for data in tmpPROCEDURES:
		if "def" in ''.join(data.split()):
			PROCEDURES_LIST.append([])
			PROCEDURES_LIST[i].append(data.split()[1])
		if "preob_cal=" in ''.join(data.split()):
			preob_txt = ''.join(data.split()).replace('=', ':').split(':')
			if preob_txt[1] == "on" and preob_txt[3] =="R_SKY":
				PROCEDURES_LIST[i].append(preob_txt[2][:-3])
				count += 1
	if count == 0:
		PROCEDURES_LIST[i].append(0)



if start_time_flag == 'any_start_vex':
	time_str =  str_time_to_time(any_time)
	time_vex= datetime.datetime(int(time_str[0]), int(time_str[1]), int(time_str[2]), int(time_str[3]), int(time_str[4]), int(time_str[5]))
	time_difference = datetime.datetime(int(str_time_to_time(SCHED_LIST[0][0][6:-1])[0]),int(str_time_to_time(SCHED_LIST[0][0][6:-1])[1]), int(str_time_to_time(SCHED_LIST[0][0][6:-1])[2]), int(str_time_to_time(SCHED_LIST[0][0][6:-1])[3]), int(str_time_to_time(SCHED_LIST[0][0][6:-1])[4]), int(str_time_to_time(SCHED_LIST[0][0][6:-1])[5])) - time_vex
if start_time_flag == 'after_start_vex':
	time_vex = datetime.datetime.today() + datetime.timedelta(days=after_day, hours=after_hour, minutes=after_minute)
	time_difference = datetime.datetime(int(str_time_to_time(SCHED_LIST[0][0][6:-1])[0]),int(str_time_to_time(SCHED_LIST[0][0][6:-1])[1]), int(str_time_to_time(SCHED_LIST[0][0][6:-1])[2]), int(str_time_to_time(SCHED_LIST[0][0][6:-1])[3]), int(str_time_to_time(SCHED_LIST[0][0][6:-1])[4]), int(str_time_to_time(SCHED_LIST[0][0][6:-1])[5])) - time_vex

#time_difference = datetime.datetime(int(str_time_to_time(SCHED_LIST[0][0][6:-1])[0]),int(str_time_to_time(SCHED_LIST[0][0][6:-1])[1]), int(str_time_to_time(SCHED_LIST[0][0][6:-1])[2]), int(str_time_to_time(SCHED_LIST[0][0][6:-1])[3]), int(str_time_to_time(SCHED_LIST[0][0][6:-1])[4]), int(str_time_to_time(SCHED_LIST[0][0][6:-1])[5])) - datetime.datetime(int(str_time_to_time('2018y136d14h12m00s')[0]),int(str_time_to_time('2018y136d14h12m00s')[1]), int(str_time_to_time('2018y136d14h12m00s')[2]), int(str_time_to_time('2018y136d14h12m00s')[3]), int(str_time_to_time('2018y136d14h12m00s')[4]), int(str_time_to_time('2018y136d14h12m00s')[5]))

#-------------------------------------------------#
#  書き出す部分
#-------------------------------------------------#
start_file = open(write_vex_file_name, "w")
for data in data_list:
	#if ''.join(data.split()) in SCHED_LIST:
	if 'start=' in ''.join(data.split()) and ('exper_nominal_start' in ''.join(data.split())) == 0:
		date_txt = datetime.datetime(int(str_time_to_time(''.join(data.split())[6:-1])[0]),int(str_time_to_time(''.join(data.split())[6:-1])[1]), int(str_time_to_time(''.join(data.split())[6:-1])[2]), int(str_time_to_time(''.join(data.split())[6:-1])[3]), int(str_time_to_time(''.join(data.split())[6:-1])[4]), int(str_time_to_time(''.join(data.split())[6:-1])[5]))

		if start_time_flag == 'after_start_ref_vex':
			write_txt = date_txt + datetime.timedelta(days = int(after_day), hours = int(after_hour), minutes = int(after_minute))
		else:
			write_txt = date_txt - datetime.timedelta(seconds = int(time_difference.total_seconds()))

		time_adjust = datetime.datetime(int(write_txt.year)-1, 12, 31)
		write_file_txt = 'start=' + str(write_txt.year) + 'y' + str(write_txt.month) + 'm' + str(write_txt.day) + 'd' + str(write_txt.hour) + 'h' + str(write_txt.minute) + 'm' + str(write_txt.second) + 's'
		write_file_txt = 'start=%04dy%03dd%02dh%02dm%02ds; %s %s\n' %(int(write_txt.year), (write_txt - time_adjust).days, int(write_txt.hour), int(write_txt.minute), int(write_txt.second), data.split()[1], data.split()[2])
		start_file.write(write_file_txt)
	elif ('exper_nominal_start' in ''.join(data.split())):
		date_txt = datetime.datetime(int(str_time_to_time(OBSERVATION_START_TIME)[0]),int(str_time_to_time(OBSERVATION_START_TIME)[1]), int(str_time_to_time(OBSERVATION_START_TIME)[2]), int(str_time_to_time(OBSERVATION_START_TIME)[3]), int(str_time_to_time(OBSERVATION_START_TIME)[4]), int(str_time_to_time(OBSERVATION_START_TIME)[5]))
		if start_time_flag == 'after_start_ref_vex':
			write_txt = date_txt + datetime.timedelta(days = int(after_day), hours = int(after_hour), minutes = int(after_minute))
		else:
			write_txt = date_txt - datetime.timedelta(seconds = int(time_difference.total_seconds()))
		time_adjust = datetime.datetime(int(write_txt.year)-1, 12, 31)
		write_file_txt = 'start=' + str(write_txt.year) + 'y' + str(write_txt.month) + 'm' + str(write_txt.day) + 'd' + str(write_txt.hour) + 'h' + str(write_txt.minute) + 'm' + str(write_txt.second) + 's'
		write_file_txt = 'exper_nominal_start=%04dy%03dd%02dh%02dm%02ds;\n' %(int(write_txt.year), (write_txt - time_adjust).days, int(write_txt.hour), int(write_txt.minute), int(write_txt.second))
		start_file.write(write_file_txt)
	elif ('exper_nominal_stop' in ''.join(data.split())):
		date_txt = datetime.datetime(int(str_time_to_time(OBSERVATION_STOP_TIME)[0]),int(str_time_to_time(OBSERVATION_STOP_TIME)[1]), int(str_time_to_time(OBSERVATION_STOP_TIME)[2]), int(str_time_to_time(OBSERVATION_STOP_TIME)[3]), int(str_time_to_time(OBSERVATION_STOP_TIME)[4]), int(str_time_to_time(OBSERVATION_STOP_TIME)[5]))
		if start_time_flag == 'after_start_ref_vex':
			write_txt = date_txt + datetime.timedelta(days = int(after_day), hours = int(after_hour), minutes = int(after_minute))
		else:
			write_txt = date_txt - datetime.timedelta(seconds = int(time_difference.total_seconds()))
		time_adjust = datetime.datetime(int(write_txt.year)-1, 12, 31)
		write_file_txt = 'start=' + str(write_txt.year) + 'y' + str(write_txt.month) + 'm' + str(write_txt.day) + 'd' + str(write_txt.hour) + 'h' + str(write_txt.minute) + 'm' + str(write_txt.second) + 's'
		write_file_txt = 'exper_nominal_stop=%04dy%03dd%02dh%02dm%02ds;\n' %(int(write_txt.year), (write_txt - time_adjust).days, int(write_txt.hour), int(write_txt.minute), int(write_txt.second))
		start_file.write(write_file_txt)
	else:
		start_file.write(data)

#-------------------------------------------------#
#  alert parameter
#-------------------------------------------------#
print ".VEX FILE NAME         : " + vex_file_name
print ".VEX FILE NAME       : " + write_vex_file_name