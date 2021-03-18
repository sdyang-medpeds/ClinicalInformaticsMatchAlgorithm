# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 11:39:20 2021

@author: sdy001
"""

from Applicant import *
from ProgramController import *

import logging
logger = logging.getLogger("match")


class MatchController:
    def __init__(self, applicants="", programs="", expectedResults = "", expectedResultsApps=""):
        """
        Parameters
        ----------
        applicants : Dict, optional
            applicants where key is ID. The default is "".
        programs : list, optional
            programs. The default is "".
        expectedResults : dict, optional
            programs where key is ID. The default is "".
        expectedResultsApps: dict, optional
            applicants where key is ID

        Returns
        -------
        None.

        """
        self.name = ""
        self.applicants = applicants
        self.programs = programs
        self.expectedResults = expectedResults
        self.expectedResultsApps = expectedResultsApps

    def RunMatch(self):
        """
        Runs the match based on preloaded data
        """
        iteration = 1
        unmatchListPrev = []
        hasConvergence = False
        while(not hasConvergence):
            logger.info("Matching the applicants, iteration " + str(iteration))        
        
            for eachApplicant in self.applicants:
                self.CIMatch(self.applicants[eachApplicant], iteration)
                
            unmatchedList = self.GetUnmatched()
            logger.info("After iteration " + str(iteration) + ", there are " + 
                         str(len(unmatchedList)) + " unmatched applicants.")
            
            if MatchController.CompareLists(unmatchListPrev, unmatchedList) == 0:
                logger.info("No change was made to the unmatched list in the last iteration")
                hasConvergence = True
    
            unmatchListPrev = unmatchedList  
            iteration += 1            
        
    def CIMatch(self, applicant, iteration=-1):
        """
        Returns true if there is a match, false otherwise
        
        iteration if wanting to track the number of times you are looping through
        """
        if applicant.match != -1:
            return True
    
        for rankedProgram in applicant.rankList:
            logger.debug("Attempting match for " + applicant.name + " with " + rankedProgram.name)
            
            applicant.RecordAttempt(rankedProgram, iteration)
            
            myController = ProgramController(rankedProgram)
            
    
            result = myController.matchCIApplicant(applicant,iteration)
            
            applicant.RecordAttemptResult(rankedProgram, iteration, result)
            
            if result == True:
                logger.debug("Temp Match " + applicant.name + " with " + rankedProgram.name)
                return True
            
    
        logger.debug("No Match for " + applicant.name )
        return False 
    
    def VerifyResults(self):
        """
        Compares the matches listed in the programs with the applicant matches
        
        The matches should be consistent
        
        Returns the number of inconsistencies
        """
        errorCount = 0
        for eachProgram in self.programs:
            for eachMatchedApp in eachProgram.matchList:
                if eachMatchedApp.match.id != eachProgram.id:
                    logger.debug("Error in consistency: matched Applicant " + eachMatchedApp.PrintApplicantShort
                                 + " matches to program " + str(eachMatchedApp.match.id)
                                 + " not " + str(eachProgram.id))
                    errorCount += 1
        return errorCount
        
        
    
    def CompareResultsWithExpected(self, caseFolder):
        """
        Compares the matches in my applicants / programs with the preloaded
        Expected results
        
        caseFolder: string, the name of the folder where the source data is

        Returns
        -------
        int - number of erros

        """
    
        #checking with results
        logger.info("Checking results for " + caseFolder)
        #pdb.set_trace()
        ErrorCount = 0
        
        for eachProgram in self.programs: 
            logger.info("For program: " + eachProgram.name)
            count = 0
            for eachApplicant in eachProgram.matchList:
                if self.expectedResults[eachProgram.id].count(eachApplicant.id) <= 0:
                    logger.info("Applicant, " + eachApplicant.name + " was not expected to match with this program")
                    count += 1
                    ErrorCount += 1
            if count == 0:
                logger.info("\tProgram: " + eachProgram.name + " is correct.")
            else:
                logger.info("\tERROR in Program Match: " + caseFolder)
                
        for eachApplicant in self.applicants.values():
            count = 0
            if eachApplicant.match == -1:
                if (self.expectedResultsApps.__contains__(eachApplicant.id) == True and
                    len(self.expectedResultsApps[eachApplicant.id]) > 0 and 
                    self.expectedResultsApps[eachApplicant.id][0] != ""):
                    ErrorCount += 1
            else:
                if (not eachApplicant.id in self.expectedResultsApps or 
                    eachApplicant.match.id != self.expectedResultsApps[eachApplicant.id][0]):
                    ErrorCount += 1
                    count += 1
                if count == 0:
                    logger.info("\tApplicant: " + eachApplicant.name + " is correct.")
                else:
                    logger.info("\tERROR in applicant Match: " + caseFolder)
        return ErrorCount
        
        
    
    def PrintApplicantTrace(self):
        """
        prints a string of text for each applicant and their experience through
        the algorithm
        
        for debugging purposes

        Returns
        -------
        List of strings.

        """
        retlines = []
        isFirst = True
        for eachApplicant in self.applicants:
            retlines.append("")
            retlines.append("Match Trace for Applicant: " + self.applicants[eachApplicant].PrintApplicantShort())
            retlines.append("Applicant Rank List: " + self.applicants[eachApplicant].PrintRankList())
            
            i = 1
            for eachAttempt in self.applicants[eachApplicant].applicantHistory:
                retlines.append("Trace " + str(i) + ": ")
                retlines.append(eachAttempt.PrintAttemptForApplicant())
                i +=1
            retlines.append("End Match Trace for Applicant: " + self.applicants[eachApplicant].PrintApplicantShort())
        return retlines
            
    def PrintProgramTrace(self):
        """
        prints a string of text for each program and their experience through 
        the algorithm
        
        for debugging purposes

        Returns
        -------
        None.

        """
        retlines = []
        for eachProgram in self.programs:
            retlines.append("")
            retlines.append("Match Trace for Program: " + eachProgram.PrintProgShort())
            retlines.append("Program Rank List: " + eachProgram.PrintRankList())
            
            isFirst = True
            for eachConstraint in eachProgram.constraints:
                if isFirst:
                    retlines.append("Constraints: ")
                    isFirst = False
                retlines.append(eachConstraint.strConstraint())
                
            if len(eachProgram.constraints) <= 0:
                retlines.append("No Constraints.")
            
            i = 1
            retlines.append("Match attempts:")
            for eachAttempt in eachProgram.applicantHistory:
                retlines.append("Trace " + str(i) + ": ")
                retlines.append(eachAttempt.PrintAttemptForProgram())
                i +=1
            retlines.append("End Match Trace for Program: " + eachProgram.PrintProgShort()) 
        return retlines
    
        
    
    def PrintResults(self):
        resultString = ""
        for eachProgram in self.programs:
            resultString += eachProgram.PrintResult()
        return resultString

    def GetProgramById(programList, ID):
        for eachProgram in programList:
            if eachProgram.id == ID:
                return eachProgram
    
    def GetApplicantById(applicantDict, ID):
        return applicantDict[ID]
          
        
    def GetUnmatched(self):
        """
        Returns the list of unmatched applicants

        Parameters
        ----------
        applicants :list of applicants
            

        Returns
        -------
        list of applicants without a matched program

        """
        unmatchedList = []
        for applicant in self.applicants.values():
            if applicant.match == -1:
                unmatchedList.append(applicant)
        return unmatchedList
    
    def CompareLists(applist1, applist2):
        """
        compares the applicants on list 1 and 2

        Parameters
        ----------
        list1 : applicants list
            DESCRIPTION.
        list2 : applicants list
            DESCRIPTION.

        Returns
        -------
        zero if equal, -1 if not

        """
        if len(applist1) != len(applist2):
            return -1
        
        if set(applist1) == set(applist2):
            return 0
        
    def AggregateResults(self):
        """
        Aggregates the results into a printable dictionary

        Parameters
        ----------


        Returns
        -------
        dictionary of results, organized by applicants

        """
        resultList = []
        for eachApplicant in list(self.applicants.values()):
            resultDict = { "id": eachApplicant.id, 
                              "name": eachApplicant.name 
                              }
            if eachApplicant.match != -1:
                resultDict["match"] = eachApplicant.match.name
            else:
                resultDict["match"] = None
            resultList.append(resultDict)
        return resultList        
        
        return -1
        
    