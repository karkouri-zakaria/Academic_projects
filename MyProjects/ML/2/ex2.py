import numpy as np
import matplotlib.pyplot as plt

def Training_set(PATH):
    import csv
    with open(PATH) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=','); data= np.array([ row for row in csv_reader],dtype='f')
    return(data)
    
def sigmoid(x):
  return 1 / (1 + np.exp(-x))

def costFunction(theta,X, y):
    m = len(y);
    h = sigmoid(np.dot(X, theta))
    J = (-np.dot(y.T, np.log(h))-np.dot((1-y).T, np.log(1-h)))/m
    return(J)

def Gradient(theta, X, y):
    m = len(y);
    h = sigmoid(np.dot(X, theta))
    grad = (np.dot(X.T,(h-y)))/m
    return(grad)

def costFunctionReg(theta, X, y, Lambda):
    m = len(y);
    h = sigmoid(np.dot(X, theta))
    theta1=np.append(np.array([[0]]),theta[1:]).reshape(len(theta),1)
    p = 2*Lambda/m * (np.dot(theta1.T,theta1))
    J = (-np.dot(y.T, np.log(h))-np.dot((1-y).T, np.log(1-h)))/m+p
    return(J)

def gradFunctionReg(theta, X, y, Lambda):
    m ,n = X.shape
    h = sigmoid(np.dot(X, theta))
    theta1=np.append(np.array([[0]]),theta[1:])
    grad = np.dot(X.T,(h-y)) + (Lambda/m)*theta1.reshape(len(theta),1)
    return(grad)

def fminunc(Cost,Grad,initial_theta,args):
    import scipy.optimize as op
    theta = op.fmin_l_bfgs_b(func=Cost, fprime=Grad, x0=initial_theta, approx_grad=True, args=(args[0], args[1].flatten()))[0]
    cost = costFunction(theta, args[0], args[1])
    return(cost, theta)

def fminuncReg(Cost,Grad,initial_theta,args):
    import scipy.optimize as op
    theta = op.fmin_tnc(func=Cost, fprime=Grad, x0=initial_theta, args=(args[0], args[1].flatten(),args[2]))[0]
    cost = costFunctionReg(theta, args[0], args[1],args[2])
    return(cost,theta)

def predict(X,theta):
    return(np.rint(sigmoid(np.dot(X,theta))).reshape(len(X),1))

def mapFeature(X1, X2, degree = 3):
    out = np.ones((len(X1),1))
    for i in range(1,degree+1):
        for j in range(0,i+1):
            out=np.append(out,((X1**(i-j))*(X2**j)).reshape(len(X1),1),axis=1)
    return(out)



def plotData(data,D=0,theta=0):
    if D==0 or D==1:
        plt.figure()
        neg=[[data[i][0],data[i][1]] for i,n in enumerate(data[:,2]) if n==0]; neg=np.array(neg)
        pos=[[data[i][0],data[i][1]] for i,p in enumerate(data[:,2]) if p==1]; pos=np.array(pos)
        plt.scatter(neg[:,0],neg[:,1], label="Not Admitted")
        plt.scatter(pos[:,0],pos[:,1], label="Admitted")
        plt.xlabel("Test 1")
        plt.ylabel("Test 2")
        plt.legend()
        if D==1:
                if len(theta) <= 3:
                #% Only need 2 points to define a line, so choose two endpoints
                    plot_x = [min(data[:,1])-2,  max(data[:,1])+2];
                    plot_y = (-1/theta[2])*(np.dot(theta[1],plot_x) + theta[0]);
                    plt.plot(plot_x, plot_y, color="black",label='Decision Boundary')

                else:
                    u = np.linspace(-1, 1.2, 50); v = np.linspace(-1, 1.5, 50);
                    z = np.zeros((len(u), len(v)));

                    for i in range(len(u)):
                        for j in range(len(v)):
                            z[i,j] = np.dot(mapFeature(np.array([u[i]]),np.array([v[j]])),theta)
                    z = z.T 

                    plt.contour(u, v, z,levels=[0.])

                    
                

def main():

    data = Training_set('C:\\Users\\zakar\\Desktop\\A\\Projects\\MyProjects\\ML\\2\\ex2data1.txt'); m,n =data.shape
    X = data[:, : 2].reshape(m,2); y = data[:, 2].reshape(m,1);    
    print('Plotting data with orange indicating (y = 1) examples and blue indicating (y = 0) examples.')
    #plotData(data)
    plt.show()

    X = np.append(np.ones((m, 1)), X,axis=1); initial_theta = np.zeros((n, 1))
    cost, grad = costFunction(initial_theta, X, y), Gradient(initial_theta, X, y)
    print('Cost at initial theta (zeros): ', cost);
    print('Gradient at initial theta (zeros): \n',grad);

    test_theta = np.array([-24, 0.2, 0.2]).reshape(n, 1)
    cost, grad = costFunction(test_theta, X, y), Gradient(test_theta, X, y)
    print('Cost at test theta (zeros): ', cost);
    print('Gradient at test theta (zeros): \n',grad);

    
    cost, theta = fminunc(costFunction, Gradient, initial_theta, [X, y.flatten()])
    print('Cost at theta found by fminunc: ', cost)
    print("theta : ", theta)

    #plotData(data,D=1,theta=theta)
    plt.show()

    print('For a student with scores 45 and 85, we predict an admission probability of: ', sigmoid(np.dot([1, 45, 85],theta)))
    print('Train Accuracy: ', np.mean((predict(X,theta) == y)) * 100)
    

def main2():
    data = Training_set('C:\\Users\\zakar\\Desktop\\A\\Projects\\MyProjects\\ML\\2\\ex2data2.txt'); m,n =data.shape
    X = data[:, : 2].reshape(m,2); y = data[:, 2].reshape(m,1);  
    print('Plotting data with orange indicating (y = 1) examples and blue indicating (y = 0) examples.')
    plotData(data)
    #plt.show()

    X=mapFeature(X[:,0],X[:,1])
    initial_theta = np.zeros((len(X[0]), 1)).reshape(len(X[0]), 1); Lambda = 1

    cost, grad= costFunctionReg(initial_theta, X, y, Lambda), gradFunctionReg(initial_theta, X, y, Lambda)
    print('Cost at initial theta (zeros): ',cost)

""" Lambda = 155
    cost, theta = fminuncReg(costFunctionReg,gradFunctionReg,initial_theta,[X, y.flatten(),Lambda])
    print('Cost at theta found by fminunc: ', cost)
    print("theta : ", theta)
    plotData(data, D=1, theta=theta)
    plt.show()"""






main()
print('----------------------------------------------------')
main2()