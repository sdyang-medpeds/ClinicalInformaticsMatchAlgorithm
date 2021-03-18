# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 13:44:28 2021

@author: sdy001
"""

class ApplicantController:
    def PrintApplicantList(applicantlist):
        string = ""
        isFirst = True
        for eachApplicant in applicantlist: 
            if isFirst:
                isFirst = False
            else:
                string += ", "
            string += eachApplicant.name + ": " + str(eachApplicant.id)
        return string    