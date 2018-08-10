#! /usr/bin/env python
# -*- coding:utf-8 -*-
import datetime

#------------------------------------------#
# default parameter
#------------------------------------------#
#---------- User name ----------#
USER_NAME = "hogehoge"

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

vex_data = open("a18075a_r1.vex", "r")
#vex_data = open(vex_file_name, "r")
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
			SOURCE_LIST[i].append(''.join(data.split()).strip('ra='))
			#print ''.join(data.split()).strip('ra=')
		if "dec=" in ''.join(data.split()):
			SOURCE_LIST[i].append(''.join(data.split()).strip('dec='))
			#print ''.join(data.split()).strip('ra=')
		if "ref_coord_frame=" in ''.join(data.split()):
			SOURCE_LIST[i].append(''.join(data.split()).strip('ref_coord_frame='))




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
FREQ_LIST = []
for data in FREQ_DATA:
	#周波数
	if "chan_def" in ''.join(data.split()):
		FREQ_LIST.append(float(''.join(data.split()).replace('=', ':').replace(';', ':').split(':')[2][:-3])*1.e6)
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
		if "start=" in ''.join(data.split()):
			SCHED_LIST.append([])
			SCHED_LIST[i].append(''.join(data.split()).strip('start='))
			#print ''.join(data.split()).strip('start=')
		if "mode=" in ''.join(data.split()):
			SCHED_LIST[i].append(''.join(data.split()).strip('mode='))
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









Create_Date = datetime.datetime.today()
start_file_name = "sample.tune"
start_file = open(start_file_name, "w")

#-------------------------------------------------#
#  obstable for the 45m Telescope
#-------------------------------------------------#
start_file.write("##################################\n")
start_file.write("# obstable for the 45m Telescope #\n")
start_file.write("##################################\n")

start_file.write("% OBSERVER=vlbi3bz\n")
start_file.write("% GROUP=vlbi3bz\n")
start_file.write("% PROJECT=proj5\n")
#------------------------------------
#     観測名を入れる
#------------------------------------
start_file.write("% OBS_NAME=")
start_file.write("%s\n" %(Observation_Name[:-1]))
start_file.write("% CHAPTER=")
start_file.write("%s\n" %(Observation_Name[:-1]))
start_file.write("% SRC_NAME=\n")
start_file.write("%s\n" %(SOURCE_LIST[0][0]))
start_file.write("% SRC_COMMENT=")
start_file.write("%s\n" %(SOURCE_LIST[0][0]))
start_file.write("% SW_MODE=POS\n")
start_file.write("% POS_ANGLE=0\n")
start_file.write("% EPOCH=J2000\n")
start_file.write("% VELO=3000.0\n")
start_file.write("% VDEF=RAD\n")
start_file.write("% VREF=LSR\n")
start_file.write("% OBS_MODE=POINTING\n")
start_file.write("% SCAN_TYPE=5POINTS\n")

################################################
################################################
start_file.write("% OBS_FREQ1=0\n")
start_file.write("% OBS_FREQ2=0\n")
start_file.write("% OBS_FREQ3=0\n")
start_file.write("% OBS_FREQ4=0\n")
start_file.write("% OBS_FREQ5=0\n")
start_file.write("% OBS_FREQ6=0\n")
start_file.write("% OBS_FREQ7=0\n")
start_file.write("% OBS_FREQ8=0\n")
start_file.write("% OBS_FREQ9=0\n")
start_file.write("% OBS_FREQ10=0\n")
start_file.write("% OBS_FREQ11=4.3122E10\n")
start_file.write("% OBS_FREQ12=2.2235E10\n")
start_file.write("% OBS_FREQ13=0\n")
start_file.write("% OBS_FREQ14=0\n")
start_file.write("% OBS_FREQ15=0\n")
start_file.write("% OBS_FREQ16=0\n")
start_file.write("% OBS_FREQ17=0\n")
start_file.write("% OBS_FREQ18=0\n")
start_file.write("% OBS_FREQ19=0\n")
start_file.write("% OBS_FREQ20=0\n")
start_file.write("% OBS_FREQ21=0\n")
start_file.write("% OBS_FREQ22=0\n")
start_file.write("% OBS_FREQ23=0\n")
start_file.write("% OBS_FREQ24=0\n")
################################################
################################################

start_file.write("% FREQ_IF1=0\n")
start_file.write("% FREQ_IF2=0\n")
start_file.write("% FREQ_IF3=0\n")
start_file.write("% FREQ_IF4=0\n")
start_file.write("% FREQ_IF5=0\n")
start_file.write("% FREQ_IF6=0\n")
start_file.write("% FREQ_IF7=0\n")
start_file.write("% FREQ_IF8=0\n")
start_file.write("% FREQ_IF9=0\n")
start_file.write("% FREQ_IF10=0\n")
start_file.write("% FREQ_IF11=6.0E9\n")
start_file.write("% FREQ_IF12=6.0E9\n")
start_file.write("% FREQ_IF13=0\n")
start_file.write("% FREQ_IF14=0\n")
start_file.write("% FREQ_IF15=0\n")
start_file.write("% FREQ_IF16=0\n")
start_file.write("% FREQ_IF17=0\n")
start_file.write("% FREQ_IF18=0\n")
start_file.write("% FREQ_IF19=0\n")
start_file.write("% FREQ_IF20=0\n")
start_file.write("% FREQ_IF21=0\n")
start_file.write("% FREQ_IF22=0\n")
start_file.write("% FREQ_IF23=0\n")
start_file.write("% FREQ_IF24=0\n")

start_file.write("% FE1=\n")
start_file.write("% FE2=\n")
start_file.write("% FE3=\n")
start_file.write("% FE4=\n")
start_file.write("% FE5=\n")
start_file.write("% FE6=\n")
start_file.write("% FE7=\n")
start_file.write("% FE8=\n")
start_file.write("% FE9=\n")
start_file.write("% FE10=\n")
start_file.write("% FE11=H40\n")
start_file.write("% FE12=H20ch2\n")
start_file.write("% FE13=\n")
start_file.write("% FE14=\n")
start_file.write("% FE15=\n")
start_file.write("% FE16=\n")
start_file.write("% FE17=\n")
start_file.write("% FE18=\n")
start_file.write("% FE19=\n")
start_file.write("% FE20=\n")
start_file.write("% FE21=\n")
start_file.write("% FE22=\n")
start_file.write("% FE23=\n")
start_file.write("% FE24=\n")

start_file.write("% MMC_CMD1=MCL\n")
start_file.write("% MMC_CMD2=MOP\n")
start_file.write("% MMC_CMD3=\n")
start_file.write("% MMC_CMD4=\n")
start_file.write("% ON_NTOTAL=6\n")
start_file.write("% ON_NSEQUENCE=6\n")
start_file.write("% ON_TINTEG=5\n")
start_file.write("% ON_COORD_SYS=AZEL\n")
#-------------------------------
#  よくわからんぞーーん
#-------------------------------
start_file.write("% ON1=(0.005556,0.000000)\n")
start_file.write("% ON2=(0.000000,0.000000)\n")
start_file.write("% ON3=(-0.005556,0.000000)\n")
start_file.write("% ON4=(0.000000,0.005556)\n")
start_file.write("% ON5=(0.000000,0.000000)\n")
start_file.write("% ON6=(0.000000,-0.005556)\n")
start_file.write("% OFF_NUSED=1\n")
start_file.write("% OFF_TINTEG=5\n")
start_file.write("% OFF_COORD_SYS=RADEC\n")
start_file.write("% OFF1=(0.100000,0.000000)\n")
start_file.write("% OFF2=(0.0,0.0)\n")
start_file.write("% OFF3=(0.0,0.0)\n")
start_file.write("% OFF4=(0.0,0.0)\n")
start_file.write("% OFF5=(0.0,0.0)\n")
start_file.write("% OFF6=(0.0,0.0)\n")
start_file.write("% OFF7=(0.0,0.0)\n")
start_file.write("% OFF8=(0.0,0.0)\n")
start_file.write("% OFF9=(0.0,0.0)\n")
start_file.write("% NSEQUENCE=100\n")
start_file.write("% CALIB_TINTEG=5\n")
start_file.write("% CALIB_UNIT=SEQUENCE\n")
start_file.write("% PATTERN=1***1***\n")
start_file.write("% CALIB_INTERVAL=100\n")

start_file.write("% OBS_TYPE=SAM45_LINE\n")
start_file.write("% SAM45_FREQ1=4.312203E10\n")
start_file.write("% SAM45_FREQ2=4.312203E10\n")
start_file.write("% SAM45_FREQ3=4.382054E10\n")
start_file.write("% SAM45_FREQ4=4.282054E10\n")
start_file.write("% SAM45_FREQ5=4.34238E10\n")
start_file.write("% SAM45_FREQ6=4.287985E10\n")
start_file.write("% SAM45_FREQ7=4.251934E10\n")
start_file.write("% SAM45_FREQ8=4.251934E10\n")
start_file.write("% SAM45_FREQ9=0\n")
start_file.write("% SAM45_FREQ10=0\n")
start_file.write("% SAM45_FREQ11=0\n")
start_file.write("% SAM45_FREQ12=0\n")
start_file.write("% SAM45_FREQ13=0\n")
start_file.write("% SAM45_FREQ14=0\n")
start_file.write("% SAM45_FREQ15=0\n")
start_file.write("% SAM45_FREQ16=0\n")
start_file.write("% SAM45_FREQ17=0\n")
start_file.write("% SAM45_FREQ18=0\n")
start_file.write("% SAM45_FREQ19=0\n")
start_file.write("% SAM45_FREQ20=0\n")
start_file.write("% SAM45_FREQ21=0\n")
start_file.write("% SAM45_FREQ22=0\n")
start_file.write("% SAM45_FREQ23=0\n")
start_file.write("% SAM45_FREQ24=0\n")
start_file.write("% SAM45_FREQ25=0\n")
start_file.write("% SAM45_FREQ26=0\n")
start_file.write("% SAM45_FREQ27=0\n")
start_file.write("% SAM45_FREQ28=0\n")
start_file.write("% SAM45_FREQ29=0\n")
start_file.write("% SAM45_FREQ30=0\n")
start_file.write("% SAM45_FREQ31=0\n")
start_file.write("% SAM45_FREQ32=0\n")
start_file.write("# NOBS_VERSION=1.180129\n")
start_file.write("# GENERATED_TIME_AND_DATE=%04d-%02d-%02d %02d:%02d:%02d\n" %(Create_Date.year, Create_Date.month, Create_Date.day, Create_Date.hour, Create_Date.minute, Create_Date.second))
start_file.write("# MODIFIED_TIME_AND_DATE=\n")
start_file.write("#\n")



#-------------------------------------------------#
#  Group Tracks
#-------------------------------------------------#
start_file.write("################\n")
start_file.write("# Group Tracks #\n")
start_file.write("################\n")

start_file.write("GROUP GRPTRK ANT RXT SAM45 SYNTHE_K\n")



#-------------------------------------------------#
#  GROUP SYNTHE CONTROLLER
#-------------------------------------------------#
start_file.write("###########################\n")
start_file.write("# GROUP SYNTHE CONTROLLER #\n")
start_file.write("###########################\n")

start_file.write("GROUP SYNTHE SYNTHE_K\n")



#-------------------------------------------------#
#  OPEN LOCAL CONTROLLER
#-------------------------------------------------#
start_file.write("#########################\n")
start_file.write("# OPEN LOCAL CONTROLLER #\n")
start_file.write("#########################\n")

start_file.write("OPEN ANT\n")
start_file.write("OPEN RXT\n")
start_file.write("OPEN IFATT\n")
start_file.write("OPEN SYNTHE\n")
start_file.write("#OPEN SAM45\n")
start_file.write("OPEN MRG\n")
start_file.write("OPEN MMC\n")

start_file.write("OPEN VLBI\n")



#-------------------------------------------------#
#  Set Tracking Parameters
#-------------------------------------------------#
start_file.write("###########################\n")
start_file.write("# Set Tracking Parameters #\n")
start_file.write("###########################\n")

start_file.write("SET GRPTRK TRK_TYPE 'RADEC'\n")
start_file.write("SET GRPTRK SRC_NAME ")
start_file.write("'%s'\n" %(SOURCE_LIST[0][0]))


right_ascension = float(SOURCE_LIST[1][1][0:2]) * 15 + float(SOURCE_LIST[1][1][3:5]) * (15/60.0) + float(SOURCE_LIST[1][1][6:8]) * (15/3600.0) + 0.01 * float(SOURCE_LIST[1][1][9:11]) * (15/3600.0)

if SOURCE_LIST[1][2][0] == "+" or SOURCE_LIST[1][2][0] == "-":
	declination = float(SOURCE_LIST[1][2][0:3]) + float(SOURCE_LIST[1][2][4:6]) / 60.0 + float(SOURCE_LIST[1][2][7:11]) / 3600.0
else:
	declination = float(SOURCE_LIST[1][2][0:2]) + float(SOURCE_LIST[1][2][3:5]) / 60.0 + float(SOURCE_LIST[1][2][6:10]) / 3600.0
start_file.write("SET GRPTRK SRC_POS (%f, %f)\n" %(right_ascension, declination))
start_file.write("SET GRPTRK EPOCH 'J2000'\n")
start_file.write("SET GRPTRK SCAN_COOD 'AZEL'\n")
start_file.write("SET ANT SCAN_COOD_OFF 'RADEC'\n")
start_file.write("SET ANT 2BEAM_MODE 0\n")
start_file.write("SET ANT POINTING 'H40'\n")
start_file.write("SET ANT OTF_MODE 'OFF'\n")


#-------------------------------------------------#
#  Set MRG Parameters
#-------------------------------------------------#
start_file.write("######################\n")
start_file.write("# Set MRG Parameters #\n")
start_file.write("######################\n")

start_file.write("SET MRG GROUP 'vlbi3bz'\n")
start_file.write("SET MRG PROJECT 'proj5'\n")
start_file.write("SET MRG BK_TYPE 'SAMZ'\n")
start_file.write("SET MRG SP_MODE 'OFF'\n")
start_file.write("SET MRG OTF_MODE 'OFF'\n")
start_file.write("SET MRG OFF_HOLD 'ON'\n")




#-------------------------------------------------#
#  Set Synthesizer SYNTHE_K Parameters
#-------------------------------------------------#
start_file.write("################################\n")
start_file.write("# Set Synthesizer SYNTHE_K Parameters #\n")
start_file.write("################################\n")

start_file.write("SET SYNTHE_K VELO 3000.0\n")
start_file.write("SET SYNTHE_K VDEF 'RAD'\n")
start_file.write("SET SYNTHE_K VREF 'LSR'\n")
start_file.write("SET SYNTHE_K INTERVAL 600\n")
start_file.write("SET SYNTHE_K DOPPLER_TRK 'ON'\n")
start_file.write("SET SYNTHE_K OBS_FREQ 4.3E10\n")
start_file.write("SET SYNTHE_K FREQ_IF1 6.0E9\n")
start_file.write("SET SYNTHE_K FREQ_SW 'OFF'\n")
start_file.write("SET SYNTHE_K FREQ_INTVAL 0.0\n")
start_file.write("SET SYNTHE_K RX_NAME 'H40'\n")
start_file.write("SET SYNTHE_K NMA_FLAG 0\n")
start_file.write("SET SYNTHE_K SIDBD_TYP 'USB'\n")
start_file.write("SET SYNTHE_K SCAN_COOD_OFF 'RADEC'\n")



#-------------------------------------------------#
#  Set RXT Parameters
#-------------------------------------------------#
start_file.write("######################\n")
start_file.write("# Set RXT Parameters #\n")
start_file.write("######################\n")
start_file.write("SET RXT VELO 3000.0\n")
start_file.write("SET RXT VDEF 'RAD'\n")
start_file.write("SET RXT VREF 'LSR'\n")
start_file.write("SET RXT OBS_FREQ (%1.4E,%1.4E,0.0,0.0,0.0,0.0,0.0,0.0)\n" %(FREQ_LIST[0], FREQ_LIST[1]))
start_file.write("SET RXT FREQ_IF1 (6.0E9,6.0E9.0,0.0,0.0,0.0,0.0,0.0,0.0)\n")
start_file.write("SET RXT RX_NAME 'H40,H22,,,,,,'\n")
start_file.write("SET RXT RX_NUM 1\n")
start_file.write("SET RXT USE_FLG (1,1,0)\n")
start_file.write("EXECUTE RXT\n")



#-------------------------------------------------#
#  Set IF Parameters
#-------------------------------------------------#
start_file.write("#####################\n")
start_file.write("# Set IF Parameters #\n")
start_file.write("#####################\n")
start_file.write("SET IFATT DESTINATION 'SAM45'\n")



#-------------------------------------------------#
#  SAM Parameters
#-------------------------------------------------#
start_file.write("SET SAM45 INTEG_TIME 5\n")
start_file.write("SET SAM45 OBS_MODE 'POINTING'\n")
start_file.write("SET SAM45 CALB_INT 100\n")
start_file.write("SET SAM45 SEQ_PTN '1***1***'\n")
start_file.write("SET SAM45 OBS_USER 'vlbi3bz'\n")
start_file.write("SET SAM45 OBS_FILE 'scrbp'\n")
start_file.write("SET SAM45 GROUP 'vlbi3bz'\n")
start_file.write("SET SAM45 PROJECT 'proj5'\n")
start_file.write("SET SAM45 VELO 3000.0\n")
start_file.write("SET SAM45 VDEF 'RAD'\n")
start_file.write("SET SAM45 VREF 'LSR'\n")
start_file.write("SET SAM45 IPTIM 0.1\n")
start_file.write("SET SAM45 MAP_POS 0\n")
start_file.write("SET SAM45 SW_MODE 'POS'\n")
start_file.write("SET SAM45 FREQ_SW 0\n")
start_file.write("SET SAM45 FREQ_INTVAL (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)\n")
start_file.write("SET SAM45 MULT_MODE 'OFF'\n")
start_file.write("SET SAM45 MULT_OFF 0.0 \n")
start_file.write("SET SAM45 MULT_NUM (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)\n")
start_file.write("SET SAM45 SIDBD_TYP 'USB,USB,USB,USB,USB,USB,USB,USB,,,,,,,,,,,,,,,,,,,,,,,,'\n")
start_file.write("SET SAM45 REF_NUM (11,11,11,11,11,11,11,11,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)\n")
start_file.write("SET SAM45 REST_FREQ (4.312203E10,4.312203E10,4.382054E10,4.282054E10,4.34238E10,4.287985E10,4.251934E10,4.251934E10,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)\n")
start_file.write("SET SAM45 OBS_FREQ (4.3E10,4.3E10,4.3E10,4.3E10,4.3E10,4.3E10,4.3E10,4.3E10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)\n")
start_file.write("SET SAM45 FREQ_IF1 (6.0E9,6.0E9,6.0E9,6.0E9,6.0E9,6.0E9,6.0E9,6.0E9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)\n")
start_file.write("SET SAM45 RX_NAME 'H40,H40,H40,H40,H40,H40,H40,H40,,,,,,,,,,,,,,,,,,,,,,,,'\n")
start_file.write("SET SAM45 OBS_BAND (1.25E8,1.25E8,1.25E8,1.25E8,1.25E8,1.25E8,1.25E8,1.25E8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)\n")
start_file.write("SET SAM45 ARRAY (1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)\n")
start_file.write("SET SAM45 OTF_MODE 'OFF'\n")
start_file.write("SET SAM45 IFATT (5,5,5,5,5,5,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)\n")
start_file.write("SET SAM45 FQDAT_F0 (4.312203E10,4.312203E10,4.382054E10,4.282054E10,4.34238E10,4.287985E10,4.251934E10,4.251934E10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)\n")
start_file.write("SET SAM45 FQDAT_FQ (4.305954E10,4.318451E10,4.305954E10,4.318451E10,4.375805E10,4.388302E10,4.275805E10,4.288302E10,4.336131E10,4.348628E10,4.281737E10,4.294233E10,4.245686E10,4.258182E10,4.245686E10,4.258182E10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)\n")
start_file.write("SET SAM45 FQDAT_CH (4096,1,4096,1,4096,1,4096,1,4096,1,4096,1,4096,1,4096,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)\n")

start_file.write("SET SAM45 TRK_TYPE 'RADEC'\n")
start_file.write("SET SAM45 SRC_NAME \n")
start_file.write("'%s'\n" %(SOURCE_LIST[0][0]))
start_file.write("SET SAM45 SRC_POS (%f, %f)\n" %(right_ascension, declination))
start_file.write("SET SAM45 EPOCH 'J2000'\n")
start_file.write("SET SAM45 SCAN_COOD 'AZEL'\n")
start_file.write("SET SAM45 CH_BIND (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)\n")
start_file.write("SET SAM45 CH_RANGE (1,4096,1,4096,1,4096,1,4096,1,4096,1,4096,1,4096,1,4096,1,4096,1,4096,1,4096,1,4096,1,4096,1,4096,1,4096,1,4096,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)\n")
start_file.write("SET SAM45 QL_AUTOSTOP 'OFF'\n")
start_file.write("SET SAM45 QL_RMSARY 'A01'\n")
start_file.write("SET SAM45 QL_POINTMODE 'SEQ'\n")
start_file.write("SET SAM45 QL_POINTNUM 1\n")
start_file.write("SET SAM45 BIN_NUM 1\n")
start_file.write("SET SAM45 SUB_ARRAY 'OFF'\n")
start_file.write("SET SAM45 MISC_FLAGS_LFS 'ON,ON'\n")
start_file.write("SET SAM45 MISC_FLAGS_MULT 'BEFORE,BEFORE'\n")
start_file.write("SET SAM45 INPUT_MODE 'XX&YY,XX&YY'\n")
start_file.write("SET SAM45 N_SPEC_WINDOW_SUB1 1\n")
start_file.write("SET SAM45 FREQ_PROF_SYNTH_SUB1 'OFF,OFF'\n")
start_file.write("SET SAM45 WIN_FUNC_ID_SUB1 'NONE,NONE'\n")
start_file.write("SET SAM45 START_CHAN_SUB1 (245760,0)\n")
start_file.write("SET SAM45 END_CHAN_SUB1 (278527,0)\n")
start_file.write("SET SAM45 CHAN_AVG_SUB1 (8,0)\n")
start_file.write("SET SAM45 MAKE_HFS_TABLE 'OFF,OFF'\n")
start_file.write("SET SAM45 MISC_FLAGS_HFS 'OFF,OFF'\n")
start_file.write("SET SAM45 BUT_SCALE 'BUT_SCALE_10.def,'\n")
start_file.write("DECIDE MANAGER LOG_ID\n")



#-------------------------------------------------#
#  Moving the antenna to the target
#-------------------------------------------------#
start_file.write("EXECUTE ANT ACTION(CREATE)\n")
start_file.write("EXECUTE SYNTHE ACTION(CREATE)\n")
start_file.write("EXECUTE SYNTHE OFFSET(0.000000,0.000000) TYPE(ZERO)\n")
start_file.write("EXECUTE ANT OFFSET(0.100000,0.000000) TYPE(ZERO)\n")
start_file.write("WAIT_READY ANT\n")
start_file.write("WAIT RXT\n")



#-------------------------------------------------#
#  END
#-------------------------------------------------#
start_file.write("EXECUTE SAM45 ACTION(CLOSE)\n")
start_file.write("EXECUTE SYNTHE ACTION(CLOSE)\n")
start_file.write("WAIT ANT\n")
start_file.write("WAIT RXT\n")
start_file.write("WAIT IFATT\n")
start_file.write("WAIT SYNTHE\n")
start_file.write("WAIT SAM45\n")
start_file.write("WAIT MRG\n")
start_file.write("WAIT MMC\n")
start_file.write("CLOSE ANT\n")
start_file.write("CLOSE RXT\n")
start_file.write("CLOSE IFATT\n")
start_file.write("CLOSE SYNTHE\n")
start_file.write("CLOSE SAM45\n")
start_file.write("CLOSE MRG\n")
start_file.write("CLOSE MMC\n")


start_file.close()





