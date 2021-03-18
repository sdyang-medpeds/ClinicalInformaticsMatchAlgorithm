# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 11:13:55 2021

@author: sdy001
"""

from ApplicantMatchAttempt import *
from Constraint import *

class Program:

    def __init__(self, name="", id=-1, maxSlots=-1):
        self.name = name
        self.id = id
        self.maxSlots = maxSlots
        self.matchList = [] #unordered
        self.rankList = [] #ordered
        self.constraints = []
        self.applicantHistory = []
        
    def RecordAttemptResult(self, applicant, iteration, result):
        myMatchAttempt = ApplicantMatchAttempt(applicant, self, iteration, 
                                               result=result, msg="Normal iteration - result")
        self.applicantHistory.append(myMatchAttempt)
    
    def RecordAttempt(self, applicant, iteration):
        myMatchAttempt = ApplicantMatchAttempt(applicant, self, iteration, 
                                               result=False, msg="Normal iteration - attempt")
        self.applicantHistory.append(myMatchAttempt)
        
    def RecordBumpApplicant(self, applicant, iteration=-1, bumper=""):
        myMatchAttempt = ApplicantMatchAttempt(applicant, self, iteration=iteration, 
                                               result=False, msg="Bumped Applicant", 
                                               bumper = bumper)
        self.applicantHistory.append(myMatchAttempt)        
        
    def PrintProgShort(self):
        return self.id + ": " + self.name
    
    def PrintConstraints(self):
        if len(self.constraints) <= 0:
            return ""
        
        string = str(len(self.constraints)) + " constraints: "
        
        for i in range(0, len(self.constraints)):
            if i > 0:
                string += ", "
            string += self.constraints[i].strConstraint()
        return string
            
    def PrintRankList(self):
        returnstr = ""
        isFirst = True
        for eachApplicant in self.rankList:
            if isFirst:
                isFirst = False
            else:
                returnstr += ", "
            returnstr += eachApplicant.PrintApplicantShort()
        return returnstr
            
    
    def ResetMatchList(self):
        """
        processes match list and ensures that all applicants in the match 
        list are also pointing to this program

        Returns
        -------
        None.

        """
        for eachApplicant in self.matchList:
            eachApplicant.match = self

    def PrintResult(self):
        """
        Returns  printable string of the result
        """
        if len(self.matchList) <= 0:
            return "Unfortunately: " + self.name + " did not match any applicants"
        mystring = self.name + " matched: "
        isFirst = True
        for eachApplicant in self.matchList:
            if isFirst:
                isFirst = False
            else:
                mystring += "\n"
            mystring += eachApplicant.name
        return mystring

    def NumSlotsAvailable(self):
        if self.maxSlots < 0:
            print("Error: max slots undefined for " + self.name)
            return 0
        return self.maxSlots - len(self.matchList)

    def GetApplicantRank(self, applicant):
        """
        Returnts the number in the rank list that applicant is ranked
        0 is best
        """
        return self.rankList.index(applicant)

    def IsApplicantRankedHigher(self, applicant):
        """
        Compare the applicant with those on the matchList
        If the applicant ranks higher, than return the bumped applicant
        returns True if someone should get bumped
        """
        applicantRank = self.GetApplicantRank(applicant)

        for eachApplicant in self.matchList:
            for i in range(0, len(self.rankList)-1):
                if eachApplicant == self.rankList[i]:
                    if applicantRank < i:
                        return True
        return False

    def GetApplicantByRank(self, rank):
        """
        rank is an index into the Rank List, 0 is the top rank
        """
        return self.rankList[rank]


    def FindLowestRankedApplicantInList(self, applicantList):
        """
        retruns the lowest ranked applicant in the list for this program
        """
        tempRankList = [] #collection of rank spots

        for eachApplicant in applicantList:
            tempRankList.append(self.GetApplicantRank(eachApplicant))

        #will sort descending, so lowest ranked applicant is first
        #pdb.set_trace()
        tempRankList.sort(reverse=True)
        return self.GetApplicantByRank(tempRankList[0])



    def GetTopRankInApplicantList(self, applicantList):
        """
        Returns the top rank for this program in the applicantList
        -1 if applicantList is empty
        """
        topRank = -1
        for eachApplicant in applicantList:

            applicantRank = self.GetApplicantRank(eachApplicant)
            if topRank == -1 or applicantRank < topRank:
                topRank = applicantRank
        return topRank        

    def GetTopRankOfMatchedApplicants(self):
        """
        Returns the highest rank of all the matched applicants
        -1 if match list is empty
        """
        return self.GetTopRankInApplicantList(self.matchList)

    def GetApplicantIdList(self, applicantList):
        idList = []
        for eachApplicant in applicantList:
            idList.append(eachApplicant.id)
        return idList

    def ListToRanks(self, myListOfApplicants):
        ranks = []
        for eachApplicant in myListOfApplicants:
            ranks.append(self.rankList.index(eachApplicant))
        ranks.sort()
        return ranks

    def MatchListToRanks(self):
        """
        Return a list of ranks for the applicants who are on the match list
        """
        return self.ListToRanks(self.matchList)