# Last edit: 10/05/2022 - Alex

import numpy
import lib.plots as plt
from lib.dim_reduction import PCA, LDA

def load(fname):
    DList = []
    labelsList = []

    with open(fname) as f:
        for line in f:
            try:
                attrs = line.split(',')[0:8]
                attrs = numpy.array([float (i) for i in attrs])
                attrs = attrs.reshape(8,1)
                label = line.split(',')[8]
                DList.append(attrs)
                labelsList.append(label)
            except:
                print("An error occurred inside the function: 'load(fname)'")

    return numpy.hstack(DList), numpy.array(labelsList, dtype=numpy.int32)


if __name__ == '__main__':
    m = 6
    
    hLabels = {
         0:'Non-Pulsar',
         1:'Pulsar'
        }
    
    D_Train, L_Train = load('data/Train.txt')
    D_Test, L_Test = load('data/Test.txt')
 
<<<<<<< Updated upstream
    plot_hist(D_Train, L_Train, 70)
    plot_scatter(D_Train, L_Train)
=======
    #plt.plot_hist(D_Train, L_Train, bi=100, title='D_Train')
    #plt.plot_scatter(D_Train, L_Train)
    print(D_Train.shape)
>>>>>>> Stashed changes
    
    
    D_PCA = PCA(D_Train, m)
    D_LDA = LDA(D_Train, L_Train, m=3, n=2)
    print(D_LDA.shape)
    D_LDA = numpy.dot(D_LDA.T, D_Train)
    print(D_LDA.shape)
    
    #plt.plot_hist(D_PCA, L_Train, bi=100, title='PCA')
    plt.plot_hist(D_LDA, L_Train, bi=100, title='LDA')




