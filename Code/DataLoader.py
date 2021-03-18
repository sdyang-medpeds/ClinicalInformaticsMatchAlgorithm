# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 12:09:08 2021

@author: sdy001
"""


import logging, pdb, csv, itertools, os.path

logger = logging.getLogger("match")

from Applicant import *
from Program import *
from Constraint import *
from MatchController import *

def LoadMatchController(caseFolder):
    """
    Loads the data from the given folder

    Parameters
    ----------
    caseFolder : string
        Name of Folder with the data.

    Returns
    -------
    myController : MatchController
        MatchController loaded with the data.

    """
    eachTestCase = caseFolder

    programs = list()
    applicants = dict()
    constraints = dict()
    expectedResults = dict()
    expectedResultsApps = dict()

    input_file = csv.DictReader(open(eachTestCase + "//" + "testDataApplicants.csv"))

    for row in input_file:
        if row["ID"] in applicants:
            logger.debug("Warning: applicant ID " + row["ID"] + " used multiple times")             
        applicants[row["ID"]] = Applicant(row["Name"], row["ID"])


    input_file = csv.DictReader(open(eachTestCase + "//" + "testDataPrograms.csv"))
    for row in input_file:
        programs.append(Program(row["Name"], row["ID"], int(row["MaxSlots"])))


    input_file = csv.DictReader(open(eachTestCase + "//" + "testDataApplicantList.csv"))
    tempRankLists = {}
    # dict accessed by applicant id
        # each applicant has list of tuples (rank, program ID)
    for row in input_file:
        rankTuple = (int(row["Rank"]), row["Program ID"])

        if row["Applicant ID"] in tempRankLists:
            tempRankLists[row["Applicant ID"]].append(rankTuple)
        else:
            tempRankLists[row["Applicant ID"]] = [rankTuple]

    for appRank in tempRankLists:

        a = MatchController.GetApplicantById(applicants, appRank)
        #pdb.set_trace()
        tRankList = []
        tempRankLists[appRank].sort()
        for eachProg in tempRankLists[appRank]:
            tRankList.append(MatchController.GetProgramById(programs, eachProg[1]))

        a.rankList = tRankList

    input_file = csv.DictReader(open(eachTestCase + "//" + "testDataProgramList.csv"))
    tempRankLists = {}
    for row in input_file:
        rankTuple = (row["Rank"], row["Applicant ID"])

        if row["Program ID"] in tempRankLists:
            tempRankLists[row["Program ID"]].append(rankTuple)
        else:
            tempRankLists[row["Program ID"]] = [rankTuple]


    for progRank in tempRankLists:
        p = MatchController.GetProgramById(programs, progRank)

        tRankList = []
        tempRankLists[progRank].sort()
        for eachApp in tempRankLists[progRank]:
            tRankList.append(MatchController.GetApplicantById(applicants, eachApp[1]))

        p.rankList = tRankList        


    input_file = csv.DictReader(open(eachTestCase + "//" + "testDataConstraints.csv"))

    for row in input_file:
        if row["Constraint ID"] in constraints:
            logger.debug("Warning: applicant ID " + row["Constraint ID"] 
                         + " used multiple times")          
        p = MatchController.GetProgramById(programs, row["Program ID"])
        constraints[row["Constraint ID"]] = Constraint(row["Constraint ID"], p, int(row["Slots"]))


    for eachConstraint in constraints.items():
        eachConstraint[1].program.constraints.append(eachConstraint[1])

    input_file = csv.DictReader(open(eachTestCase + "//" + "testDataConstraintList.csv"))
    for row in input_file:
        a = MatchController.GetApplicantById(applicants, row["Applicant ID"])
        constraints[row["Constraint ID"]].applicantList.append(a)


    testFile = eachTestCase + "//" + "testDataExpectedResults.csv"
    if os.path.exists(testFile):
            
        input_file = csv.DictReader(open(testFile))
        
        for row in input_file:
            
            progId = ""
            try:
                progId = row["Program ID"]
            except ValueError:
                progId = ""
                
            
            appId = ""
            try:
                appId = row["Applicant ID"]
            except ValueError:
                appId = ""
            
            if progId in expectedResults and progId != "" :
                if appId != "":
                    expectedResults[progId].append(appId)
            else:
                if appId != "":
                    expectedResults[progId] = [appId]
                
            if appId in expectedResultsApps and progId != "":
                expectedResultsApps[appId].append(progId)
            else:
                if appId != "":
                    expectedResultsApps[appId] = [progId]           

        logger.debug("Loading Test Case: " + caseFolder + ", "
                      + "There are "
                      + str(len(applicants)) + " applicants, and there are" 
                      + str(len(programs)) + " programs." )
    

    myController = MatchController(applicants, programs, expectedResults, expectedResultsApps)
    return myController






