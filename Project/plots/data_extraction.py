# PER ESTRARRE I DATI E PLOTTARLI

import numpy
import random
import matplotlib.pyplot as plt

def plot_DCF(x, y, xlabel, base=10, title=''):
    if title=='':
        name= (str(random.uniform(0, 10))+".png")
    else: name = title
    print(name)
    plt.figure()
    #plt.suptitle(title, fontsize=16)
    plt.plot(x, y[0], label='min DCF prior=0.5', color='b')
    plt.plot(x, y[1], label='min DCF prior=0.9', color='r')
    plt.plot(x, y[2], label='min DCF prior=0.1', color='g')
    plt.xlim([min(x), max(x)])
    plt.xscale("log", base=base)
    plt.legend(["min DCF prior=0.5", "min DCF prior=0.9", "min DCF prior=0.1"],loc='lower right')
    plt.xlabel(xlabel)
    plt.ylabel("min DCF")
    plt.savefig(name)
    return

def extract_minDCFs(fname, n=20):
    """
    fname -> nome file
    n -> numero di righe per ogni prior
    """
    
    minDCFs = {} # Liste -> [[minDCF prior 0,5],[minDCF prior 0,9],[minDCF prior 0,1]]
    
    act_key = ''
    flag = True
    
    with open(fname) as f:
        while True:
            # titolo sezione
            if flag:
                line = f.readline()
                if not line: break
                act_key = line.strip()
                flag = False
                minDCFs[act_key] = []
            # dati
            else:    
                for prior in range(3):
                    dcf_prior = [] 
                    for l in range(n): # n iterazioni per ogni prior
                        line = f.readline()
                        if not line: break
                        attrs = line.split(',')[-1].strip()
                        dcf = float(attrs.split("=")[-1].strip())
                        # print(dcf)
                        dcf_prior.append(dcf)
                    if not line: break
                    minDCFs[act_key].append(dcf_prior)
                if not line: break
                flag = True
                # print(act_key)
                # print(minDCFs[act_key])
       
    return minDCFs


def plot_minDCFs_LR(minDCFs):
    lambdas = numpy.logspace(-5, 2, num=20)  # For Graphichs Use
    
    for key in minDCFs.keys():
        DCFs = minDCFs[key]
        plot_DCF(lambdas, DCFs, "λ", title=key)
        #print(DCFs)


if __name__ == '__main__':
    #minDCFs = extract_minDCFs("LogReg_GraphData.txt", 20)
    minDCFs = extract_minDCFs("minDCFs_QLR.txt", 20)
    
    plot_minDCFs_LR(minDCFs)