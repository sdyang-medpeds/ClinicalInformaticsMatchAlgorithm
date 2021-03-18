# ClinicalInformaticsMatchAlgorithm
Implements the Match Algorithm for the Clinical Informatics Fellowship program.  Loosely based on the NRMP match, it allows for programs to implement additional "constraints" based on resources.  For example, a program may have funding for 4 total spots, but 1 spot is reserved for a pediatrician, thus the program cannot accept more than one pediatrician.

To data is defined in a folder.  

There is a list of applicants and a list of programs.  Each applicant has an ordered list of programs that he/she is willing to accept a match to.  Similarly, each program has an ordered list that of applicants.  In addition, each program has a size limit and, optionally, may have additional constraints as described above.  See testCases-1-1 for example.  

The program is run via MatchRunner.py.  Supporting code is found in the Code directory.  

In general the program reads in the applicant, program, and constraint data. It then loops through each applicant to find a match.  The loop continues until the list of unmatched applicants remains unchanged.

Output is in the resultsFolder specific in MatchRunner.  It is a CSV file - each row is an applicant with the associated program.  If no program is listed, the applicant did not match.

The "Test" directories also have an "expected results" file.  This is intended to be used in testing.  MatchRunner can be setup to loop through the directories to test different scenarios as development continues to verify that testing is accurate.  testCase-5-1 is a large scale test with around 50 programs and 100 applicants.

Note - there is a known issue with the logger, where the logging is not correctly written to the log file specified in MatchRunner.  Logging messages are written to console for review.  Debugging information can also be seen using the DebugToExcel and WriteTrace functions in MatchViewer.  These functions write to the debugFolder.  DebugToExcel re-writes the input data to confirm that the objects you have are correctly linked.  WriteTrace writes two files, one for applicants and one for programs.  In WriteTrace, there is a record of an applicant as it goes through the algorithm.  Similar record is printed in the programs file.
