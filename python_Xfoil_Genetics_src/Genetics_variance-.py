
import random
from math import *
from Gen2Airfoil import *
from xfoil_dat import *
import sys
import os

# remove all files from last run
filelist = [ f for f in os.listdir(".") if f.endswith(".dat") ]
for f in filelist:
    os.remove(f)
#    print f   
filelist = [ f for f in os.listdir(".") if f.endswith(".log") ]
for f in filelist:
    os.remove(f)


# Airfoil is defined by
#  LEU = Leading edge up            LED = Leading edge down      
#  C25 = Camber at 25%              T25 = Camber at 25%
#  C50 = Camber at 50%              T50 = Camber at 50%
#  C75 = Camber at 75%              T75 = Camber at 75%


#              LEU   LED     C25   C50    C75      T25   T50   T75
#genmaxs = [    0.2,  0.2,    0.2,  0.2,   0.2,     0.2,  0.2,  0.1   ]
#genmaxs = [    0.1,  0.05,   0.2,  0.2,   0.2,     0.2,  0.2,  0.1   ]
genmaxs =  [    0.1,  0.1,   0.1,  0.1,   0.1,     0.1,  0.1,  0.1   ]

genmins = [    0.01,  0.01,  0.0,  0.0,   0.0,     0.01,  0.01,  0.01   ]


ngen= len (genmaxs)

foilnum = 0

# ==============================================
# ============== BASIC FUNCTIONS ===============
# ==============================================

def newborn(gen):
    global foilnum
    foilnum+=1
    return [0,gen,'%06d' %foilnum]

def check_range(gen):
    for i in range(0,ngen):
        if(gen[i]>genmaxs[i]):
            gen[i]=genmaxs[i]
        if(gen[i]<genmins[i]):
            gen[i]=genmins[i]

def proximity(gen1,gen2):
    proximity = 0
    for i in range(0,ngen):
        d = (gen1[i] - gen2[i])/(0.00001+abs(gen1[i] + gen2[i]))
        proximity+= d*d
    return sqrt(proximity)

def breed_random():
    print  "            breed_random "
    child = [0]*ngen
    for i in range(0,ngen):
        child[i] = random.uniform(genmins[i],genmaxs[i])
        check_range(child)
    return newborn(child)

def breed_interpolate(mother,father,weight):
    print  "            breed_interpolate"
    child = [0]*ngen
    for i in range(0,ngen):
        child[i] = (1-weight)*mother[i] + weight*father[i]
    return newborn(child)

def breed_crossover(mother,father):
    print  "            breed_crossover"
    child = [0]*ngen
    for i in range(0,ngen):
        if(random.random()>0.5):
            child[i] = mother[i]
        else:
            child[i] = father[i]
    return newborn(child)

def breed_mutate(mother, scale):
    print  "            breed_mutate"
    child = [0]*ngen
    for i in range(0,ngen):
        child[i] = mother[i] * (1 + random.uniform(-scale,scale) )
        check_range(child)
    return newborn(child)

def gen2log(gen,logfile):
    #logfile.write(" %3.2f          " %gen[0])
    logfile.write (gen[2])
    logfile.write (' {0:10.2f}       '.format(gen[0]))
    #for i in range(0,ngen):
    #    logfile.write(" %1.4f " %gen[1][i])
    #logfile.write("\n")
    logfile.write("[   %1.4f" %gen[1][0])
    for i in range(1,ngen):
        logfile.write(", %1.4f" %gen[1][i])
    logfile.write('   ]\n')
    
    
#              LEU   LED     C25   C50    C75      T25   T50   C75
testgen = [    0.5,  0.1,    0.1,  0.1,   0.3,     0.5,  0.6,  0.7   ]

#print testgen
#check_range(testgen)
#print
#print testgen
#print breed_random()



# ==============================================
# ============== Algorithm ===============
# ==============================================

nsubjects = 15
nbest     = 10
name = "testfoil"

niterations = 30
Re = 40000
Ncrit = 9.0

logfile = open("logfile.log","w")

population = [[0,[],""] for i in range(0,nsubjects)]
print len(population)
breedprob = [0]*9   # breeding probabilities

def populate():
    for i in range (0,nsubjects):
        #foilnum++
        population[i] = breed_random()
        #name = '%06d' %foilnum
        gen2airfoil(population[i][1],population[i][2]) # generate Airfoil shape by Bezier interpolation
        Xfoil(population[i][2],Ncrit,Re)                   # compute fittness in Xfoil
        population[i][0] = getLDmax(population[i][2])      # set fittness = LD
        print population[i][2],population[i][2],population[i][0]
        gen2log(population[i],logfile)

def eval_fitness():
    for i in range (0,nsubjects):
        if (population[i][0] == 0):
            # evaluate fittens just for new ones
            #print population[i][2],population[i][0]
            #print population[i][1]
            gen2airfoil(population[i][1],population[i][2]) # generate Airfoil shape by Bezier interpolation
            Xfoil(population[i][2],Ncrit,Re)                   # compute fittness in Xfoil
            population[i][0] = getLDmax(population[i][2])      # set fittness = LD
            print population[i][2],population[i][0]
            gen2log(population[i],logfile)


def set_breedprob():
    global breedprob
    suma=0
   # breedprob[0] = 1.0 # modify 1
   # breedprob[1] = 1.0 # modify any
   # breedprob[2] = 1.0 # generate new
   # breedprob[3] = 1.0 # crossover 1 and 2
   # breedprob[4] = 1.0 # crossover 1 and X
   # breedprob[5] = 1.0 # crossover X and Y
   # breedprob[6] = 1.0 # interpolate 1 and 2
   # breedprob[7] = 1.0 # interpolate 1 and X
   # breedprob[8] = 1.0 # interpolate X and Y
    breedprob[0] = 1.0 # modify 1
    breedprob[1] = 0.1 # modify any
    breedprob[2] = 0.1 # generate new
    breedprob[3] = 0.1 # crossover 1 and 2
    breedprob[4] = 1.0 # crossover 1 and X
    breedprob[5] = 0.1 # crossover X and Y
    breedprob[6] = 0.1 # interpolate 1 and 2
    breedprob[7] = 0.1 # interpolate 1 and X
    breedprob[8] = 1.0 # interpolate X and Y
   
    for i in range (0,len(breedprob)):
        suma+=breedprob[i]
        breedprob[i] = suma
    for i in range (0,len(breedprob)):
        breedprob[i]/=suma
    for i in range (0,len(breedprob)):
        print breedprob[i]

def choose_breeding():
    randnum = random.random()
    child = []
    if  (( randnum >            0)&( randnum < breedprob[0])):
        child = breed_mutate(population[0][1],0.2)                          # modify 1 best      
    elif(( randnum > breedprob[0])&( randnum < breedprob[1])):       
        child = breed_mutate(population[random.randint(2,nbest-1)][1],0.1)  # modify any
    elif(( randnum > breedprob[1])&( randnum < breedprob[2])):
        child = breed_random()                                              # generate new from scratch
    elif(( randnum > breedprob[2])&( randnum < breedprob[3])):
        child = breed_crossover  ( population[0][1] ,population[1][1])                         # crossover 1 and 2
    elif(( randnum > breedprob[3])&( randnum < breedprob[4])):
        child = breed_crossover  ( population[0][1] ,population[random.randint(2,nbest-1)][1]) # crossover 1 and X
    elif(( randnum > breedprob[4])&( randnum < breedprob[5])):
        a =  random.randint(0,nbest-1)                                                         # crossover X and Y
        b = a
        while (b == a):
            b = random.randint(0,nbest-1)
        child = breed_crossover  ( population[a][1] ,population[b][1])
    elif(( randnum > breedprob[5])&( randnum < breedprob[6])):
        child = breed_interpolate( population[0][1] ,population[1][1],0.5)                         # interpolate 1 and 2
    elif(( randnum > breedprob[6])&( randnum < breedprob[7])):
        child = breed_interpolate( population[0][1] ,population[random.randint(2,nbest-1)][1],0.5) # interpolate 1 and 2
    elif(( randnum > breedprob[7])&( randnum < breedprob[8])):
        a =  random.randint(0,nbest-1)                                                             # interpolate X and Y
        b = a
        while (b == a):
            b = random.randint(0,nbest-1)
        child = breed_interpolate  ( population[a][1] ,population[b][1], 0.5)
    return child
        
def evolve():
    population.sort( reverse=True)
    for i in range (0,nbest):   # write out last survived
        print " survived : ",population[i][2],"      ",population[i][0]
        if (population[i][0] == 0):
            print "            replace zero "
            population[i] = choose_breeding()
    for i in range (1,nbest):             # replace duplicate genes
        dist =  proximity(population[0][1],population[i][1])
        print "dist ",population[0][2]," ",population[i][2]," ",dist
        if (dist < 0.5 ):
            print "   => kill ! "
            population[i] = breed_random()
    for i in range (nbest,nsubjects):     # replace less fit genes
        population[i] = choose_breeding()


set_breedprob()
    
print " ===== iteration: 0"
populate()
for i in range (1,niterations):
    print " ===== iteration: ",i
    evolve()
    eval_fitness()
logfile.close()






