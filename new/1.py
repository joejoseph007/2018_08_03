
import subprocess as sp
#import os
import shutil
import sys
import string
import csv, random, re, sys, os, math, numpy, time, subprocess, shutil,thread
import matplotlib.pyplot as plt 
from multiprocessing import Pool
from distutils.dir_util import copy_tree

'''
def run(I):
	#ps = sp.Popen(['xfoil <controlfile.xfoil >outputfile.out'],stdin=sp.PIPE,stdout=None,stderr=None)

	ps = sp.Popen(['xfoil'],stdin=sp.PIPE,stdout=None,stderr=None)

	res = ps.communicate(string.join(["NACA 0012","pacc","Naca0012%i.dat"%I,"oper","Visc","130000","Aseq -1 10 0.5","\n","QUIT"],'\n') )
	#print string.join(["NACA 0012","oper","Visc","130000","Aseq -1 10 0.5","Hard"],'\n')
	#print res
	


y = Pool()
result = y.map(run,range(5))
y.close()
y.join()    
'''

subprocess.call(['xfoil <controlfile.xfoil >outputfile.out'])
