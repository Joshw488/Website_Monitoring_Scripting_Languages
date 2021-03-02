#! /usr/bin/python3

import matplotlib.pyplot as plt
import sys

def main():
    file_flag, file_name = "--fileName", "collectedstats.tsv" #default value = collectedstats.tsv
    graph_flag, graph_name = "--graphFile", "graph.png"   #default value = graph.png
    try:
        for i, arg in enumerate(sys.argv):    #look for the flags, if one is found, grab the argument after it
            if arg == file_flag:
                file_name = sys.argv[i+1]
            elif arg == graph_flag:
                graph_name = sys.argv[i+1]
    except Exception as e:
        print("Invalid flag: defaulting to fileName = collectedstats.tsv and graphFile = graph.png")
    try:
        with open(file_name, "r") as stats:
            time_list, fivehun_list, twohun_list, fourhun_list, t_plus  = [], [], [], [], []
            for line in stats:
                split_line = line.split("\t")   #still not very pythonic?
                time_list.append(int(split_line[0]))
                fivehun_list.append(int(split_line[1]))
                twohun_list.append(int(split_line[2]))
                fourhun_list.append(int(split_line[3]))
            #get rates for each return code
            fivehun_rate = calculateRate(fivehun_list)
            twohun_rate = calculateRate(twohun_list)
            fourhun_rate = calculateRate(fourhun_list)
            for time in time_list:  #get the time additional time from start (0, 10, 20... for 10 second intervals)
                t_plus.append(int(time - time_list[0]))
            #format the graph using the t_plus and rates
            plt.plot(t_plus[6:], twohun_rate)
            plt.plot(t_plus[6:], fourhun_rate)
            plt.plot(t_plus[6:], fivehun_rate)
            plt.legend(["200s","404s","500s"])
            plt.ylim(bottom=0)
            plt.xlim(left=0)
            plt.ylabel("RPS (Requests per second)")
            plt.xlabel("Time after start (seconds)")
            plt.savefig(graph_name)
            #plt.show()
    except Exception:
        print("File ", file_name, " could not be found.")
    
    

def calculateRate(base_list): #calculate the one minute rate, starting at the 6th so 1 min has passed
    list_rate = [(x1 - x0)/60 for (x1, x0) in zip(base_list[6:], base_list)]
    return list_rate

if __name__ == "__main__":
    main()
