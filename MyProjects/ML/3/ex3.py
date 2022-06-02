import numpy as np
import matplotlib.pyplot as plt
import pygame


def Training_set(PATH):
    import scipy.io
    return(scipy.io.loadmat(PATH))
    
def plotData(X,D=0,run=True):
    if D==0:
        from random import randint
        pygame.init()
        W,H,FPS=1000,1000,360
        WIN=pygame.display.set_mode((W,H))
        Clock=pygame.time.Clock()
        def draw():
            for h in range(10):
                for j in range(10):
                    p=X[randint(0,4999)]
                    for i in range(20):
                        for k in range(0,381,20):
                            if p[i+k]>=1/8:
                                c=225
                                pygame.draw.rect(WIN,(c*abs(p[i+k])/(max(p)-min(p)), c*abs(p[i+k])/(max(p)-min(p)), c*abs(p[i+k])/(max(p)-min(p))),(j*100+k/4,h*100+i*5,5,5))
        
        draw()
        while run:
            Clock.tick(FPS)
            pygame.display.update()
            pygame.time.delay(5000)
            run = False
            break
        pygame.quit()

def sigmoid(x):
  return 1 / (1 + np.exp(-x))

def costFunctionReg(theta, X, y, Lambda):
    m,n = X.shape
    J = 0
    h = (sigmoid(X@theta)).reshape(m,-1)
    J = (-(y.T@np.log(h))-(1-y).T@(np.log(1-h)))/m + Lambda*np.sum(theta[1:]**2)/(2.*m)
    return J


def gradFunctionReg(theta, X, y, Lambda):
    m ,n = X.shape
    grad = np.zeros(np.size(theta))
    h = (sigmoid(X@theta)).reshape(m,-1)
    grad = X.T@(h-y)/m
    grad[1:] = grad[1:]+Lambda/m*theta[1:].reshape(-1,1)
    return(grad)

def oneVsAll(X, y, num_labels, Lambda):
    import scipy.optimize as op
    m, n = X.shape
    all_theta=np.zeros((num_labels,n+1))
    X = np.append(np.ones((m, 1)), X,axis=1)
    for i in range(num_labels):
        initial_theta=np.zeros((n+1,1))
        theta = op.fmin_l_bfgs_b(func=costFunctionReg, fprime=gradFunctionReg, x0=initial_theta, args=(X, y==(i+1),Lambda), factr=10)
        all_theta[i, :] = theta[0].T
    return(all_theta,theta)   

def predictOneVsAll(theta, X):
    m = X.shape[0]
    X = np.append(np.ones((m, 1)), X, axis=1)
    return (np.argmax(sigmoid(X@theta.T),axis = 1))

def main():
    data = Training_set('C:\\Users\\zakar\\Desktop\\A\\Projects\\MyProjects\\ML\\3\\ex3data1.mat'); 
    X=data['X']; y=data['y']

    input_layer_size  = 400; num_labels = 10

    print('Loading and Visualizing Data ...')
    #plotData(X)

    print('Training One-vs-All Logistic Regression...')
    Lambda = 0.1
    all_theta,theta = oneVsAll(X, y, num_labels, Lambda)
    print(theta[1])
    #pred=predictOneVsAll(all_theta,X)
    #print('Training Set Accuracy: ', np.mean((pred == y)) * 1e3)


main()