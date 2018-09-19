---------------------------------------------------------------
-                vex_to_start.pyの仕様書                      -
-							      -
-                          made by                            -
-                                   Takeru Kawaguchi          -
---------------------------------------------------------------
1. 使い方
使用したい.vexファイルが存在しているディレクトリで、

$python vex_to_start.py

で使用可能である。上記の場合、各パラメータはparam.txtに記述する。
スクリプト実行用パラメータの入力ファイルの名前については、毎回param.txtを使うよりも、
各観測用に記録として残すべく、個別に名前を与えた方が良い。例： r18264a.vtos


2. param.txtの書き方
基本的に全てのパラメータは "hogehoge = "の先に記述する。=の先には""は必要ない。

・USER_NAME = hogehoge
→ ユーザー名を"hogehoge"にする。

・Station_Name = Vm
→ .vexファイルから参照するアンテナを"Vm"にする

・start_time_flag =
→ 希望の観測開始時間を選択することができる。
start_time_flag = original_start
.vexファイルに従う場合に使用。時間がズレる可能性はある。

start_time_flag = any_start
任意の時間で観測を開始する場合に使用。any_time = 2016y136d14h12m00sという形式で次の行に書く必要がある(JST)。

start_time_flag = after_start
現時刻から指定の時間後に観測する場合に使用。現時刻を使用する場合は
after_day = 0
after_hour = 0
after_minute = 0と記述する。

3つから好きなものを選ぶ。使いたいもの以外の行頭に#をつける。
start_time_flag = original_start
#start_time_flag = any_start
#start_time_flag = after_start

・TIME_MOVE_ANTENNA = 1200
→ 1SCAN目にアンテナを動かす時間(天体を追尾する時間)。単位は秒。

・vex_file_name = r16136a.vex
→ 使用する.vexファイルを指定する。

・start_file_flag =
→ .startファイルの名前を決めることができる。

start_file_flag = file_date
ファイル名_作成日で作る場合に使用する。r16136a.vexを使用した場合、r16136a_yymmddhhmmss.startというファイルができる。

start_file_flag = file_selected
start_file_nameで指定した名前のファイルができる。

・after_mmc = 10
→ MMCの一連の流れの後に何秒待つかを決める。

・before_observation = 30
→ 観測を何秒前から行うかを決める。

・time_of_second_move = 20
→ 2SCAN目以降にアンテナを動かす時間。
