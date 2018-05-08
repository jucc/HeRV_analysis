#code in this file was copied from Bin's answer in
#https://stackoverflow.com/questions/28200786/how-to-plot-scikit-learn-classification-report


import matplotlib.pyplot as plt
import numpy as np

def plot_classification_report(cr, title='Classification', with_avg_total=False, cmap=plt.cm.coolwarm_r):

    lines = cr.split('\n')

    classes = []
    plotMat = []
    for line in lines[2 : (len(lines) - 3)]:
        #print(line)
        t = line.split()
        # print(t)
        classes.append(t[0])
        v = [float(x) for x in t[1: len(t) - 1]]
        print(v)
        plotMat.append(v)

    if with_avg_total:
        aveTotal = lines[len(lines) - 1].split()
        classes.append('avg/total')
        vAveTotal = [float(x) for x in t[1:len(aveTotal) - 1]]
        plotMat.append(vAveTotal)


    plt.imshow(plotMat, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    x_tick_marks = np.arange(3)
    y_tick_marks = np.arange(len(classes))
    plt.xticks(x_tick_marks, ['precision', 'recall', 'f1-score'], rotation=45)
    plt.yticks(y_tick_marks, classes)
    plt.tight_layout()
    plt.ylabel('Classes')
    plt.xlabel('Metrics')

    plt.show()
    plt.clf()
    plt.cla()
    plt.close()



def  fscore_from_report(cr):
    return cr[-1].split('      ')[-2]
