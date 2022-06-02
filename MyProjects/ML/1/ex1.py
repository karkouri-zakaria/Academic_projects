import numpy as np
import matplotlib.pyplot as plt

def warmUpExercise():
    print(np.eye(5))

def Training_set(PATH):
    import csv
    with open(PATH) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=','); data= np.array([ row for row in csv_reader],dtype='f')
    return(data)

def computeCost(X,y,theta):
    m = len(y)
    dif=np.dot(X,theta)-y
    J=np.dot(dif.T,dif)/2*m
    return(J)

def gradientDescent(X, y, theta, alpha, num_iters):
    m = len(y)
    J_history = np.zeros((num_iters+1, 1))
    theta_history = np.zeros((num_iters+1, len(theta)))
    J_history[0]= computeCost(X, y, theta)
    theta_history[0, :]=theta.T

    for iter in range(1,num_iters+1):
        theta_prev=theta;
        for j in range(0,len(theta)):
            deriv=np.dot((np.dot(X,theta_prev)-y).T,X[:,j].reshape(m, 1))/m
            theta[j]=theta_prev[j]-alpha*deriv
        J_history[iter] = computeCost(X, y, theta)
        theta_history[iter, :] = theta.T
    return(theta, J_history, theta_history)

def featureNormalize(X):
    X_norm = X; mu = np.zeros((len(X[0]),1)); sigma = np.zeros((len(X[0]),1));
    for p in range(0,len(X[0])):
        mu[p]=np.mean(X[:,p])
        sigma[p]=np.std(X[:,p])
        print(X[:,p],"\n*****\n",mu[p],"\n*****\n",sigma[p])
        if sigma[p]!=0:
            for i in range(0,len(X)):
                X_norm[i,p]=(X[i,p]-mu[p])/(sigma[p])
        else:
            X_norm[:,p]=np.zeros((len(X)+1,1))
    
    return(X_norm, mu, sigma)
    

def plotData(data,D=0,theta=0):
    if D==0 or D==1:
        plt.figure()
        plt.scatter(data[:,0], data[:,1], zorder=0, label ='Training data')
        plt.xlabel("Population of City in 10,000s")
        plt.ylabel("Profit in $10,000s")
        plt.legend()
        if D==1:
            m=len(data[:,0])
            plt.plot(data[:,0],np.dot(np.append(np.ones((m, 1)), data[:,0].reshape(m,1),axis=1),theta),color="red", zorder=1 , label ='Linear regression')
            plt.legend()

    elif D==2:
        plt.figure()
        theta0_vals = np.linspace(-50, 50, 100); theta1_vals = np.linspace(-2, 4, 100)
        J_vals = np.zeros((len(theta0_vals), len(theta1_vals)))
        for i in range(0,len(theta0_vals)):
            for j in range(0,len(theta1_vals)):
                t = [theta0_vals[i], theta1_vals[j]]
                J_vals[i,j] = computeCost(data[:,0], data[:,1]  , t)[0][0]
        from matplotlib import cm
        _, ax = plt.subplots(subplot_kw={"projection": "3d"})
        theta0_vals, theta1_vals = np.meshgrid(theta0_vals, theta1_vals)
        ax.plot_surface(theta0_vals, theta1_vals, J_vals.T, cmap=cm.coolwarm,linewidth=0, antialiased=False)
        ax.set_xlabel('THETA 0')
        ax.set_ylabel('THETA 1')
        ax.set_zlabel('COST')
        ax.contour(theta0_vals, theta1_vals, J_vals.T,np.logspace(-2,3,20), zdir='z', offset=-100, colors='black')
    elif D==3:
        plt.figure()
        m=len(data)
        x1=data[:,0].reshape(m, 1);x2=data[:,1].reshape(m, 1);z=data[:,2].reshape(m, 1)
        ax = plt.figure().add_subplot(projection='3d')
        ax.scatter(x1, x2, z,label='Training data')
        xx = np.linspace(0,5000,25); yy = np.linspace(1,5,25); zz = np.zeros((len(xx),len(yy))) 
        for i in range(0,len(xx)):
            for j in range(0,len(yy)):
                t=np.array([1,xx[i], yy[j]]).reshape(1,3)
                zz[i,j] = np.dot(t,theta);
        xx, yy = np.meshgrid(xx,yy);
        ax.plot_surface(xx, yy, zz.T,linewidth=0, color="red",antialiased=True,alpha=0.5)
        #print(z,"\n next \n", zz)



def main():
    #warmUpExercise()
    data = Training_set('C:\\Users\\zakar\\Desktop\\A\\Projects\\MyProjects\\ML\\1\\ex1data1.txt')

    X = np.array(data[:, 0]); y = np.array(data[:, 1]); m=len(data)
    print('Plotting Data ...computeCost')
    plotData(data)
    plt.show()

    X=np.array_split(X, m);y=np.array_split(y, m)
    X = np.append(np.ones((m, 1)), X,axis=1); theta = np.array([[8.],[3.]])
    iterations = 1500; alpha = 0.02

    print('Running Gradient Descent ...computeCost')
    print(computeCost(X, y, theta))

    theta, J_history,  theta_history = gradientDescent(X, y, theta, alpha, iterations)

    print('Theta found by gradient descent: ',theta[0],theta[1])
    plotData(data,1,theta)
    plt.show()

    print('For population = 35,000, we predict a profit of ',np.dot([1, 3.5],theta)*10000);
    print('For population = 70,000, we predict a profit of ',np.dot([1, 7],theta)*10000);

    plotData(data,D=2)
    plt.show()

def normalEqn(X,y):
    theta=np.dot(np.dot(np.linalg.inv(np.dot(X.T,X)),X.T),y)
    return(theta)

def main2():
    Upload = Training_set('C:\\Users\\zakar\\Desktop\\A\\Projects\\MyProjects\\ML\\1\\ex1data2.txt');data = Upload.copy()
    m=len(data); X = data[:, :2]; y = data[:, 2].reshape(m, 1)

    print('Normalizing Features ...');
    X, mu, sigma = featureNormalize(X)

    X = np.append(np.ones((m, 1)),X,axis=1);

    print('Running gradient descent ...\n');
    alpha = 0.3; num_iters = 50; theta = np.zeros((3,1))
    theta, J_history,  theta_history = gradientDescent(X, y, theta, alpha, num_iters)

    i_J_history=[i for i,_ in enumerate(J_history)]
    plt.plot(i_J_history,J_history)
    plt.show()

    price=np.dot(np.array([1,(1650-mu[0])/sigma[0],(3-mu[1])/sigma[1]]),theta)
    print('Estimate the price of a 1650 sq-ft, 3 br house :', price[0])

    
    data = np.append(Upload[:, :2],y,axis=1)
    print('Solving with normal equations...')
    X = np.append(np.ones((m, 1)),Upload.copy()[:, :2],axis=1)

    theta = normalEqn(X, y)

    plotData(data,3,theta)
    plt.show()
    print('Theta : \n',theta)





    
    


main()
main2() 