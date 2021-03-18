# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 10:41:44 2021

ApplicantMatchAttempt - contains an instance of an attempted match


@author: Samuel Yang
"""

import copy
from ApplicantController import *

class ApplicantMatchAttempt:
    
    def __init__(self, applicant="", program="", iteration="", result="", msg="", bumper = ""):
        """
        Used to document an attempted match between an applicant or program

        Parameters
        ----------
        applicant : Applicant, optional
            This is the applicant object. The default is "".
        program : Program, optional
            This is the program object. The default is "".
        iteration : int, optional
            This is the iteration that the overall algorithm is in. The default is "".
        result : Boolean, optional
            True if match, False otherwise. The default is "".
        msg : string, optional
            Msg related to attempt
        bumper : Applicant, optional
            The applicant who is causing the bump

        Returns
        -------
        None.

        """
        self.applicant = applicant
        self.program = program
        if program != "":
            self.matchListSnapshot = copy.copy(program.matchList)
        self.iteration = iteration
        self.result = result 
        self.msg = msg
        self.bumper = bumper
        
    def PrintAttemptForApplicant(self):
        returnstr = ""
        
        if self.program != "":
            returnstr += self.program.PrintProgShort()
        returnstr += ", on iteration: " + str(self.iteration) + " "
        returnstr += ", with message: " + str(self.msg)
        returnstr += ", with result: " + str(self.result)        
        if self.program != "":
            returnstr += ", match list at the time was: " 
            if len(self.matchListSnapshot) > 0:
                returnstr += ApplicantController.PrintApplicantList(self.matchListSnapshot)
            else:
                returnstr += "N/A"
        if self.bumper != "":
            returnstr += ", bumper is: " + self.bumper.PrintApplicantShort()
        return returnstr
    
    def PrintAttemptForProgram(self):
        returnstr = ""
        
        returnstr += self.applicant.PrintApplicantShort()
        returnstr += ", on iteration: " + str(self.iteration) + " "
        returnstr += ", with message: " + str(self.msg)
        returnstr += ", with result: " + str(self.result)        
        if self.program != "":
            returnstr += ", match list at the time was: " 
            if len(self.matchListSnapshot) > 0:
                returnstr += ApplicantController.PrintApplicantList(self.matchListSnapshot)
            else:
                returnstr += "N/A"
        return returnstr
        
