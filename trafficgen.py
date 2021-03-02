#! /usr/bin/python3

import sys
import time
import random
import requests

def main():
    url_flag, url = "--url", "http://localhost:8080/"  #default url is http://localhost:8080/
    rps_flag, rps = "--rps", 500    #default rps is 500
    jitter_flag, jitter = "--jitter", 0.3   #default jitter is 0.3
    try:
        for i, arg in enumerate(sys.argv):    #look for the interval flag and collect the value, if none found, it will default to 10
            if arg == url_flag:
                url = sys.argv[i+1]
            elif arg == rps_flag:           #look for url flag if users wants something other than localhost, default is http://localhost:8080/stats
                rps = sys.argv[i+1]
            elif arg == jitter_flag:           #look for file name if user wants somethiong different than the default collectedstats.tsv
                jitter = sys.argv[i+1]
    except Exception:   #user typed --interval but no value after
        print("Invalid flag: url=", url, " rps=", rps, " jitter=", jitter)
    try:    #validate input
        rps = int(rps)
        if rps > 0:
            try:
                jitter = float(jitter)
                if jitter >= 0.0 and jitter <= 1.0:
                    genTraffic(url, rps, jitter)    #all valid, call traffic gen
                else:
                    print("jitter must be between 0 and 1, please fix argument #3")
            except ValueError:
                print("jitter is not a number, please fix argument #3")
            except Exception:
                print("Error pinging the server")
        else:
            print("rps must be a positive value")
    except ValueError:
        print("rps is not an integer, please fix argument #2")


def genTraffic(url, rps, jitter):
    while True: 
        sec_start = time.time() #calculate the current time and 2 seconds later for the current run
        sec_end = sec_start + 2.0

        lower_rps = int(rps * (1.0 - jitter)) #these could be moved out for better performance
        upper_rps = int(rps * (1.0 + jitter))
        rand_rps = random.randrange(lower_rps, upper_rps)

        for _ in range(rand_rps*2): #do the amount for two seconds (2x)
            requests.get(url)

        time.sleep(max(0, (sec_end - time.time()))) #if there is still more time to wait (taken less than 2 sec), wait that remaining time
        #sec_now = time.time() #reduced from this
        #if sec_now < sec_end:   
        #    sec_wait = sec_end - sec_now
        #    time.sleep(sec_wait)


if __name__ == "__main__":
    main()
