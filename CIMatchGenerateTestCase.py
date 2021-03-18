# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 14:26:47 2020

@author: sdy001

Generates test cases.  
Programs and Applicants must be specified prior
This will generate rank lists for programs and applicants

You can then go and add extra criteria manually
- automation is to be done for criteria

"""
import csv
from CIMatchClasses import *
from CIMatchController import *


testCaseFolder = "testCases-4-1"

#Load in the Applicants and Programs
input_file = csv.DictReader(open(testCaseFolder + "//" + "testDataApplicants.csv"))

applicants = dict()
programs = list()
   
print("reading in applicants and programs") 
for row in input_file:
    if row["ï»¿ID"] in applicants:
        print("Warning: applicant ID " + row["ï»¿ID"] + " used multiple times")
    applicants[row["ï»¿ID"]] = Applicant(row["Name"], row["ï»¿ID"])

input_file = csv.DictReader(open(testCaseFolder + "//" + "testDataPrograms.csv"))
for row in input_file:
    programs.append(Program(row["Name"], row["ï»¿ID"], int(row["MaxSlots"])))

import random
import itertools
import pdb
def generateApplicantRankList(applicant, programList):
    #apply up to 10 programs
    for i in range(0,random.randint(1, 10)):
        prog = programs[random.randint(0,len(programs)-1)]
        applicant.AddToRankList(prog)
    return applicant

def findApplicantsForProgram(program, applicantDict):
    applicantList = []
    for eachApplicant in applicantDict.values():
        if eachApplicant.rankList.count(program) > 0:
            applicantList.append(eachApplicant)
    return applicantList

def generateProgramRankList(program, applicantList):
    #applicantList is a list of applicants that have applied ot the program
    maxRanked = min(len(applicantList)-1, program.maxSlots*3 )

    progRanklist = []
    for i in range(0, maxRanked):
        selector = random.randint(0,len(applicantList)-1)
        if progRanklist.count(applicantList[selector]) <= 0:
            progRanklist.append(applicantList[selector])

    print("generated a rank list of size " + str( len(progRanklist)) +
          " for " + program.name )
    program.rankList = progRanklist
    

print("generating test data")

for eachApplicant in applicants.values():
    eachApplicant = generateApplicantRankList(eachApplicant, programs)
    
for eachProgram in programs:
    applist = findApplicantsForProgram(eachProgram, applicants)
    generateProgramRankList(eachProgram, applist)
    

print("printing test data")
myFile = open(testCaseFolder + "//" + "testDataApplicantList.csv"
                             , "w+", newline="")
outputFile = csv.writer(myFile)
outputFile.writerow(["Applicant ID", "Program ID", "Rank"])

for eachApplicant in applicants.values():
    i = 1
    for eachProg in eachApplicant.rankList:
        outputFile.writerow([eachApplicant.id, eachProg.id, i])
        i += 1
myFile.close()

myFile = open(testCaseFolder + "//" + "testDataProgramList.csv"
                             , "w+", newline="")
outputFile = csv.writer(myFile)
outputFile.writerow(["Program ID", "Applicant ID", "Rank"])

for eachProgram in programs:
    i = 1
    for eachApp in eachProgram.rankList:
        outputFile.writerow([eachProgram.id, eachApp.id, i])
        i += 1
myFile.close()