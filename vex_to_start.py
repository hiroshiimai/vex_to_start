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
vex_file_name = "a18075a_r1.vex"

#----------- time of antenna ---------#
after_mmc = 10
before_observation = 30
time_of_second_move = 20

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
			print start_file_name
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

for data in FREQ_DATA:
	#周波数
	if "chan_def" in data.split():
		#print data.split()[2], "=", data.split()[3], "MHz"
		#print data.split()[5], "=", data.split()[6], "MHz"
		#print data.split()[8], "=", data.split()[10], data.split()[12], data.split()[13]
		pass


#-------------------------------------------------#
#  STATION - Don't use
#-------------------------------------------------#
"""
#$STATIONを分解する。
STATION_INDEX_START = 0
STATION_INDEX_END = 0
for data in data_list:
	if data.strip() in "$STATION;":
		STATION_INDEX_START = data_list.index(data)
		STATION_INDEX_END = title_index[title_index.index(STATION_INDEX_START)+1]
#print STATION_INDEX_START, STATION_INDEX_END
STATION_DATA = data_list[STATION_INDEX_START+1:STATION_INDEX_END]
#print STATION_DATA
count = 0
STATION_index = []
for data in STATION_DATA:
	if "*" in data.strip():
		STATION_index.append(count)
	count += 1
STATION_index.sort()
STATION_LIST = []
for i in range(len(STATION_index)-1):
	tmpSTATION = STATION_DATA[STATION_index[i]:STATION_index[i+1]]
	for data in tmpSTATION:
		#望遠鏡
		if "$SITE" in data.split():
			#print data.split()[-1][:-1]
			pass
		if "$ANTENNA" in data.split():
			#print data.split()[-1][:-1]
			pass
		if "$DAS" in data.split():
			#print data.split()[-1][:-1]
			pass
"""
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



#-------------------------------------------------#
#  書き出す部分
#-------------------------------------------------#
offset_time = SCHED_LIST[0][0]
start_offset_time = str_time_to_time(offset_time)
start_offset_time = datetime.datetime(int(start_offset_time[0]), int(start_offset_time[1]), int(start_offset_time[2]), int(start_offset_time[3]), int(start_offset_time[4]), int(start_offset_time[5]))
end_offset_time = start_offset_time - datetime.timedelta(seconds=1000)


if start_file_flag == "file_date":
	start_file_name = Observation_Name[:-1] + "_" + Station_Name + "_" + str(Create_Date.year)[2:] + "%02d%02d%02d%02d%02d.start" %(int(str(Create_Date.month)), int(str(Create_Date.day)), int(str(Create_Date.hour)), int(str(Create_Date.minute)), int(str(Create_Date.second)))
else:
	pass
start_file = open(start_file_name, "w")


#-------------------------------------------------#
#  write title
#-------------------------------------------------#
start_file.write("#---------------------------------------------------\n")
start_file.write("#------- WS COSMOS INSTRUCTION FILE\n")
start_file.write("#------- Generated from VLBI Schedule\n")
start_file.write("#------- Conversion Software ver. 17SEP18\n")
start_file.write("#------------------- made by " + "H.Imai" + "\n")
start_file.write("#------- Creation Date : %04d/%02d/%02d %02d:%02d:%02d\n" %(Create_Date.year, Create_Date.month, Create_Date.day, Create_Date.hour, Create_Date.minute, Create_Date.second))
start_file.write("#---------------------------------------------------\n")
start_file.write("\n")


#-------------------------------------------------#
#  write OBSTABLE
#-------------------------------------------------#
start_file.write("#-------- OBSTABLE Information Table --------\n")
start_file.write("% OBSERVER=" + os.getlogin() + "\n")
#start_file.write("% GROUP=" + os.getlogin() + "\n")
start_file.write("% GROUP=" + USER_NAME + "\n")
#start_file.write("% PROJECT=vlbi\n")
start_file.write("% PROJECT=" + PROJECT_NAME + "\n")
start_file.write("% OBS_NAME=" + Observation_Name.rstrip(";") + "\n")
start_file.write("% MMC_CMD1=MCL\n")
start_file.write("% MMC_CMD2=MOP\n")
start_file.write("% MMC_CMD3=\n")
start_file.write("% MMC_CMD4=\n")
start_file.write("% ON_TINTEG=10\n")
start_file.write("% OFF_TINTEG=10\n")
start_file.write("% CALIB_TINTEG=10\n")
start_file.write("\n")

#-------------------------------------------------#
#  write GROUP OF DEVICES
#-------------------------------------------------#
start_file.write("#-------- DEFINE GROUP OF DEVICES --------\n")
start_file.write("GROUP TRK_LOCAL ANT VLBI\n")
start_file.write("\n")

#-------------------------------------------------#
#  write OPEN DEVICES
#-------------------------------------------------#
start_file.write("#-------- OPEN DEVICES --------\n")
start_file.write("OPEN ANT\n")
start_file.write("OPEN MMC\n")
start_file.write("OPEN VLBI\n")
start_file.write("\n")


#SCHEDの名前からSOURCEを探索
for scan in range(len(SCHED_Start_index)):
	SOURCE_NAME_SAMPLE = SCHED_LIST[scan][2]
	start_file.write("#-------- PARAMS for SKED%04d --------\n" %(scan+1))
	start_file.write("EXECUTE MMC CMD(AOF)\n")
	start_file.write("EXECUTE MMC CMD(OPN)\n")
	start_file.write("SET ANT TRK_TYPE \'RADEC\'\n")

	SOURCE_NUMBER = 0
	for i in range(len(SOURCE_LIST)):
		if SOURCE_NAME_SAMPLE == SOURCE_LIST[i][0]:
			SOURCE_NUMBER = i
	#print SOURCE_NAME_SAMPLE, ":", SOURCE_LIST[SOURCE_NUMBER][0]


	right_ascension = float(SOURCE_LIST[SOURCE_NUMBER][1][0:2]) * 15 + float(SOURCE_LIST[SOURCE_NUMBER][1][3:5]) * (15/60.0) + float(SOURCE_LIST[SOURCE_NUMBER][1][6:8]) * (15/3600.0) + 0.01 * float(SOURCE_LIST[SOURCE_NUMBER][1][9:11]) * (15/3600.0)

	if SOURCE_LIST[SOURCE_NUMBER][2][0] == "+" or SOURCE_LIST[SOURCE_NUMBER][2][0] == "-":
		declination = float(SOURCE_LIST[SOURCE_NUMBER][2][0:3]) + float(SOURCE_LIST[SOURCE_NUMBER][2][4:6]) / 60.0 + float(SOURCE_LIST[SOURCE_NUMBER][2][7:11]) / 3600.0
	else:
		declination = float(SOURCE_LIST[SOURCE_NUMBER][2][0:2]) + float(SOURCE_LIST[SOURCE_NUMBER][2][3:5]) / 60.0 + float(SOURCE_LIST[SOURCE_NUMBER][2][6:10]) / 3600.0

	#ファイル書き込み部
	start_file.write("SET TRK_LOCAL SRC_NAME \'" + SOURCE_LIST[SOURCE_NUMBER][0] + "\'\n")
	start_file.write("SET TRK_LOCAL SRC_POS ( %.5f, %.5f)\n" %(right_ascension, declination))
	start_file.write("SET ANT SCAN_COOD \'RADEC\'\n")
	start_file.write("SET ANT SCAN_COOD_OFF \'RADEC\'\n")
	start_file.write("SET VLBI OBS_MODE \'NORMAL\'\n")
	start_file.write("SET VLBI SCHDULE \'SKED%03d\'\n" %(scan+1))
	start_file.write("SET TRK_LOCAL EPOCH \'" + SOURCE_LIST[SOURCE_NUMBER][3] + "'\n")



#----------------------------------------------------------

	#------------------------------------#
	#---------- original start ----------#
	#------------------------------------#
	if start_time_flag == "original_start":
		offset_time = SCHED_LIST[scan][0]
		start_offset_time = str_time_to_time(offset_time)
		start_offset_time = datetime.datetime(int(start_offset_time[0]), int(start_offset_time[1]), int(start_offset_time[2]), int(start_offset_time[3]), int(start_offset_time[4]), int(start_offset_time[5]))
		start_offset_time = start_offset_time + datetime.timedelta(hours=9)
		end_offset_time = end_offset_time + datetime.timedelta(seconds=time_of_second_move)



		WAIT_MMC_TIME = 0
		#print MODE_LIST
		for m in MODE_LIST:
			if SCHED_LIST[scan][1] == m[0]:
				for p in PROCEDURES_LIST:
					if m[1] == p[0]:
						WAIT_MMC_TIME = int(p[1])



		#observation start time
		if WAIT_MMC_TIME > 0:
			OBSERVATION_BEFORE_TIME = start_offset_time - datetime.timedelta(seconds=before_observation+WAIT_MMC_TIME+after_mmc)
		else:
			OBSERVATION_BEFORE_TIME = start_offset_time - datetime.timedelta(seconds=before_observation)



		#時間のERROR判定
		if (time_plus_or_minus(OBSERVATION_BEFORE_TIME, end_offset_time) > 0):
			pass
		else:
			if WAIT_MMC_TIME > 0:
				OBSERVATION_BEFORE_TIME = start_offset_time - datetime.timedelta(seconds=WAIT_MMC_TIME+after_mmc)
			else:
				OBSERVATION_BEFORE_TIME = start_offset_time



			if (time_plus_or_minus(OBSERVATION_BEFORE_TIME, end_offset_time) > 0):
				pass
			else:
				print "#############################"
				print "######## TIME ERR0R #########"
				print "# between scan%d and scan%d #" %(scan, scan+1)
				print "#############################"
				sys.exit()



		if scan == 0:
			CULLENT_TIME = OBSERVATION_BEFORE_TIME - datetime.timedelta(seconds=TIME_MOVE_ANTENNA)


		end_sec = int(SCHED_LIST[scan][3].split(':')[2].strip('sec'))
		end_offset_time = start_offset_time + datetime.timedelta(seconds=end_sec)


		#ファイルに書き込み部
		start_file.write("EXECUTE ANT OFFSET(0,0) TIME_RANGE(%04d/%02d/%02d %02d:%02d:%02d - %04d/%02d/%02d %02d:%02d:%02d) TYPE(ON)\n" %(CULLENT_TIME.year, CULLENT_TIME.month, CULLENT_TIME.day, CULLENT_TIME.hour, CULLENT_TIME.minute, CULLENT_TIME.second, OBSERVATION_BEFORE_TIME.year, OBSERVATION_BEFORE_TIME.month, OBSERVATION_BEFORE_TIME.day, OBSERVATION_BEFORE_TIME.hour, OBSERVATION_BEFORE_TIME.minute, OBSERVATION_BEFORE_TIME.second))

		CULLENT_TIME = OBSERVATION_BEFORE_TIME
		start_file.write("WAIT_READY ANT\n")


		if WAIT_MMC_TIME > 0:
			start_file.write("EXECUTE MMC CMD(MCL)\n")
			NEXT_TIME = CULLENT_TIME + datetime.timedelta(seconds=WAIT_MMC_TIME)
			start_file.write("EXECUTE ANT OFFSET(0,0) TIME_RANGE(%04d/%02d/%02d %02d:%02d:%02d - %04d/%02d/%02d %02d:%02d:%02d) TYPE(ON)\n" %(CULLENT_TIME.year, CULLENT_TIME.month, CULLENT_TIME.day, CULLENT_TIME.hour, CULLENT_TIME.minute, CULLENT_TIME.second, NEXT_TIME.year, NEXT_TIME.month, NEXT_TIME.day, NEXT_TIME.hour, NEXT_TIME.minute, NEXT_TIME.second))

			CULLENT_TIME = NEXT_TIME + datetime.timedelta(seconds=after_mmc)
			#end_offset_time = CULLENT_TIME + datetime.timedelta(seconds=end_sec+30)
			start_file.write("WAIT_READY ANT\n")
			start_file.write("WAIT MMC\n")
			start_file.write("EXECUTE MMC CMD(MOP)\n")
			start_file.write("WAIT MMC\n")





		start_file.write("EXECUTE ANT OFFSET(0,0) TIME_RANGE(%04d/%02d/%02d %02d:%02d:%02d - %04d/%02d/%02d %02d:%02d:%02d) TYPE(ON)\n" %(CULLENT_TIME.year, CULLENT_TIME.month, CULLENT_TIME.day, CULLENT_TIME.hour, CULLENT_TIME.minute, CULLENT_TIME.second, end_offset_time.year, end_offset_time.month, end_offset_time.day, end_offset_time.hour, end_offset_time.minute, end_offset_time.second))
		start_file.write("WAIT ANT VLBI\n")
		start_file.write("\n")
		CULLENT_TIME = end_offset_time



	#------------------------------#
	#---------- any time ----------#
	#------------------------------#
	if start_time_flag == "any_start":
		if scan == 0:
			start_offset_time = str_time_to_time(any_time)
			start_offset_time = datetime.datetime(int(start_offset_time[0]), int(start_offset_time[1]), int(start_offset_time[2]), int(start_offset_time[3]), int(start_offset_time[4]), int(start_offset_time[5]))

			CULLENT_TIME = start_offset_time

		WAIT_MMC_TIME = 0
		#print MODE_LIST
		for m in MODE_LIST:
			if SCHED_LIST[scan][1] == m[0]:
				for p in PROCEDURES_LIST:
					if m[1] == p[0]:
						WAIT_MMC_TIME = int(p[1])

		end_sec = int(SCHED_LIST[scan][3].split(':')[2].strip('sec'))

		'''
		if WAIT_MMC_TIME > 0:
			end_offset_time = CULLENT_TIME + datetime.timedelta(seconds=end_sec+after_mmc+before_observation+WAIT_MMC_TIME)
		else:
			end_offset_time = CULLENT_TIME + datetime.timedelta(seconds=end_sec+before_observation)
		'''



		if scan == 0:
			OBSERVATION_BEFORE_TIME = CULLENT_TIME + datetime.timedelta(seconds=TIME_MOVE_ANTENNA)
			#end_offset_time = end_offset_time + datetime.timedelta(seconds=TIME_MOVE_ANTENNA)
		else:
			#もしかしたらパラメタにしたほうがいいかも
			OBSERVATION_BEFORE_TIME = CULLENT_TIME + datetime.timedelta(seconds=time_of_second_move)


		#ファイルに書き込み部
		start_file.write("EXECUTE ANT OFFSET(0,0) TIME_RANGE(%04d/%02d/%02d %02d:%02d:%02d - %04d/%02d/%02d %02d:%02d:%02d) TYPE(ON)\n" %(CULLENT_TIME.year, CULLENT_TIME.month, CULLENT_TIME.day, CULLENT_TIME.hour, CULLENT_TIME.minute, CULLENT_TIME.second, OBSERVATION_BEFORE_TIME.year, OBSERVATION_BEFORE_TIME.month, OBSERVATION_BEFORE_TIME.day, OBSERVATION_BEFORE_TIME.hour, OBSERVATION_BEFORE_TIME.minute, OBSERVATION_BEFORE_TIME.second))

		CULLENT_TIME = OBSERVATION_BEFORE_TIME
		start_file.write("WAIT_READY ANT\n")


		if WAIT_MMC_TIME > 0:
			start_file.write("EXECUTE MMC CMD(MCL)\n")

			NEXT_TIME = CULLENT_TIME + datetime.timedelta(seconds=WAIT_MMC_TIME)
			start_file.write("EXECUTE ANT OFFSET(0,0) TIME_RANGE(%04d/%02d/%02d %02d:%02d:%02d - %04d/%02d/%02d %02d:%02d:%02d) TYPE(ON)\n" %(CULLENT_TIME.year, CULLENT_TIME.month, CULLENT_TIME.day, CULLENT_TIME.hour, CULLENT_TIME.minute, CULLENT_TIME.second, NEXT_TIME.year, NEXT_TIME.month, NEXT_TIME.day, NEXT_TIME.hour, NEXT_TIME.minute, NEXT_TIME.second))

			CULLENT_TIME = NEXT_TIME + datetime.timedelta(seconds=after_mmc)
			start_file.write("WAIT_READY ANT\n")
			start_file.write("WAIT MMC\n")
			start_file.write("EXECUTE MMC CMD(MOP)\n")
			start_file.write("WAIT MMC\n")

		end_offset_time = CULLENT_TIME + datetime.timedelta(seconds=end_sec)
		start_file.write("EXECUTE ANT OFFSET(0,0) TIME_RANGE(%04d/%02d/%02d %02d:%02d:%02d - %04d/%02d/%02d %02d:%02d:%02d) TYPE(ON)\n" %(CULLENT_TIME.year, CULLENT_TIME.month, CULLENT_TIME.day, CULLENT_TIME.hour, CULLENT_TIME.minute, CULLENT_TIME.second, end_offset_time.year, end_offset_time.month, end_offset_time.day, end_offset_time.hour, end_offset_time.minute, end_offset_time.second))
		start_file.write("WAIT ANT VLBI\n")
		start_file.write("\n")
		CULLENT_TIME = end_offset_time

	#------------------------------#
	#---------- after time ----------#
	#------------------------------#
	if start_time_flag == "after_start":
		if scan == 0:
			start_offset_time = datetime.datetime.today() + datetime.timedelta(days=after_day, hours=after_hour, minutes=after_minute)
			CULLENT_TIME = start_offset_time

		WAIT_MMC_TIME = 0
		#print MODE_LIST
		for m in MODE_LIST:
			if SCHED_LIST[scan][1] == m[0]:
				for p in PROCEDURES_LIST:
					if m[1] == p[0]:
						WAIT_MMC_TIME = int(p[1])

		end_sec = int(SCHED_LIST[scan][3].split(':')[2].strip('sec'))


		if scan == 0:
			OBSERVATION_BEFORE_TIME = CULLENT_TIME + datetime.timedelta(seconds=TIME_MOVE_ANTENNA)
			#end_offset_time = end_offset_time + datetime.timedelta(seconds=TIME_MOVE_ANTENNA)
		else:
			#もしかしたらパラメタにしたほうがいいかも
			OBSERVATION_BEFORE_TIME = CULLENT_TIME + datetime.timedelta(seconds=time_of_second_move)


		#ファイルに書き込み部
		start_file.write("EXECUTE ANT OFFSET(0,0) TIME_RANGE(%04d/%02d/%02d %02d:%02d:%02d - %04d/%02d/%02d %02d:%02d:%02d) TYPE(ON)\n" %(CULLENT_TIME.year, CULLENT_TIME.month, CULLENT_TIME.day, CULLENT_TIME.hour, CULLENT_TIME.minute, CULLENT_TIME.second, OBSERVATION_BEFORE_TIME.year, OBSERVATION_BEFORE_TIME.month, OBSERVATION_BEFORE_TIME.day, OBSERVATION_BEFORE_TIME.hour, OBSERVATION_BEFORE_TIME.minute, OBSERVATION_BEFORE_TIME.second))

		CULLENT_TIME = OBSERVATION_BEFORE_TIME
		start_file.write("WAIT_READY ANT\n")


		if WAIT_MMC_TIME > 0:
			start_file.write("EXECUTE MMC CMD(MCL)\n")

			NEXT_TIME = CULLENT_TIME + datetime.timedelta(seconds=WAIT_MMC_TIME)
			start_file.write("EXECUTE ANT OFFSET(0,0) TIME_RANGE(%04d/%02d/%02d %02d:%02d:%02d - %04d/%02d/%02d %02d:%02d:%02d) TYPE(ON)\n" %(CULLENT_TIME.year, CULLENT_TIME.month, CULLENT_TIME.day, CULLENT_TIME.hour, CULLENT_TIME.minute, CULLENT_TIME.second, NEXT_TIME.year, NEXT_TIME.month, NEXT_TIME.day, NEXT_TIME.hour, NEXT_TIME.minute, NEXT_TIME.second))

			CULLENT_TIME = NEXT_TIME + datetime.timedelta(seconds=after_mmc)
			start_file.write("WAIT_READY ANT\n")
			start_file.write("WAIT MMC\n")
			start_file.write("EXECUTE MMC CMD(MOP)\n")
			start_file.write("WAIT MMC\n")

		end_offset_time = CULLENT_TIME + datetime.timedelta(seconds=end_sec)
		start_file.write("EXECUTE ANT OFFSET(0,0) TIME_RANGE(%04d/%02d/%02d %02d:%02d:%02d - %04d/%02d/%02d %02d:%02d:%02d) TYPE(ON)\n" %(CULLENT_TIME.year, CULLENT_TIME.month, CULLENT_TIME.day, CULLENT_TIME.hour, CULLENT_TIME.minute, CULLENT_TIME.second, end_offset_time.year, end_offset_time.month, end_offset_time.day, end_offset_time.hour, end_offset_time.minute, end_offset_time.second))
		start_file.write("WAIT ANT VLBI\n")
		start_file.write("\n")
		CULLENT_TIME = end_offset_time


start_file.close()




#-------------------------------------------------#
#  alert parameter
#-------------------------------------------------#
print "USER NAME              : " + USER_NAME
print "CREATE Date            :",
print Create_Date
print "ANTENNA NAME           : " + Station_Name
print ".VEX FILE NAME         : " + vex_file_name
print ".START FILE NAME       : " + start_file_name
