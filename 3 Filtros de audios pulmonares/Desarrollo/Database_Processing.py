# -*- coding: utf-8 -*-
"""
Created on Sun May 31 20:56:30 2020

@author: SANTIAGO
"""

import os
import csv
import pandas as pd
import numpy as np
import librosa

from Features import features
from Processor import process

#%% Interest Files

# Filtered files by .wav and .txt
dataset = os.listdir('audio_and_txt_files')
list_txt = [i for i in dataset if 'wav' not in i]
list_wav = [j for j in dataset if 'txt' not in j]

# txt file (Demographic Information)
header = ['patient_ID','Diagnosis']
df1 = pd.read_csv("patient_diagnosis.csv", delimiter=',',names = header)

header = ['patient_ID','age','sex','IMC','weight','height']
df2 = pd.read_csv("demographic_info.txt", delimiter=' ',names = header)

patients_df = pd.merge(df1, df2, on='patient_ID') # df for analysis
df = patients_df # df for append auscultation features

del(dataset, df1, df2)
#%%
dataFrames = []
for i in range(len(list_txt)):
    
    # Create of a temporal dataset with the anotation 
    # contents. On it, features of each auscultation cycle
    # will be added. 
    
    # txt files processing (Anotations)
    path = list_txt[i]
    file = open('audio_and_txt_files/'+path, 'rt',encoding='utf-8')
    content = csv.reader(file, delimiter = '\t')
    
    auscultation = []
    header = ['start','end','crackles','wheezes']
    
    for row in content:
        dictionary = dict(zip(header, row))
        
        adq_format = {'adq_format':path[4:22]}
        dictionary['start'] = float(dictionary['start'])
        dictionary['end'] = float(dictionary['end'])
        dictionary['crackles'] = int(dictionary['crackles'])
        dictionary['wheezes'] = int(dictionary['wheezes'])
        
        if (dictionary['crackles'] == 0) and (dictionary['wheezes'] == 0):
            state = {'state':0}
        elif (dictionary['crackles'] == 1) and (dictionary['wheezes'] == 0):
            state = {'state':1}
        elif (dictionary['crackles'] == 0) and (dictionary['wheezes'] == 1):
            state = {'state':2}
        elif (dictionary['crackles'] == 1) and (dictionary['wheezes'] == 1):
            state = {'state':3}
            
        adq_format.update(dictionary)
        adq_format.update(state)
        auscultation.append(adq_format)
        
    # wav files processing (Aucultation Audios)
    path = list_wav[i]
    original_signal, sr = librosa.load('audio_and_txt_files/'+path, 4000)
    time, filtered_signal = process(original_signal, sr)
    
    for j in range(len(auscultation)):
        start = auscultation[j]['start']
        end = auscultation[j]['end']
        chunk = filtered_signal[(time >= start) & (time <= end)]
        dictionary = features(chunk) # Calculate Time & Freq Domain Statistics
        auscultation[j].update(dictionary)
        
    auscultation = pd.DataFrame(auscultation)
     
    # Identify patient ID (path[:3]) and add it to the df to concatenate it later
    patient_id = pd.Series(int(path[:3])*np.ones(len(auscultation)),name='patient_ID')
    auscultation = pd.concat([patient_id,auscultation],axis=1)
    dataFrames.append(pd.merge(df, auscultation, on='patient_ID')) 

#%% This routine generate an union of each aucultation cycle from every patient
for i in range(len(dataFrames)):
    if i == 0:
        df = dataFrames[0]
    else:
        df = df.append(dataFrames[i])

del(dataFrames)
df = df.set_index(['patient_ID'])
patients_df = patients_df.set_index(['patient_ID'])

#%% Finally the collected data is exported to an excel table
df.to_excel(r'auscultation_features.xlsx', index = True)
patients_df.to_excel(r'patients_diagnosis.xlsx', index = True)

