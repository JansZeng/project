# 根据时间选择退出刷新当前视频
import datetime

chen_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '2:00:00', '%Y-%m-%d%H:%M:%S')
start_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '5:00:00', '%Y-%m-%d%H:%M:%S')
new_time = datetime.datetime.now()

if new_time > chen_time and new_time < start_time:
    print('2-5点停止运行。')
    os._exit(0)