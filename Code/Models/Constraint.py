# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 11:18:24 2021

@author: sdy001
"""
import logging

classLogger = logging.getLogger("match.class")

from ApplicantController import *

class Constraint:
    """ 
    A contstraint is a list of applicants from which a program can only take a certain subset of size numSlots
    """
    def __init__(self, id, program, numSlots):
        self.id = id
        self.program = program
        self.numSlots = numSlots
        self.applicantList = []
        
    def strConstraint(self):
       string = "Constraint " + str(self.id) + ", can take "
       string += str(self.numSlots) + " from " 
       string += ApplicantController.PrintApplicantList(self.applicantList)
       return string

    def EnforceConstraint(self, potapplicantList):
        """
            enforces the constraint, i.e. someone from the applicant list may be bumped
            
            returns the new list with constraint enforced and the bumpedApplicant
        """
        
        classLogger.debug("Enforcing constraint " + self.strConstraint() 
                          + " on " 
                          + ApplicantController.PrintApplicantList(potapplicantList) + 
                          " from program " + str(self.program.id))
        
        count = 0
        constraintApplicantList = []
        for eachApplicant in potapplicantList:
            if self.applicantList.count(eachApplicant) > 0:
                constraintApplicantList.append(eachApplicant)
                count += 1

        bumpedApplicant = None
        if count > self.numSlots:
            
            classLogger.debug("Constraint " + str(self.id) + " triggered with " + 
                              ApplicantController.PrintApplicantList(constraintApplicantList) + 
                              " - someone will be bumped")
            
            classLogger.debug("Program " + str(self.program.id) + " rank list: "
                              + ApplicantController.PrintApplicantList(self.program.rankList))
            
            bumpedApplicant = self.program.FindLowestRankedApplicantInList(constraintApplicantList)
            potapplicantList.remove(bumpedApplicant)
            classLogger.debug("Applicant " + bumpedApplicant.name + 
                              " was removed from this list " 
                              + self.program.name)            
            
        return potapplicantList


    def IsApplicantInConstraint(self, applicant):
        """
            is this applicant listed in a constraint?
        """
        if self.applicantList.count(applicant) > 0:
            return True
        return False
