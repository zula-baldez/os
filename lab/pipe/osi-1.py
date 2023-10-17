import subprocess
import matplotlib.pyplot as plt
import time
import re
from time import sleep
##
#cpu: [union,idct]; cache: [prefetch-l3-size,cache-ways]; io: [ioprio,ioport]; memory: [lockbus,mmaphuge-mmaps]; network: [netlink-task,sockdiag]; pipe: [sigpipe,pipeherd-yield]; sched: [resched,sched-runtime]
##
def run_stress_ng(command):
    print(command)
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Функция для построения графика
def plot_graph(timestamps, data, name, isList):
    plt.figure(figsize=(10, 6))
    print(data)

    if not isList:
        for sublist in data:
            plt.plot(timestamps, sublist)
            print(sublist)
    else:
        plt.plot(timestamps, data)

    plt.title('System Performance')
    plt.grid(True)
    plt.savefig(name)
    return 
    


def pipe_test():
    c_sw = []
    for i in range(1, 17, 5):
        sp = run_stress_ng(f'sudo perf stat -e context-switches stress-ng --sigpipe {i} --timeout 20')
        output = sp.communicate()[1]

        output = output.split('\n')

        c_s_l = output[6]
        c_s_l = re.sub(r'\s+', ' ', c_s_l)
        c_s_l = re.sub(r',', '.', c_s_l)
        c_s_l = c_s_l.split(' ')
        j = 1
        switch_num = 0
        while(c_s_l[j].isnumeric()): 
            switch_num = switch_num*1000 + float(c_s_l[j])
            j+=1
        c_sw.append(switch_num)
    plot_graph([i for i in range(1, 17, 5)], c_sw, f'sigpipe', True)


pipe_test()