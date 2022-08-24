

import numpy as np

class Knn:

    def __init__(self,k=3):
        self.k=k

    def fit(self,X_train,y_train):
        self.stock=np.concatenate((X_train,np.array(y_train).reshape(-1,1)),axis=1)

    def predict(self,X_test):

        from collections import Counter

        res=[]
        for vec in X_test:
            distances=[]
            kinds=[]
            for vec2 in self.stock:
                distances.append(  (np.linalg.norm(vec-(vec2[:-1])), vec2[-1] ) )

            ## find k shortest distances

            for i in range(self.k):
                mini=distances[0][0]
                kind=distances[0][1]
                for tup in distances:
                    if tup[0]<mini:
                        mini=tup[0]
                        kind=tup[1]
                kinds.append(kind)

            ## appending the most common in kinds

            res.append(Counter(kinds).most_common(1)[0][0])

        return np.array(res)

    def score(self,X_test,y_test):
        from sklearn.metrics import accuracy_score
        y_pred=self.predict(X_test)
        return accuracy_score(y_test,y_pred)


#function to save model to a file

def save_model_to_file(model,file_name):
    import pickle

    with open(file_name,"wb") as file:
        pickle.dump(model,file)
    print("model was saved")

#function to load model from a file

def load_model(file_name):
    import pickle

    with open(file_name,"rb") as file:
        model=pickle.load(file)

    return model




## function to get the data from the dataset
def get_data():
    import idx2numpy

    X_train = idx2numpy.convert_from_file('MNIST/train-images-idx3-ubyte')
    y_train = idx2numpy.convert_from_file("MNIST/train-labels-idx1-ubyte")

    X_test = idx2numpy.convert_from_file("MNIST/t10k-images-idx3-ubyte")
    y_test = idx2numpy.convert_from_file("MNIST/t10k-labels-idx1-ubyte")

    return X_train, y_train, X_test, y_test





if __name__ == '__main__':

    ##creating model
    knn=Knn(k=5)

    ## getting the data

    X_train, y_train, X_test, y_test = get_data()

    ## reshaping the X_train , X_test

    X_train = X_train.reshape(60000, 28 * 28)
    X_test = X_test.reshape(10000, 28 * 28)

    ## training the model

    knn.fit(X_train,y_train)

    ## we can't upload the model to mongo because of it's size so let's save it to a file

    save_model_to_file(knn, "knn")








