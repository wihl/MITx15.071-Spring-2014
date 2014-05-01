# MITx 15.074x Spring 2014 Kaggle Competition
# David Wihl

import csv
import numpy as np
from sklearn import preprocessing
from sklearn.cross_validation import cross_val_score
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.ensemble import ExtraTreesClassifier
from sklearn import metrics

global labelEncoders

class Dataset(object):
    def __init__(self):
        self.labelEncoders = []

    def trainProcess(self,headers, array):
        newRow = [0] * len(headers)
        YOB = []

        factors = []

        for i in xrange(len(headers)):
            factors.append(set([]))
            self.labelEncoders.append(preprocessing.LabelEncoder())

        target = []
    
        for row in array:
            # YOB - to be normalized
            if row[1] != 'NA':
                YOB.append(row[1])

            # Gender, Income, HouseholdStatus, EducationLevel, Party
            factors[0].add(row[2])
            factors[1].add(row[3])
            factors[2].add(row[4])
            factors[3].add(row[5])
            factors[4].add(row[6])

            # Target (Happy = {0,1})
            target.append(int(row[7]))
                
            colnum = 5
            for col in row[8:-1]: # omit last column (votes)
                factors[colnum].add(col)
                colnum += 1

        # Encode Labels
        colnum = 0
        for f in factors:
            self.labelEncoders[colnum].fit(list(f))
            colnum += 1

        # ok, let's add a new cleaned up row 
        rownum = 0
        cleanArray = []
        for row in array:
            newRow = []
            colnum = 0
            if rownum % 1000 == 0 and rownum != 0:
                print rownum
            #demographics
            for col in row[2:7]:
                newRow.append(self.labelEncoders[colnum].transform([col])[0])
                colnum += 1

            # 101 questions
            for col in row[8:-1]:
                newRow.append(self.labelEncoders[colnum].transform([col])[0])
                colnum += 1

            cleanArray.append(newRow)
            rownum += 1

        return cleanArray, target


    def testProcess(self,headers, array):
        userIds = []

        YOB = []

        # ok, let's add a new cleaned up row 
        rownum = 0
        cleanArray = []
        for row in array:
            userIds.append(row[0])

            newRow = []
            colnum = 0
            if rownum % 1000 == 0 and rownum != 0:
                print rownum

            for col in row[2:-1]:
                newRow.append(self.labelEncoders[colnum].transform([col])[0])
                colnum += 1

            cleanArray.append(newRow)
            rownum += 1

        return userIds, cleanArray

# TODO: 1) output submission, 2) tune params, 3) try other classifier
def tune(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=size)


def main():
    nrow = 0
    ds = Dataset()
    print "reading and processing..."
    with open('train.csv', 'rU') as csvfile:
        reader = csv.reader(csvfile, lineterminator='\r')
        headers = reader.next()
        trainData = []
        for row in reader:
            trainData.append(row)
        X_array, target = ds.trainProcess(headers,trainData)

    print "starting train..."
    X = np.array(X_array)
    y = np.array(target)
    print "X shape", X.shape

    #tune(X,y)

    clf = RandomForestRegressor(n_estimators=10, max_depth=None,min_samples_split=1, random_state=0)


    print "starting predictions..."

    nrow = 0
    with open('test.csv', 'rU') as csvfile:
        reader = csv.reader(csvfile, lineterminator='\r')
        headers = reader.next()
        testData = []
        for row in reader:
            testData.append(row)
        userIds, testArray = ds.testProcess(headers, testData)

    X_test = np.array(testArray)
    print "X test shape", X_test.shape
    pred = clf.predict(X_test)
    print pred

    return
    with open('subrf.csv','wb') as f:
        writer = csv.writer(f)
        for u, p in zip(userIds, pred):
            writer.writerow(u,p)



if __name__ == "__main__":
    main()
