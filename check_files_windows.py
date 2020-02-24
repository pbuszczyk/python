import os
import time
import subprocess

last_month = 0
last_90_days = 0
last_year = 0
total_no_of_files = 0
text_file = open("./share_names.txt", "r")
dir_in_consideration = ''
atime = 0
total_percentage = 0.0
for line in text_file:
  #print line
  if(1 == 1):
    #print line.split('\t')[0]
    dir_in_consideration = line#.split('\t')[0]
    print(dir_in_consideration)
    last_month = 0
    last_90_days = 0
    last_year = 0
    total_no_of_files = 0
    total_size = 0

    subprocess.call("net use Z: \\\\zmy12nap01\\" + dir_in_consideration.strip(), shell=True)

    for root, dirs, files in os.walk("Z:\\"):
      path = root.split(os.sep)
      for file in files:
        try:
          
          atime =  os.path.getatime(root+os.sep+file)
          total_size = total_size + os.path.getsize(root+os.sep+file)
          total_no_of_files = total_no_of_files + 1
          if(int(time.time()) - atime  <=2592000):
            last_month = last_month + 1
          elif(int(time.time()) - atime <=7776000):
            last_90_days = last_90_days + 1
          elif(int(time.time()) - atime <=31540000):
            last_year = last_year + 1
        except OSError as e:
          error_file = open("error.txt","a")
          error_file.write(file)
          error_file.close()

    #print(dir_in_consideration)
    print('No. of files in last month:%d' %last_month)
    print('No. of files in last 90 days:%d' %last_90_days)
    print('No. of files in last year:%d' %last_year)
    print('Total no. of files not accessed:%d' %(total_no_of_files - (last_month+last_90_days+last_year)))
    print('Total size in MB:%f' %(total_size/1000000.0))

    if(total_no_of_files != 0):
      total_percentage = (last_month+last_90_days+last_year) * 1.0 / total_no_of_files
      total_percentage = total_percentage * 100.0
    else:
      total_percentage = 0.0;

    print('Percentage of files accessed: %f' %total_percentage)
    print('Total no. of files:%d' %total_no_of_files)
    subprocess.call("net use Z: /d", shell=True)
text_file.close()
