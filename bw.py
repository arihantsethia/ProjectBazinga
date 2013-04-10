# This file is part of the BotWarsServer program.
# Copyright (C) 2013 Rahul Huilgol, Rajat Khanduja
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# This file defines functions required to compile and run the code and 
# evaluate the output
# Currently supports only the following langauges
#  - C
#  - C++
#  - Python
#
# TODO : Take care of naming when multiple users might be accessing.

#Edited (Shreyas)
#How to use:
#import and write the following to get output
#(output, error) = compilerun(submission_id, code, test_case_input, language, memlimit, time)
#output will contain output of program
#error will contain errors if any
#language: 'c', 'py', 'cpp'.
#memlimit in bytes
#
#example
#(out, err) = compilerun(1, "#include<stdio.h>\nint main(){printf(\"hello\");return 0;}", "testcase", "c", 20000000, 20000)
#print out
#print err

import subprocess
import logging
import os, sys, time

PROBLEMS_DIR = "Problems"
TEST_DIR = "Problems"

class NoSuchProblemException(Exception):
  def __init__ (self, value):
    self.value = value

  def __str__ (self):
    return repr(self.value)

class CompilationError (Exception):
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return repr(self.value)



def judge(problemRef, sourceFile):
  '''
  This function takes as input the reference number of the problem
  and the submitted file and calls the compile-run function 
  appropriately. Eventually, it returns the score earned by the 
  submitted solution based on the problemRef and the evaluation
  function given in the file problems/problemRef.py
  '''

  # First ensure that the problem reference is a valid one.
  importFile = PROBLEMS_DIR + "." + str(problemRef)
  try:
    prob = __import__(importFile, fromlist = [problemRef])
  except Exception as e:
    logging.debug(str(e))
    raise NoSuchProblemException("Problem " + str(problemRef) + " not defined")
    return
  

  # Initial setup
  prob.setup(sourceFile, os.path.realpath(PROBLEMS_DIR))

  score = 0
  allErrors = ""
  # For each input, output pair run the test.
  # TODO : This step calls the compilation of files over and over. Fix this.
  try:
    for (inFile,outFile) in prob.testFiles:
      inFile  = os.path.join(PROBLEMS_DIR, inFile)
      outFile = os.path.join(PROBLEMS_DIR, outFile)
      (producedOutput, error) = compilerun(sourceFile, inFile, prob.MEM_LIM,
                                           prob.TIME_LIM)
      inputData = open(inFile).read()
      expectedOutput = open(outFile).read()
      if not error:
        score += prob.evaluate (inputData, expectedOutput, producedOutput, 
                                sourceFile)
      else:
        allErrors += error + "\n"
  except CompilationError as e:
    logging.debug ("CompilationError:" + str(e))
    allErrors += str(e)
    pass
  except Exception as e:
    logging.info (str(e))
    raise e 
    
  return score, allErrors


def init():
  '''
  Initializations required for judging steps.
  '''
  compilec = ['/usr/bin/gcc', 'runner.c', '-o', 'runner','-lm']
  subprocess.call(compilec)

#def compilerun(filename, inputfile, memlimit, timelimit):
def compilerun(sid, code, testCase, language, memlimit, timelimit):

  filename = PROBLEMS_DIR + '/' + str(sid) + '_code.c'
  inputfile = PROBLEMS_DIR + '/' + str(sid) + '_input'

  with open(filename, "w") as codeFile:
    codeFile.write(code)

  with open(inputfile, "w") as inFile:
    inFile.write(testCase)

  TEST_DIR    = os.path.dirname(filename)
  outFiles    = {'c'  : filename + ".out",
                 'cpp': filename + '.out'}
  compiler    = {'c'  : ['/usr/bin/gcc', '-lm', '-w', '-o', outFiles['c']],
                 'cpp': ['/usr/bin/g++', '-lm', '-w', '-o', outFiles['cpp']]}
  interpreter = {'py' : '/usr/bin/python'}              
    # Convert all parameters to string
  filename   = str(filename)
  inputfile  = str(inputfile)
  memlimit   = str(memlimit)
  timelimit  = str(timelimit)
  logging.debug("%s; %s; %s; %s", filename, inputfile, memlimit, timelimit)
  
  # Find language of the program
  #dotpos = filename.find(".")
  #language = filename[dotpos + 1:]
  logging.debug("Language of file %s is '%s'", filename, language)

  compileerror = False
  
  # Create and open output and error files
  t = str(int(time.time()))
  errfile    = os.path.join(TEST_DIR, os.path.basename(inputfile) + "_err_" + t)
  outputfile = os.path.join(TEST_DIR, os.path.basename(inputfile) + "_out_" + t)
  ferr = open(errfile,'w')
  fout = open(outputfile, 'w') # Ensures that the file is created
  fout.close()  # Close it as only creation of file is required
  logging.debug("Created output file : %s ; Created error file : %s", errfile, outputfile)
  error  = ""
  output = ""
  # Check if it is a compiled language
  if language in compiler:
    compiler[language].append(filename)
    subprocess.call(compiler[language], stderr = ferr)
    with open(errfile) as error_file:
      error = error_file.read()
    if not error:
      logging.debug("Compiled %s successfully", filename)
      run =  ['./runner', outFiles[language], '--input=' + inputfile, 
              '--output=' + outputfile, '--mem=' + memlimit, 
              '--time=' + timelimit, '--chroot=.']
      subprocess.call(run, stderr = ferr)
    else:
      logging.debug("Error when compiling %s", filename)
      compileerror = True
      raise CompilationError(error)
  elif language in interpreter:
    run = ['./runner', interpreter[language], filename, '--input=' + inputfile, 
           '--output=' + outputfile, '--mem=' + memlimit, 
           '--time=' + timelimit, '--chroot=.']
    subprocess.call(run, stderr = ferr)
    with open(errfile, 'r') as error_file:
      error = error_file.read()
    if error:
      compileerror = True       
      
  ferr.close()
  with open(errfile, 'r') as error_file:
    if compileerror == False:
      error = error_file.read()
    else:
      error = 'CERR  ' + error_file.read()
#        print error
  with open(outputfile, 'r') as output_file:
    output = output_file.read()
#   print output
  
    # TODO : Delete error and output files
  return (output, error)

if __name__ == '__main__':
  #init()
  (out, err) = compilerun(1, "#include<stdio.h>\nint main(){printf(\"hello\");return 0;}", "testcase", "c", 20000000, 20000)
  print out
  print err
  if out == "hello":
    print 'congrats'
