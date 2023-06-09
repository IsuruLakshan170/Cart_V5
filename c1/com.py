import time
from util import requestModel
from errorList import errMsg

def communicationProx(mySocket,USERID,MODE,TimerOut,MODELPARAMETERS):
    CLUSTERID = ""
    PEERLIST = []
    MODELPARAMETERLIST = []

    CLusterIDLoop = True
    ModelParamLoop = True
    ################################################################################
    #-----------------------BEGIN----COMMUNICATION SCRIPT--------------------------#
    ################################################################################
    peerTypeReq = ["PEERTYPE",MODE]#-------------Cluster ID REQUEST-----------------
    mySocket.request(requestModel(USERID,peerTypeReq))

    while CLusterIDLoop: #----------------------GET Cluster-------------------------
        tempDataSet = mySocket.RECIVEQUE.copy()
        if len(tempDataSet) > 0:
            for x in tempDataSet:
                tempData = x.get("Data")
                if tempData[0] != "ERROR":
                    if (tempData[0] == "CLUSTERID") & (tempData[2] == "PEERLIST"):
                        mySocket.queueClean(x)
                        CLUSTERID = tempData[1]
                        PEERLIST = tempData[3]
                        print("CLUSTER ID : ",CLUSTERID)
                        print("PEER LIST  : ",PEERLIST)
                        CLusterIDLoop = False
                        break
                else:
                    return MODELPARAMETERLIST
    for x in PEERLIST:#----------------------GET Model params-------------------
        if x != USERID:
            modelReq = ["MODELREQUEST"]
            mySocket.request(requestModel(USERID,modelReq,x))
            print("SEND MODEL REQUEST TO : ",x)
    timerCal =0
    while ModelParamLoop:
        tempDataSet = mySocket.RECIVEQUE.copy()
        if len(tempDataSet) > 0:
            for x in tempDataSet:
                mySocket.queueClean(x)
                if x.get("Data")[0] == "MODELREQUEST":
                    print("MODEL REQUEST FROM : ",x.get("Sender"))
                    modelparameters = ["MODELPARAMETERS",MODELPARAMETERS]
                    mySocket.request(requestModel(USERID,modelparameters,x.get("Sender")))
                    print("MODEL PARAMETERS SEND TO : ",x.get("Sender"))
                elif x.get("Data")[0] == "MODELPARAMETERS":
                    print("MODEL PARAMETERS RECIVED FROM : ",x.get("Sender"))
                    MODELPARAMETERLIST.append(x)
                else:
                    print("UNKNOWN MESSAGE : ",x)
        time.sleep(1)
        timerCal +=1
        if timerCal == TimerOut:
            ModelParamLoop = False
    mySocket.close(0)
    return MODELPARAMETERLIST
    ################################################################################
    #-------------------------END----COMMUNICATION SCRIPT--------------------------#
    ################################################################################