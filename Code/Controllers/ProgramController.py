# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 11:32:59 2021

@author: sdy001
"""

from Applicant import *
from ApplicantController import *

import copy, itertools

import logging
logger = logging.getLogger("match")

class ProgramController:
    def __init__(self, program):
        self.program = program
    
        
    def matchCIApplicant(self, applicant,iteration=-1):
        """
        adds the applicant if possible, taking into account constraints
        another applicant(s) may be bumped
        
        iteration - optional, to track iterations of algorithm

        returns True if there is a match for applicant

        """

        self.program.RecordAttempt(applicant, iteration)

        #easy check to see if the applicant is listed in the program rank list
        if self.program.rankList.count(applicant) <= 0:
            logger.debug("Applicant: " + applicant.name + ", " 
                          + applicant.id + " not in rank list for program: " 
                          + self.program.id)
            return False

        potentialMatchList = copy.copy(self.program.matchList)
        potentialMatchList.append(applicant)
        
        logger.debug("Applicant: " + applicant.name + ", "
                      + applicant.id + " added to potential match list for prog: "
                      + self.program.id)
    
        if len(self.program.constraints) > 0:
            bestMatchList = self.ApplyConstraints(potentialMatchList, iteration)
            #note that apply constraints also calls EnforceSize
        else:
            bestMatchList = self.EnforceSize(potentialMatchList, iteration, applicant)
            
        bumpingApplicants = self.findMissingApplicants(bestMatchList)
        self.bumpApplicants(bumpingApplicants, iteration, applicant)
        
        self.program.matchList = bestMatchList

        
        if bestMatchList.count(applicant) > 0:
            logger.debug("Applicant: " + applicant.PrintApplicantShort() +
                         " temp match to " + self.program.PrintProgShort())
            applicant.match = self.program
            
            self.program.RecordAttemptResult(applicant, iteration, True)
            return True
        
        self.program.RecordAttemptResult(applicant, iteration, False)
        return False
  

    def ApplyConstraints(self, potentialMatchList, iteration=-1):
        """
        Apply the programs constraints to the potential Match List and 
            the size constraint for the matchList
        return the best possible match list under the current constraints

        Parameters
        ----------
        potentialMatchList : list of applicants
        iteration: optional, to track progress in algorithm

        Returns
        -------
        best possible list of applicants that fit the program's constraints

        """
        
        #depending on how we apply the constraints, we can end up with different lists
        #we will apply the constraints in different order (each permutation)
        # and then compare the resulting lists
        #for example, apply contraint 1, 2, 3, then apply constraint 2, 1, 3, etc
        
        
        numConstraints = len(self.program.constraints)
        
        constraintIndexer = [*range(0,numConstraints)]
        
        constraintPermutations = list(itertools.permutations(constraintIndexer))
        
        logger.debug("Building constraint permutations for program " 
                     + self.program.id 
                     + " and current applicant list: " 
                     + ApplicantController.PrintApplicantList(potentialMatchList))
        
        listOfMatchLists = [] #list of list of tuples (match list, bumped applicant)

        for eachConstPermutation in constraintPermutations:
            tempMatchList = copy.copy(potentialMatchList)
            
            logger.debug("Evaluating constraints with the following order: " 
                          + str(eachConstPermutation) + 
                          " for current list: " + ApplicantController.PrintApplicantList(potentialMatchList))
            
            for eachConstraintIndex in eachConstPermutation:
                myConstraint = self.program.constraints[eachConstraintIndex]
                
                #Enforce Constraint returns a list 
                tempMatchList = myConstraint.EnforceConstraint(tempMatchList)
                
                logger.debug("Enforced constraint: " + str(eachConstraintIndex)
                              + " with result: " + ApplicantController.PrintApplicantList(tempMatchList))
                
                tempMatchList = self.EnforceSize(tempMatchList,iteration)
                
                logger.debug("Enforcing size limit: " + str(self.program.maxSlots)
                              + " with result: " + ApplicantController.PrintApplicantList(tempMatchList))
            
                logger.debug("Adding potential Match List after applying constraints: " 
                          + "constraint " + str(eachConstPermutation)
                          + " with result " + ApplicantController.PrintApplicantList(tempMatchList))
            
                listOfMatchLists.append(tempMatchList)
            
        bestList = self.compareLists(listOfMatchLists)
        
        # this is confusing but let's revisit what we are doing
        # we have taken a potential list of applicants and applied the constraints
        # in every permutation to come up with a set of lists
        # at this point each list satisfies the constraints
        # now, we need to select the "best" list from the set of lists
        
        return bestList
        

    def compareLists(self, setOfLists):
        """
        Compares of set of lists to find the "best" list
        - so far, we are favoring the programs, that is we are selecting the 
        list that for the program, selects the highest rank

        Parameters
        ----------
        setOfLists : list of tuples (applicants, bumpedApplicant).

        Returns
        -------
        tuple (best list and bumped applicant)

        """
        bestList = None
        for eachList in setOfLists:
            if bestList == None:
                bestList = eachList
            else:
                if self.compareTwoLists(bestList, eachList) == 2:
                    bestList = eachList
        return bestList

    def bumpApplicants(self, bumpedList, iteration=-1, bumper= ""):
        """
        this sets the applicants match to -1 for all in bumpedlist
        this does not do anything to my programs list

        Parameters
        ----------
        bumpedList : the list of applicants to bump
        iteration : optional, to track iteration of algorithm
        bumper : the applicant causing the bump, can be the one who is being bumped

        Returns
        -------
        None.

        """
        logger.debug("Bumping the following applicants: ")

        for eachApplicant in bumpedList:
            eachApplicant.BumpApplicant(self.program, iteration, bumper)
            self.program.RecordBumpApplicant(eachApplicant, iteration, bumper)
            logger.debug("Applicant bumped: " + eachApplicant.PrintApplicantShort() 
                         + " program: " + str(self.program.id))


    def findMissingApplicants(self, applicantList):
        """
        compares the match list with the applicant list to find who is missing 
        from the applicant list 
        
        """
        
        missingApplicants = []

        for eachApplicant in self.program.matchList:
            if applicantList.count(eachApplicant) <= 0:
                missingApplicants.append(eachApplicant)

        return missingApplicants

    def createPotentialListsWithConstraints(self, applicant, potentialList):
        """
        #creates n unique lists based on the program's constraints, applicant and current matchlist

        Parameters
        ----------
        applicant : Applicant
        potentialList: the current match list that includes applicant

        Returns
        -------
        returnLists : a list of lists

        """

        potentialMatchList = []
        for eachApplicant in self.program.matchList:
            potentialMatchList.append(eachApplicant)
        potentialMatchList.append(applicant)        

        if len(potentialMatchList) > self.program.maxSlots:
            nsize = self.program.maxSlots
        else:
            listCombinations = []
            for i in range(1, nsize+1):
                nsize = len(potentialMatchList)
    
                listCombinations.extend(list(itertools.combinations(potentialMatchList, i)))

        returnLists = []
        for eachList in listCombinations:
            if eachList.count(applicant) > 0:
                returnLists.append(eachList)
        return returnLists


    def compareTwoLists(self, matchList1, matchList2):
        """
        Compares two lists as related to the program's rank list

        Parameters
        ----------
        matchList1 : list of applicants
        matchList2 : list of applicants

        Returns
        -------
        int
            0 if equal, 1 if matchList1 better, or 2 if matchlist2 better

        """

        list1Ranks = self.program.ListToRanks(matchList1)
        list2Ranks = self.program.ListToRanks(matchList2)

        if list1Ranks == list2Ranks:
            return 0

        length = min(len(list1Ranks), len(list2Ranks))
        for i in range(0, length):
            if list1Ranks[i] < list2Ranks[i]:
                return 1

        if len(list1Ranks) > len(list2Ranks):
            return 1

        return 2


    def EnforceSize(self, potentialList, iteration=-1, bumper=""):
        """
        from the potentiallist, enforce the overall slot size from the program

        Parameters
        ----------
        potentialList : list of applicants
        iteration: optional, if you are tracking the algorithms iteration
        bumper: optional, the applicant who is causing the bump

        Returns
        -------
        potentialList : a new set of applicants with any applicants removed
        """
        #pdb.set_trace()
        while len(potentialList) > self.program.maxSlots:
            bumpedApplicant = self.FindLowestRankedApplicantInList(potentialList)
            potentialList.remove(bumpedApplicant)
            # bumpedApplicant.BumpApplicant()
            
            bumpedApplicant.BumpApplicant(self.program, iteration, bumper)
            self.program.RecordBumpApplicant(bumpedApplicant, iteration, bumper)
            
            logger.debug("Applicant " + bumpedApplicant.name 
                         + " was removed from " + self.program.name
                         + " due to size constraints")
        return potentialList


    def FindLowestRankedApplicantInList(self, potapplicantList):
        tempRankList = [] #collection of rank spots

        for eachApplicant in potapplicantList:
            tempRankList.append(self.program.GetApplicantRank(eachApplicant))

        #will sort descending, so lowest ranked applicant is first
        #pdb.set_trace()
        tempRankList.sort(reverse=True)
        return self.program.GetApplicantByRank(tempRankList[0])

