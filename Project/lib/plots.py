import numpy as np
import matplotlib.pyplot as plt
import random
import numpy
import pylab
import lib.model_evaluation as ev

hFea = {
    0: 'Mean of the integrated profile',
    1: 'Standard deviation of the integrated profile',
    2: 'Excess kurtosis of the integrated profile',
    3: 'Skewness of the integrated profil',
    4: 'Mean of the DM-SNR curve',
    5: 'Standard deviation of the DM-SNR curve',
    6: 'Excess kurtosis of the DM-SNR curve',
    7: 'Skewness of the DM-SNR curve'
}


def plot_hist(D, L, title='', showClass=True):
    '''
    Plot Histograms

    Parameters
    ----------
    D : Matrix of features.
    L : Array of labels.
    bi : Number of bins to use in plot, default equal to 10.

    Returns
    -------
    None.

    '''
    D0 = D[:, L == 0]
    D1 = D[:, L == 1]

    for idx in range(D.shape[0]):
        plt.figure()
        plt.suptitle(title, fontsize=16)
        plt.xlabel(hFea[idx])
        if showClass:
            plt.hist(D0[idx, :], bins=70, histtype='stepfilled',
                     density=True, label='Non-Pulsar', color='blue', alpha=0.5)
            plt.hist(D1[idx, :], bins=70, histtype='stepfilled',
                     density=True, label='Pulsar', color='red', alpha=0.5)
        else:
            plt.hist(D[idx, :], bins=70, histtype='stepfilled',
                     density=True, label='Dataset', color='green', alpha=0.5)
        plt.legend()
        plt.tight_layout()

    plt.show()


def plot_scatter(D, L):
    '''
    Plot Scatter

    Parameters
    ----------
    D : Matrix of features.
    L : Array of labels.

    Returns
    -------
    None.

    '''

    D0 = D[:, L == 0]
    D1 = D[:, L == 1]

    for idx1 in range(D.shape[0]):
        for idx2 in range(D.shape[0]):
            if idx1 == idx2:
                continue
            plt.figure()
            plt.xlabel(hFea[idx1])
            plt.ylabel(hFea[idx2])
            plt.scatter(D0[idx1, :], D0[idx2, :],
                        label='Non-Pulsar', color='blue', linewidths=1)
            plt.scatter(D1[idx1, :], D1[idx2, :],
                        label='Pulsar', color='red', linewidths=1)
            plt.legend()
            plt.tight_layout()  # Use with non-default font size to keep axis label inside the figure
            #plt.savefig('scatter_%d_%d.pdf' % (idx1, idx2))
        plt.show()


def plot_scatter_matrix(D, L, subtitles=True):

    D0 = D[:, L == 0]
    D1 = D[:, L == 1]

    fig, axs = plt.subplots(D.shape[0], D.shape[0])
    for idx1 in range(D.shape[0]):
        for idx2 in range(D.shape[0]):
            if idx1 == idx2:
                axs[idx1, idx2].hist(
                    D0[idx1, :], bins=70, histtype='stepfilled', label='Non-Pulsar', color='blue', alpha=0.5)
                axs[idx1, idx2].hist(
                    D1[idx1, :], bins=70, histtype='stepfilled', label='Pulsar', color='red', alpha=0.5)
                continue
            axs[idx1, idx2].scatter(
                D0[idx1, :], D0[idx2, :], label='Non-Pulsar', color='blue')
            axs[idx1, idx2].scatter(
                D1[idx1, :], D1[idx2, :], label='Pulsar', color='red')
            axs[idx1, idx2].set(xlabel=hFea[idx1], ylabel=hFea[idx2])
    if subtitles:
        plt.legend()
    plt.tight_layout()
    plt.rcParams["figure.figsize"] = (50, 50)
    plt.show()


def plot_heatmap(D, title=''):
    L = hFea.values()
    fig, ax = plt.subplots()
    im = ax.imshow(D)

    # Show all ticks and label them with the respective list entries
    ax.set_xticks(np.arange(len(L)))
    ax.set_yticks(np.arange(len(L)))

    # Rotate the tick labels and set their alignment
    plt.setp(ax.get_xticklabels(), ha="right", rotation_mode="anchor")

    # Loop over data dimensions and create text annotations
    for i in range(len(L)):
        for j in range(len(L)):
            text = ax.text(j, i, D[i, j], ha="center", va="center", color="white")

    ax.set_title(title)
    fig.tight_layout()
    plt.show()


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
    plt.savefig(name,dpi=1200)
    return


def bayesErrorPlot(dcf, mindcf, effPriorLogOdds, model, calibarted=None, lambd=1e-4):
    name=model+"bayesErrorPlot"
    if calibarted == True:
        calibrates="  Calibrated - lambda: "+ str(lambd)
        name="Calibarted" + model+"bayesErrorPlot"
    else:
        calibrates=""
    
    plt.figure()
    plt.plot(effPriorLogOdds, dcf, label='act DCF', color='r')
    plt.plot(effPriorLogOdds, mindcf, label='min DCF', color='b', linestyle="--")
    plt.xlim([min(effPriorLogOdds), max(effPriorLogOdds)])
    plt.legend([model + " - act DCF" + calibrates, model+" - min DCF"])
    plt.xlabel("prior log-odds")
    plt.ylabel("DCF")
    plt.savefig(name,dpi=800)
    return


def plotROC(FPR1, TPR1, FPR2, TPR2, FPR3, TPR3):
    plt.figure()
    plt.grid(linestyle='--')
    plt.plot(FPR1, TPR1, linewidth=2, color='r')
    plt.plot(FPR2, TPR2, linewidth=2, color='b')
    plt.plot(FPR3, TPR3, linewidth=2, color='g')
    plt.legend(["MVG Tied Full-Cov", "Logistic Regression", "Linear SVM"])
    plt.xlabel("FPR")
    plt.ylabel("TPR")
    plt.savefig("ROC",dpi=800)
    return


def plotDET(FPR1, FNR1, FPR2, FNR2, FPR3, FNR3):
    plt.figure()
    plt.grid(linestyle='--')
    plt.plot(FPR1, FNR1, linewidth=2, color='r')
    plt.plot(FPR2, FNR2, linewidth=2, color='b')
    plt.plot(FPR3, FNR3, linewidth=2, color='g')
    plt.legend(["MVG Tied Full-Cov", "Logistic Regression", "Linear SVM"])
    plt.xlabel("FPR")
    plt.ylabel("TPR")
    plt.savefig("DET",dpi=800)
    return






