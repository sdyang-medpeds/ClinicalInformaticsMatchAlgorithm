# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 08:52:35 

Different ways to view the Match data

@author: sdy001
"""
import csv


class MatchViewer:
    
    def __init__(self, myMatchController=""):
        """
        """
        self.myMatchController = myMatchController
        
    def WriteResults(self, file):
        
        csv_columns = ['name', 'id', 'match']
        with open(file, 'w', newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in self.myMatchController.AggregateResults():
                writer.writerow(data)        
                
    def WriteTrace(self, debugFolder, prefix):
        """
        Writes the applicant and program trace for debugging purposes
        
        prefix is the prefix filename
        
        debugFolder is where the files will go
        """
        
        applicantTrace = self.myMatchController.PrintApplicantTrace()
        self.listToFile(applicantTrace,debugFolder + "//" + prefix + "_trace_applicants.txt" )
        
        programTrace = self.myMatchController.PrintProgramTrace()
        self.listToFile(programTrace,debugFolder + "//" + prefix + "_trace_programs.txt" )
               
        
    def listToFile(self, myList, filename):
        with open(filename, 'w') as filehandle:
            for listitem in myList:
                filehandle.write('%s\n' % listitem)        
        
        
    def dictToFile(self, myDictionaryList, headers, csvfilename):
        """
        Simple support function print a dictionary with headers into a CSV
        """       
        with open(csvfilename, "w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(myDictionaryList)
            
    def DebugToExcel(self, debugFolder, prefix):
        """
        This is for debugging purposes
        Prints out the programs, constraints and applicants.
        
        prefix is the file prefix
        """
        self.ApplicantsToExcel(debugFolder + "//" + prefix + "_debug_applicants.csv" )
        self.ProgramsToExcel(debugFolder + "//" + prefix + "_debug_programs.csv" )
        self.ConstraintsToExcel(debugFolder + "//" + prefix + "_debug_constraints.csv" )


    def ApplicantsToExcel(self, csvfilename):
        """
        applicantDict is a dictionary of applicants
        
        prints the applicants to the filename
    
        Returns
        -------
        None.
    
        """
        
        headers = ["Applicant ID", "Name", "Rank", "Program ID", "Program Name"]
    
        printableList = []
        for eachApplicant in self.myMatchController.applicants:
            i = 1
            for eachProg in self.myMatchController.applicants[eachApplicant].rankList:
                myApplicant = {}
                myApplicant["Applicant ID"] = eachApplicant
                myApplicant["Name"] = self.myMatchController.applicants[eachApplicant].name
                
                myApplicant["Rank"] = i
                myApplicant["Program ID"] = eachProg.id
                myApplicant["Program Name"] = eachProg.name
                printableList.append(myApplicant)
                i += 1
                
        self.dictToFile(printableList, headers, csvfilename)            
        
    def ProgramsToExcel(self, csvfilename):
        headers = ["Program ID", "Program Name", "Slots", "Rank", "Applicant ID", "Name"]
        
        printableList = []
        for eachProgram in self.myMatchController.programs:
            i = 1
            for eachApplicant in eachProgram.rankList:
                myApplicant = {}
                myApplicant["Applicant ID"] = eachApplicant.id
                myApplicant["Name"] = eachApplicant.name
                
                myApplicant["Rank"] = i
                myApplicant["Program ID"] = eachProgram.id
                myApplicant["Program Name"] = eachProgram.name
                myApplicant["Slots"] = eachProgram.maxSlots
                printableList.append(myApplicant)
                i += 1    
                
        self.dictToFile(printableList, headers, csvfilename)        

    def ConstraintsToExcel(self, csvfilename):
        headers = ["Program ID", "Program Name", "Constraint ID", "Constraint Slots", "Applicant ID", "Applicant Name"]
        
        printableList = []
        for eachProgram in self.myMatchController.programs:
            for eachCon in eachProgram.constraints:
                
                for eachApplicant in eachCon.applicantList:
                    myApplicant = {}
                    myApplicant["Applicant ID"] = eachApplicant.id
                    myApplicant["Applicant Name"] = eachApplicant.name
                    
                    myApplicant["Constraint ID"] = eachCon.id
                    myApplicant["Constraint Slots"] = eachCon.numSlots
                    
                    myApplicant["Program ID"] = eachProgram.id
                    myApplicant["Program Name"] = eachProgram.name
                    printableList.append(myApplicant)   
                
        self.dictToFile(printableList, headers, csvfilename)