# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 12:32:53 2021



@author: sdy001
"""

import logging, pdb, csv, itertools

logger = logging.getLogger("match")

log_format = (
    '[%(filename)s:%(lineno)s-4s %(name)-4s %(message)s')

logging.basicConfig(
    level=logging.DEBUG,   
    format=log_format
)


if not logger.hasHandlers():
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    logger.addHandler(console)

    file = logging.FileHandler("csvload-debug.log")
    file.setLevel(logging.DEBUG)
    logger.addHandler(file)
    
import sys, pathlib

sys.path.append(".\\Code\\Models")
sys.path.append(".\\Code\\Controllers")
sys.path.append(".\\Code\\Views")

import Code.DataLoader as DataLoader
from Code.Views.MatchViewer import *


testCaseFolders = ["testCases-1-1", "testCases-1-2", "testCases-1-3", 
                    "testCases-2-1", "testCases-2-2", "testCases-2-3", 
                    "testCases-3-1", "testCases-3-2", "testCases-4-1", 
                    "testCases-5-1"]
resultsFolder = "results"
debugFolder = "debug"


errorList = []
inconsistencies = []

for caseFolder in testCaseFolders:
    myMatchController = DataLoader.LoadMatchController(caseFolder)
    myMatchViewer = MatchViewer(myMatchController)
    myMatchViewer.DebugToExcel(debugFolder, caseFolder)
    
    myMatchController.RunMatch()
    
    incon = myMatchController.VerifyResults()
    if incon >= 1:
        inconsistencies.append((caseFolder, incon))
    
    errors = myMatchController.CompareResultsWithExpected(caseFolder)
    
    errorList.append((caseFolder, errors) )

    myMatchViewer.WriteResults(resultsFolder + "//MatchResults-" + caseFolder + ".csv")
    myMatchViewer.WriteTrace(debugFolder, caseFolder)

for eachErrorT in errorList:
    print("While running test: " + eachErrorT[0] + ", there are " + str(eachErrorT[1]) + " errors")

for eachIncon in inconsistencies:
    print("While running test: " + eachIncon[0] + ", the matched programs/applicants were not consistent " 
          + str(eachIncon[1]) + " number of times.")
    


