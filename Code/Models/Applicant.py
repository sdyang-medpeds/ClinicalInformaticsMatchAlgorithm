# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 10:39:42 2021

@author: Samuel Yang
"""

from ApplicantMatchAttempt import *
from Program import *

class Applicant:

    def __init__(self, name="", id=-1):
        self.name = name
        self.id = id
        self.rankList = []
        self.match = -1
        self.bumpHistory = []
        self.applicantHistory = [] #this is a list of match attempts
        
    def RecordAttemptResult(self, program, iteration, result):
        myMatchAttempt = ApplicantMatchAttempt(applicant=self, program=program, 
                                               iteration=iteration, 
                                               result=result, msg="Normal iteration - result")
        self.applicantHistory.append(myMatchAttempt)

    def RecordAttempt(self, program, iteration):
        myMatchAttempt = ApplicantMatchAttempt(self, program, iteration, result=False, msg="Normal iteration - attempt")
        self.applicantHistory.append(myMatchAttempt)
        
    def PrintApplicantShort(self):
        return self.id + ": " + self.name
    
    def PrintRankList(self):
        """
        Returns a string of the rank list
        """
        returnstr = ""
        isFirst = True
        for eachProgram in self.rankList:
            if isFirst:
                isFirst = False
            else:
                returnstr += ", "
            returnstr += eachProgram.PrintProgShort()
        return returnstr
            
    
    def PrintResult(self):
        """
        Returns  printable string of the result
        """
        if self.match == -1:
            return "Unfortunately " + self.name + " did not match"
        return self.name + " matched at " + self.match.name
    
    def BumpApplicant(self, program="", iteration=-1, bumper=""):
        """
        Keeps track of the bumps
        
        iteration : optional, to track algorithm iteration
        bumper : the appicant who is causing the bump

        Returns
        -------
        None.

        """
        bumpedAttempt = ApplicantMatchAttempt(self,program=program, iteration=iteration, 
                                              result=False, msg="Bumped Applicant", 
                                              bumper = bumper)
        self.applicantHistory.append(bumpedAttempt)
        self.match = -1
        
    def AddToRankList(self, program):
        self.rankList.append(program)