#! /usr/bin/python3

import time
import urllib.request
import sys

def main():
    interval_flag, interval = "--interval", 10  #default interval value = 10 seconds
    url_flag, url = "--statsUrl", "http://localhost:8080/stats" #default url value = http://localhost:8080/stats
    file_flag, fileName = "--statsFile", "collectedstats.tsv"   #default stats file value = collectedstats.tsv
    second_flag, seconds = "--seconds", 3600       #default seconds to run is 3600 or one hour
    try:
        for i, arg in enumerate(sys.argv):    #look for the interval flag and collect the value, if none found, it will default to 10
            if arg == interval_flag:
                interval = sys.argv[i+1]
            elif arg == url_flag:           #look for url flag if users wants something other than localhost, default is http://localhost:8080/stats
                url = sys.argv[i+1]
            elif arg == file_flag:           #look for file name if user wants somethiong different than the default collectedstats.tsv
                fileName = sys.argv[i+1]
            elif arg == second_flag:           #look for file name if user wants somethiong different than the default collectedstats.tsv
                seconds = sys.argv[i+1]
    except Exception:   #user typed --interval but no value after
        print("Invalid flag: defaulting to interval = 10, url = http://localhost:8080/stats, and fileName = collectedstats.tsv")
    try:
        interval = int(interval)
        try:
            seconds = int(seconds)
            if seconds <= 0:
                print("Number of seconds to run must be greater than 0")
            elif seconds < interval:
                print("Number of seconds cannot be less than the collection interval")
            else:
                try:
                    collected_file = ""
                    with open(fileName, "w") as save_file:
                        test_time = time.time()
                        end_time = test_time + seconds    #set end time for one hour from start
                        while test_time < end_time:
                            while_start = time.time()
                            while_end = while_start + interval #10 seconds from start (or whatever interval is)
                            file = urllib.request.urlopen(url)
                            csv_line = ""
                            for line in file:   #read each line and save it to the file
                                decoded_line = line.decode("utf-8")
                                for i, value in enumerate(decoded_line.split()):
                                    if i == 1:
                                        csv_line += value + "\t"
                                print(decoded_line)
                            csv_line = csv_line[:-1]
                            save_file.write(csv_line + "\n")
                            time.sleep(max(0, (while_end - time.time()))) #if process took less than 10 seconds, wait until that 10 seconds is up
                            #while_now = time.time() #reduced from this
                            #if while_now < while_end:   
                            #    while_wait = while_end - while_now
                            #    time.sleep(while_wait)
                            test_time = time.time() #reset test time to test against the end time
                    #save input file
                except Exception as e:
                    print("Unable to connect to url")
        except ValueError:
            print("Number of seconds is not an integer")
    except ValueError:
        print("Interval value is not an integer")


if __name__ == "__main__":
    main()