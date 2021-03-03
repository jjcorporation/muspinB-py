#%%
#%reset
import numpy as np
import pandas as pd
import warnings
from stats import MarkovRenewalProcess as MRP

class Participant_data :
    def __init__(self,  Remove_Amb=[], Nb_Remove_Amb =0,New_Amb_list =[]):#sujet_name,
        pass
        #self.name= sujet_name
    '''This is a class of participant_datas'''
    def data_Amb_call(self, path_file):
        data = pd.read_excel('C:/Users/Utilisateur/Desktop/Graph par participant/2021_02_22_95/XLSX_Amb/Ok/' + path_file)
        data = data.to_records(index=False)
        data = list(data)
        return data 
    def data_nAmb_call(self, path_file):
        data = pd.read_excel('C:/Users/Utilisateur/Desktop/Graph par participant/2021_02_22_95/XLSX_nAmb/Ok/' + path_file)
        data = data .to_records(index=False)
        data = list(data)
        return data
    def remove_one_or_solo(self, list_considérée, type_stim):# Warning : may remove a lot for nAmb condition, plus besoin avec new initialisation
        touch_press = [x[0] for x in list_considérée]
        Number_touch_press = [[x,touch_press.count(x)] for x in set(touch_press)]
        Remove =[]
        Nb_Remove = 0 # Ronald question
        for x in range (len (Number_touch_press)):
            if Number_touch_press[x][1] == 1 :
                Nb_Remove = Nb_Remove + 1
                Remove.extend([Number_touch_press[x][0]])
        New_list = [list_considérée[i] for i in range (len(list_considérée)) if list_considérée[i][0] not in Remove]
        if type_stim == 'Amb':
            self.Remove_Amb = Remove
            self.Nb_Remove_Amb = Nb_Remove
            self.New_Amb_list = New_list
            return self.Remove_Amb, self.Nb_Remove_Amb, self.New_Amb_list
        elif type_stim =='nAmb':
            self.Remove_nAmb = Remove
            self.Nb_Remove_nAmb = Nb_Remove
            self.New_nAmb_list = New_list
            return self.Remove_nAmb, self.Nb_Remove_nAmb, self.New_nAmb_list
        else:
            warnings.warn("Warning : Is it an Amb or nAmb list that is injected into the loop ? Please Specify type 'Amb' or 'nAmb' in type_stim ")
import os
import pandas as pd
path = ('C:/Users/Utilisateur/Desktop/Graph par participant/2021_02_22_95/XLSX_Amb/Ok')

#%%
for roots, dirs, files in os.walk(path):
    xlsfiles = [ _ for _ in files if _.endswith('.xlsx')]

All_participants_steady_states_Amb = pd.DataFrame()
for sujet in xlsfiles:
    Participant_name = 'P_'+ sujet[0:4]
    Participant = Participant_data()# Chose the participant, Ronald Help, c'est galère d'instancier un nom différent pour chaque objets
    # Create List
    Participant.Amb_list = Participant.data_Amb_call(sujet)
    Participant.nAmb_list = Participant.data_nAmb_call(sujet)
    #Participant.remove_one_or_solo(Participant.Amb_list,'Amb')
    # #Participant.remove_one_or_solo(Participant.nAmb_list,'nAmb')
    
    # Markov renewal process Amb
    moyenne_temps_séjours_a_priori =3
    écart_type_temps_séjours_a_priori = 1
    
    states = set([x[0] for x in Participant.Amb_list])
    k = len(states)
    tm= np.zeros((k,k))
    tm.flat[::k+1] = 1 #force donnée, soit disant observé 3 échantillons (moyenne_temps_séjours_a_priori), si observe 20 autre, moins de force, m
    Participant.mrp_Amb = MRP(states, tm= tm, mu = np.full((k, ), moyenne_temps_séjours_a_priori),  sigma = np.full((k,), écart_type_temps_séjours_a_priori))
    Participant.mrp_Amb.train([(s[0], s[2]) for s in Participant.Amb_list])#if not s[0]== 'Left_coh'])
    Participant.mrp_Amb.steady_state
    for k, v in Participant.mrp_Amb.survival_times.items():
        print('{}: params s={}, mean={}'.format(k, v.kwds['s'], v.mean()))# v.stats(moments='m')
        print(np.log(v.kwds['s']))
    
    Participant.mrp_Amb.transition_matrix
    names = list(Participant.mrp_Amb.states)#
    Participant.mrp_Amb.transition_matrix_noms = pd.DataFrame(Participant.mrp_Amb.transition_matrix, index=names, columns=names)
    name_csv = Participant_name +'.mrp_Amb.transition_matrix_noms.csv'
    Participant.mrp_Amb.transition_matrix_noms.to_csv(name_csv, index=True, header=True, sep=' ')
    Participant.mrp_Amb.transition_matrix_noms

    Participant.mrp_Amb.steady_state_noms = pd.DataFrame([Participant.mrp_Amb.steady_state], columns=names, index = [Participant_name])
    All_participants_steady_states_Amb = All_participants_steady_states_Amb.append(Participant.mrp_Amb.steady_state_noms)
#%%

'''#Ronald question
#Participant.mrp_Amb.sample# Donne une réalisation typique pour le processus. Aléa deveient causes, états. observables, action changer de percepts.

#Markov renewal process nAmb
Participant.mrp_nAmb = MRP(set([Participant.New_nAmb_list[i][0] for i in range (len(Participant.New_nAmb_list))]))
Participant.mrp_nAmb.train([(s[0], s[2]) for s in New_nAmb_list])#if not s[0]== 'Left_coh'])
Participant.mrp_nAmb.steady_state

for k, v in Participant.mrp_nAmb.survival_times.items():
            print('{}: params s={}, mean={}'.format(k, v.kwds['s'], v.mean()))# v.stats(moments='m')
            print(np.log(v.kwds['s']))

Participant.mrp_nAmb.transition_matrix'''
