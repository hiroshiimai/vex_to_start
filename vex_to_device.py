#! /usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import sys
import os

#------------------------------------------#
# default parameter
#------------------------------------------#
#---------- User name ----------#
USER_NAME = "hogehoge"
#---------- Project name ----------#
PROJECT_NAME = "vlbi"

#---------- Create Date ----------#
Create_Date = datetime.datetime.today()

#---------- choose antenna name ----------#
Station_Name = "Vm"
#Station_Name = "Vr"
#Station_Name = "Vo"
#Station_Name = "Vs"
#Station_Name = "Nb"
#Station_Name = "Ks"

#---------- set start observation time ----------#
#---------- choose original start time ----------#
start_time_flag = "original_start"

#---------- set any time(Set time JST) ----------#
#start_time_flag = "any_time"
any_time = "2016y136d14h12m00s"

#---------- set after time ----------#
#start_time_flag = "after_time"
after_day = 10
after_hour = 0
after_minute = 0

#---------- time of Move antenna ----------#
TIME_MOVE_ANTENNA = 1200

#---------- vex file name ----------#
#vex_file_name = "r16136a.vex"
#vex_file_name = "k18hi01d_180507_kvn.vex"
vex_file_name = "k18hi02f.vex"

#----------- time of antenna ---------#
after_mmc = 10
before_observation = 30
time_of_second_move = 20


#----------- ERROR MODE ---------#
#error_flag = "skip_flag"
error_flag = "stop_flag"


device_file_flag  = 'file_selected'
device_file_name  = 'sample.device'
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
		if "device_file_flag" == data.strip()[0:16]:
			device_file_flag  = data.split('=')[1].split()[0]
		if "device_file_name" == data.strip()[0:16]:
			device_file_name  = data.split('=')[1].split()[0]

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

count = 0
FREQ_Start_index = []
FREQ_End_index = []
for data in FREQ_DATA:
	if "def" == data.strip()[0:3]:
		FREQ_Start_index.append(count)
	elif "enddef" == data.strip()[0:6]:
		FREQ_End_index.append(count)
	count += 1
FREQ_Start_index.sort()
FREQ_End_index.sort()

FREQ_LIST = []
for i in range(len(FREQ_Start_index)):
	if "stations" in FREQ_DATA[FREQ_Start_index[i]+1].split() and "Ny" in FREQ_DATA[FREQ_Start_index[i]+1].rstrip().split(':'):
		for j in range(FREQ_Start_index[i]+3, FREQ_End_index[i]):
			FREQ_LIST.append(FREQ_DATA[j])


#-------------------------------------------------#
#  BBC
#-------------------------------------------------#
#$BBCを分解する。
BBC_INDEX_START = 0
BBC_INDEX_END = 0
for data in data_list:
	if data.strip() in "$BBC;":
		BBC_INDEX_START = data_list.index(data)
		BBC_INDEX_END = title_index[title_index.index(BBC_INDEX_START)+1]
#print BBC_INDEX_START, BBC_INDEX_END

BBC_DATA = data_list[BBC_INDEX_START:BBC_INDEX_END]
#print BBC_DATA  #この中に$BBC;の中身が書いてある。

count = 0
BBC_Start_index = []
BBC_End_index = []
for data in BBC_DATA:
	if "def" == data.strip()[0:3]:
		BBC_Start_index.append(count)
	elif "enddef" == data.strip()[0:6]:
		BBC_End_index.append(count)
	count += 1
BBC_Start_index.sort()
BBC_End_index.sort()

BBC_LIST = []
for i in range(len(BBC_Start_index)):
	if "stations" in BBC_DATA[BBC_Start_index[i]+1].split() and "Ny" in BBC_DATA[BBC_Start_index[i]+1].rstrip().split(':'):
		for j in range(BBC_Start_index[i]+2, BBC_End_index[i]):
			BBC_LIST.append(BBC_DATA[j])





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
		if "start=" in ''.join(data.split()):
			SCHED_LIST.append([])
			SCHED_LIST[i].append(''.join(data.split())[6:])
			#print ''.join(data.split()).strip('start=')
		if "mode=" in ''.join(data.split()):
			SCHED_LIST[i].append(''.join(data.split())[5:])
			#print ''.join(data.split()).strip('mode=')
		if "source=" in ''.join(data.split()):
			SCHED_LIST[i].append(''.join(data.split())[7:])
			#print ''.join(data.split()).strip('source=')
		if "source1=" in ''.join(data.split()):
			SCHED_LIST[i].append(''.join(data.split())[8:])
			#print ''.join(data.split()).strip('source1=')
		if Station_Name_ANT in ''.join(data.split()):
			SCHED_LIST[i].append(''.join(data.split())[9:])
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

BBC_NAME = 0
BBC_NUMBER = []
tmpBBC_NUMBER = []
for i in range(len(BBC_LIST)):
	if BBC_LIST[i].split()[-1] == BBC_NAME:
		pass
	else:
		tmpBBC_NUMBER.append(i)
		BBC_NUMBER.append(i)
		BBC_NAME = BBC_LIST[i].split()[-1]
		#print BBC_LIST[i].split()[-1]
#print BBC_NUMBER
newFREQ_LIST = []
tmpBBC_NUMBER.append(16)
#print tmpBBC_NUMBER
for i in range(len(tmpBBC_NUMBER)-1):
	tmpCenterFreq = []
	for j in range(int(tmpBBC_NUMBER[i]), int(tmpBBC_NUMBER[i+1])):
		print j
		tmpCenterFreq.append(float(FREQ_LIST[j].split()[3]))
		print float(FREQ_LIST[j].split()[3])
	tmpCenterFreq = 0.5*(max(tmpCenterFreq) + min(tmpCenterFreq) + float(FREQ_LIST[j].split()[8]))

	for j in range(int(tmpBBC_NUMBER[i]), int(tmpBBC_NUMBER[i+1])):
		newFREQ_LIST.append(tmpCenterFreq)
#print newFREQ_LIST



#-------------------------------------------------#
#  書き出す部分
#-------------------------------------------------#"
if device_file_flag == "file_date":
	device_file_name = Observation_Name[:-1] + "_" + str(Create_Date.year)[2:] + "%02d%02d%02d%02d%02d.ndevice" %(int(str(Create_Date.month)), int(str(Create_Date.day)), int(str(Create_Date.hour)), int(str(Create_Date.minute)), int(str(Create_Date.second)))
else:
	pass

start_file = open(device_file_name, "w")
#start_file = open("sample.device", "w")

start_file.write("zobs_version=OUv.34.2.02\n")
start_file.write("saved_time_and_date=%04d/%02d/%02d %02d:%02d:%02d\n" %(Create_Date.year, Create_Date.month, Create_Date.day, Create_Date.hour, Create_Date.minute, Create_Date.second))
start_file.write("modified_time_and_date=\n")
#-----------------------
#   H20ch1とかつける
#-----------------------
count20 = 1
count40 = 1
for i in range(1, 9):
	flag = 0
	for j in range(len(BBC_NUMBER)):
		if i==j+1:
			if float(FREQ_LIST[BBC_NUMBER[j]].split()[3])-20000 < 10000:
				start_file.write("Rx_Type%s=H20ch%s\n" %(i, count20))
				count20+=1
				flag += 1
				device_freq
				continue
			elif float(FREQ_LIST[BBC_NUMBER[j]].split()[3])-40000 < 10000:
				start_file.write("Rx_Type%s=H40\n" %(i))
				count40+=1
				flag += 1
				continue
	if flag == 0:
		start_file.write("Rx_Type%s=\n" %(i))

for i in range(1, 9):
	start_file.write("Rx_SB%s=USB\n" %(i))

#------------------------
#  freqを入れる
#------------------------
counter = 1
for i in range(1, 9):
	flag = 0
	for j in range(len(BBC_NUMBER)):
		if i==j+1:
			if float(newFREQ_LIST[BBC_NUMBER[j]])-20000 < 10000:
				tmpFreq = float(newFREQ_LIST[BBC_NUMBER[j]])/1000
				start_file.write("Rx_Freq%s=%2.2f\n" %(i, tmpFreq))
				count20+=1
				flag += 1
				device_freq
				continue
			elif float(newFREQ_LIST[BBC_NUMBER[j]])-40000 < 10000:
				tmpFreq = float(newFREQ_LIST[BBC_NUMBER[j]])/1000
				start_file.write("Rx_Freq%s=%2.2f\n" %(i, tmpFreq))
				count40+=1
				flag += 1
				continue
	if flag == 0:
		start_file.write("Rx_Freq%s=\n" %(i))

for i in range(1, 9):
	start_file.write("Rx_IF%s=\n" %(i))

for i in range(1, 17):
	start_file.write("SAM_Rx%s=\n" %(i))

freq_number = []
for i in BBC_NUMBER:
	freq_number.append(int(BBC_LIST[i].rstrip().split()[-1].split("&IF_A")[1][:-1]))

BBC_NUMBER.append(len(BBC_LIST))
counter = 1
for i in range(1, 17):
	flag = 0
	for j in freq_number:
		if i == j:
			if float(newFREQ_LIST[j])-20000 < 10000:
				tmpFreq = float(newFREQ_LIST[BBC_NUMBER[counter]-2])/1000
				start_file.write("SAM_Freq%s=%2.2f\n" %(i, tmpFreq))
				count20+=1
				flag += 1
				device_freq
				continue
			elif float(newFREQ_LIST[j])-40000 < 10000:
				tmpFreq = float(newFREQ_LIST[BBC_NUMBER[counter]-2])/1000
				start_file.write("SAM_Freq%s=%2.2f\n" %(i, tmpFreq))
				count40+=1
				flag += 1
				continue
		if i == j+1:
			if float(newFREQ_LIST[BBC_NUMBER[counter]-1])-20000 < 10000:
				tmpFreq = float(newFREQ_LIST[BBC_NUMBER[counter]-2])/1000
				start_file.write("SAM_Freq%s=%2.2f\n" %(i, tmpFreq))
				flag += 1
				counter += 1
				continue

			elif float(newFREQ_LIST[BBC_NUMBER[counter]-1])-40000 < 10000:
				tmpFreq = float(newFREQ_LIST[BBC_NUMBER[counter]-2])/1000
				start_file.write("SAM_Freq%s=%2.2f\n" %(i, tmpFreq))
				flag += 1
				counter += 1
				continue

	if flag == 0:
		start_file.write("SAM_Freq%s=\n" %(i))


for i in range(1, 17):
	start_file.write("SAM_Att%s=5\n" %(i))

start_file.write("SAM_Resolution1=15.26\n")
start_file.write("SAM_Resolution2=3.81\n")
start_file.write("SAM_Sub_Array=false\n")
start_file.write("SAM_High_Resolution=false\n")
start_file.write("TMULT_Rot_Angle=0.0\n")
start_file.write("SAM_IPTIM=0.1\n")