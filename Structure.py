''' Librairies'''
#from stims import circle, fix_point, plaid
from __future__ import absolute_import, division, print_function
from builtins import range
from random import random
from psychopy import data
from constants import trialTypes # ['Amb_nKp', 'Amb_Kp', 'nAmb_nKp', 'nAmb_Kp']

from psychopy.hardware import keyboard
from psychopy import core


""" Create a list of the 4 possibles trials (random position in the list) : ['Amb_nKp', 'Amb_Kp', 'nAmb_nKp', 'nAmb_Kp']
"""
trials = data.TrialHandler(trialTypes, 1, method='random') # correspond à 1 Block

""" Create 1 Block with the four differents trials for Learning phase"""
Block_Learn = trials.trialList

""" Create several Blocks (each with the four differents trials) for testing phase"""
Blocks_Test = []
NumberOfBlock = 14 # number of blocks
i = 0
for i in range (NumberOfBlock)  :
    trials = data.TrialHandler(trialTypes, 1, method='random')
    Block = trials.trialList
    Blocks_Test.append(Block)

""" Create 1 block of four 'Amp_Kp' trials for Estimation Parameters Phase"""
Block_Estimation = ['Amb_Kp', 'Amb_Kp', 'Amb_Kp', 'Amb_Kp']

""" First Block Learn , then block Estimation, then block test'''
''' Block learn : at the end of each trial of nAmb_KP, feedback (good/wrong answer)"""
from utils import*
create_experiment_structure( nBlocks = 3)




"""
Je reprends ici car boucles dans boucles, et je vais plutot faire avec les matrix
Donc ici pas fini, tourne pas
Save ID Bloc + trial + datas
+

Idée : créer np numpy de listes nommée Result qui reprend, pour chaque essai :
[Numéro du bloc, numéro de l'essai, type d'essai (Amb_KP, nAMb_KP, Amb_nKP ou nAmb_nKP) ],
Dans le cas de nAmb_Kp, la liste de Result sera : 
[Numéro du bloc, numéro de l'essai, type d'essai (Amb_KP, nAMb_KP, Amb_nKP ou nAmb_nKP), Réponse attendue (left, right ou up), Réponse donnée, Temps pour donner cette réponse( t0 = changement de percept controlé car nAMb)]
 
 In the case of nAmb_Kp, create couples of the 3 possibles visuals (transpL, transpR, coh) with their good answer associated
"""
#targets_responses = [{'Type': plaid[transpL], 'Correct_response': 'left'},{'Type': plaid[transpR], 'Correct_response': 'right'}, {'Type': plaid[coh], 'Correct_response': 'up'}]
#see https://www.marsja.se/trialhandler-a-psychopy-tutorial/ tutorial 


#Idée : créer np numpy de listes nommée Result qui reprend, pour chaque essai :
#[Numéro du bloc, numéro de l'essai, type d'essai (Amb_KP, nAMb_KP, Amb_nKP ou nAmb_nKP), Réponse attendue (left, right ou up), Réponse donnée, Temps pour donner cette réponse( t0 = changement de percept controlé car nAMb)]
# [float, float, float(Amb_KP:1, nAMb_KP:2, Amb_nKP:3 ou nAmb_nKP:4), float(right: 1, up:2 ou left:4), float(right: 1, up:2 ou left:4), Float]
# We have 14 * 4 = 56 trials, we have 6 columns. So we have 56*6=336 values
Nb_trials_tot = 56
Nb_columns = 6
Values = 336
import numpy as np 
array = np.arange(Values).reshape(Nb_trials_tot,Nb_columns)
np.zeros_like(array)

keycode = {'right': 1, 'up': 2, 'left':4}
dt = np.dtype({'col1': ('U10', 0), 'col2': (np.float32, 10),'col3': (int, 14)})

from plaids import keys
Result =[]
count_Bloc = 0
count_Trial = 0
for bloc in Blocks_Test :
    #list(enumerate (Blocks_Test))
    #for idx, val in list(enumerate(bloc)):
    count_Bloc = count_Bloc+1
    Bloc_ID = 'Bloc {}'.format(count_Bloc)
    print('Bloc {}'.format(count_Bloc))
    for trial in bloc :
        count_Trial = count_Trial+1
        Trial_ID = 'Trial {}'.format(count_Trial)
        print('Trial {}'.format(count_Trial ))
        if trials == 'nAmb_Kp':
            nAmbTypes = [transpL, transpR, coh]
            for target in nAmbTypes:
                for thisKey in keys :
                    if target == transpL :
                        if thisKey =='left': 
                            print('correct_response left')
                        else :
                            print ('incorrect_response')
                    if target == transpR :
                        if thisKey =='right': 
                            print('correct_response Right')
                        else :
                            print ('incorrect_response')
                    if target == coh :
                        if thisKey =='up':
                            print('correct_response left')
                        else :
                            print ('incorrect_response')
Result = Result.append(Bloc_ID)
    
    
            
            

#key_resp.keys #a python list of keys pressed
#key_resp.rt #the time to the first key press
#key_resp.corr #None, 0 or 1, if you are using 'store correct'



#New list containing a dictionary for each trial. Each dictionairy (i.e., trial) contain the keys ‘Target’ and ‘CorrectResponse’. This is were we store each Target and its correct response.
#targets_responses = []

#for target in visual_targets:
#    if target == Amb_KP:
#        correct_response = Resp_Amb_KP
#    elif target == Amb_nKP:
#        correct_response = Resp_Amb_nKP
#    elif target == nAmb_KP:
#        correct_response = Resp_nAmb_KP
#    else:
#        correct_response = Resp_nAmb_nKP
#    targets_responses.append({'Target':target, 'CorrectResponse':correct_response})



#We also want to record what the subjects responded, if a correct response (Accuracy) was given
#trials.data.addDataType('Response')
#trials.data.addDataType('Accuracy')


# Amb
#[{'Amb', 
# nAmb 
#{'transpL'}, {'transpR'}, {'coh'}
#stimList = [{'Type': plaid[Amb], 'KP': on}, {'Type':plaid[nAmb], 'KP': on}, {'Type':plaid[Amb], 'KP': off}, {'Type':plaid[nAmb], 'KP': off}]

'''
# run to test (à retirer du code final)
nDone = 0
for thisTrial in trials:  # handler can act like a for loop
    print(thisTrial)
    nDone += 1
    '''

    '''kb = keyboard.Keyboard()
keycode = {'right': 1, 'up': 2, 'left':4}
nAmbTypes = [transpL, transpR, coh]
kb.clock.reset()  # when you want to start the timer from
keys = kb.getKeys(['right', 'left', 'up', 'esc'], waitRelease=True)
if 'esc' in keys:
    core.quit()
for key in keys:
    print(key.name, key.rt, key.duration)'''
