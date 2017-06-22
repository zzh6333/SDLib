from baseclass.SDetection import SDetection
from sklearn.metrics import classification_report
from sklearn import preprocessing
import numpy as np
from sklearn import metrics
import math
from tool import metric
import heapq


class PSA(SDetection):
    def __init__(self, conf, trainingSet=None, testSet=None, labels=None, fold='[1]'):
        super(PSA, self).__init__(conf, trainingSet, testSet, labels, fold)
        # K = top-K vals of cov
        self.k = 3

    def readConfiguration(self):
        super(PSA, self).readConfiguration()
        self.topS = float(self.config['topStandardDeviation'])
        self.topDA = float(self.config['topDegreeofAgreement'])
        self.topDS = float(self.config['topDegSim'])
        self.topR = float(self.config['topRDMA'])


    def buildModel(self):
        self.trStandardDeviation = {}
        self.trDegreeofAgreement = {}
        self.trDegSim = {}
        self.trRDMA = {}

        trainingusernum=len(self.dao.trainingSet_u)
        testusernum=len(self.dao.testSet_u)
        self.trainingtopS=int(self.topS*trainingusernum)
        self.trainingtopDA=int(self.topDA*trainingusernum)
        self.trainingtopDS=int(self.topDS*trainingusernum)
        self.trainingtopR=int(self.topR*trainingusernum)

        self.trStandardDeviation = metric.StandardDeviation(self.dao.trainingSet_u)
        trStandardDeviation = sorted(self.trStandardDeviation.iteritems(), key=lambda d:d[1],reverse=False)
        trStUser = []
        countsd = 0
        while countsd < self.trainingtopS:
            trStUser.append(trStandardDeviation[countsd][0])
            countsd = countsd +1
        print trStUser

        self.trDegreeofAgreement = metric.DegreeofAgreement(self.dao.trainingSet_u,self.dao.trainingSet_i)
        trDegreeofAgreement = sorted(self.trDegreeofAgreement.iteritems(),key=lambda d:d[1],reverse=True)
        trDaUser = []
        countda = 0
        while countda < self.trainingtopDA:
            trDaUser.append(trDegreeofAgreement[countda][0])
            countda = countda +1
        print trDaUser

        self.trDegSim = metric.DegreeofSimilarity(self.dao.trainingSet_u,self.k)
        trDegSim = sorted(self.trDegSim.iteritems(),key=lambda d:d[1],reverse=True)
        trDsUser = []
        countds = 0
        while countds < self.trainingtopDS:
            trDsUser.append(trDegSim[countds][0])
            countds = countds + 1
        print trDsUser

        self.trRDMA = metric.RatingDeviation(self.dao.trainingSet_u,self.dao.trainingSet_i)
        trRDMA = sorted(self.trRDMA.iteritems(), key=lambda d:d[1],reverse=True)
        trRdUser = []
        countrd = 0
        while  countrd < self.trainingtopR:
            trRdUser.append(trRDMA[countrd][0])
            countrd = countrd + 1
        print trRdUser


        self.pred = {}
        for user in self.labels:
            if (user in trStUser) and (user in trDaUser) and (user in trDsUser) and (user in trRdUser):
                self.pred[user] = 1
            else:
                self.pred[user] = 0


    def predict(self):
        self.predLabels = []
        self.trueLabels = []
        for user in self.dao.trainingSet_u:
            self.predLabels.append(int(self.pred[user]))
            self.trueLabels.append(int(self.labels[user]))

        print self.trueLabels
        print self.predLabels
        print classification_report(self.trueLabels, self.predLabels, digits=4)
        print metrics.confusion_matrix(self.trueLabels, self.predLabels)
        return classification_report(self.trueLabels, self.predLabels, digits=4)








