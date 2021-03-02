# Website_Monitoring_Scripting_Languages
This project contains three seperate scripts, trafficgen, collector, and plot. These scripts work together
to create traffic to a website and measures the number of 200, 404, and 500 http response codes. The 
scripts will then create a graph based on the retrieved information.
--trafficgen--
    This script takes in three arguments, the url of the website to ping, the number of pings per second, and the
    jitter or variation in pings per second. The script works by calculating the upper and lower rps value using the 
    jitter (rps*(1.0-jitter) and rps*(1.0+jitter)) and getting a random value between there. Then, the script gets
    the current time and calulates the time in two seconds. After that, the script performs the random rps*2 number
    of pings, then once that is finished checks how much time is remaining until the 2 seconds has passed, and waits 
    that amount of time.
--collector--
    This script runs while the traffic gen is running and periodically collects the number of 200, 404, and 500 http
    response codes and saves them to a tab seperated file defaulted to "collectedstats.tsv" with the current time as well. 
    This script takes in three optional arguments, the first is the collection interval, by default, this value is set to 
    10 seconds. This script runs with the same get time/wait_time as the traffic gen except the wait time is determied 
    by the interval value. The second optional flag is statsUrl, this is the location of the website which the server
    is running on in case you change the port number, the final flag is statsFile, this is the file name that the 
    stats should be saved to.
--plot--
    This script processes the tab seperated log file created with the collector and uses matplotlib to create a graph
    called "graph.png". All three http status codes are imputted on the same graph. The x axis is the time since the 
    script started running, ex. 10 seconds, 20, 30.. and the y axis is the number of requests per second. This script 
    uses a delta t of one minute, that means the rate of requests is not taken raw from each collection, but rather
    compared against the rate of 1 minute ago, this creates a constantly moving rate to calculate. There are 
    two optional flags, fileName and graphFile, fileName is the name of the log file, graphFile is the
    name of the file you want to save.

Running Instructions:
These scripts should all be in the same folder for the easiest use, plot needs the data pulled from collector.
--trafficgen--
    To run this script enter the name of the script followed by the argument flags and arguments url, rps, and jitter.
    Url should be the website name which you want to ping like http://localhost:8080/
    Rps should be the number of requests per second you want as a whole number, ex 300
    Jitter should be the desired amount of fluctuation for your rps as a number between 0 and 1, ex 0.5
    	    ./trafficgen.py --url <url> --rps <rps> --jitter <jitter>
        ex: ./trafficgen.py --url http://localhost:8080 --rps 500 --jitter 0.3
             or you may call with python
            python3 trafficgen.py --url <url> --rps <rps> --jitter <jitter>
        ex: python3 trafficgen.py --url http://localhost:8080 --rps 500 --jitter 0.3
    If any of these required values are omitted, default values will be provided, the default values
    in order are http://localhost:8080/ 500 0.3

--collector--
    To run this script type the name of the script, you may also add the additional flag "--interval" followed 
    by the desired interval value as a whole value.
            ./collector.py 
        or you may call with python
	    python3 collector.py 
        or  python3 collector.py --interval <interval>
        ex: python3 collector.py --interval 20
--collector flags--
    These are optional flags that may be used to change the default values, any number of these flags may
    be used as long as the values are space seperated and follow the format --flag flagValue --flag flagValue..
    "--interval" is used to change the collection interval of the application, the default value is 10
            ./collector.py --interval <interval>
        ex: ./collector.py --interval 20
    "--statsUrl" is used to change the location that the stats are retrieved from, if you changed the
    port number for example. Default value is http://localhost:8080/stats
            ./collector.py --statsUrl <url>
        ex: ./collector.py --statsUrl http://localhost:9999/stats
    "--statsFile" is used to change the file location that the statistics log file is saved to, the 
    default file name is collectedstats.tsv. The recommended extenstions are .txt and .tsv
            ./collector.py --statsFile <file>
        ex: ./collector.py --statsFile savedstats.txt
    "--seconds" is used to change the number of seconds that the collector will collect for, the default value is
    set to 3600 or one hour.
            ./collector.py --seconds <seconds>
        ex: ./collector.py --seconds 1200

--plot--
    This script has no additional arguments so just use the name of the script.
	    ./plot.py
         or you may call with python
            python3 plot.py
--plot flags--
    These are optional flags that may be used to change the default values, any number of these flags may
    be used as long as the values are space seperated and follow the format --flag flagValue --flag flagValue..
    "--fileName" is used to change the location that the statistics log is read from, the default value
    is collectedstats.tsv
            ./plot.py --fileName <file>
        ex: ./plot.py --fileName savedstats.txt
    "--graphFile" is used to change the file name of the prapg image that is saved, the default value
    is graph.png. Please only use .jpg and .png for this flag
            ./plot.py --graphFile <file>
        ex: ./plot.py --graphFile picture.jpg

Required Extensions
There are a couple required imports for this project that may require installing
    urllib.request
    requests
    matplotlib.pyplot
Some other imports that should be included with python already and wont be an issue include
    sys
    time
    random
