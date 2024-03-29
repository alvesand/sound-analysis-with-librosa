"""
Created on Sun Mar 22 16:30:38 2020

@author: Anderson Alves

# A short example on how importing several audio files into a data frame 
"""
import os
import librosa
import pandas as pd
import numpy as np

directory = 'C:\\Users\\eu\\Documents\\estudar\\Python\\Audio Classification\\audio_dataset\\raw_data'
audiodata = []
files = []

sr = 20000
for filename in os.listdir(directory):
    if filename.endswith(".wav"):
        files.append (filename)
        path = (f'C:\\Users\\eu\\Documents\\Python\\Audio Classification\\audio_dataset\\raw_data\\{filename[0:len(filename)]}')
        y , sr = librosa.load(path, sr = sr, duration = 4)
        y_harmonic, y_percussive = librosa.effects.hpss(y)        
        audiodata.append (y_percussive)


audiodf = pd.DataFrame(audiodata)
audiodf.head
audiodf.shape
n = len(audiodf)

  
"""The next lines will create a data.frame with several features 
for all imported audio files"""

descri_dat = []
for k in range(0,n):
    vec = np.array([0.0]*12)
    y = np.array(audiodf.iloc[k,0:], dtype=np.float32)    
    # 1 signal minimum
    mi = min(y)
    vec[0] = mi
    # 2 signal maximum
    ma = max(y)
    vec[1] = ma       
    # 3 RMS
    rms = librosa.feature.rms(y)
    vec[2] = np.mean(rms)    
    # 4 Zero crossing rates
    zc = librosa.zero_crossings(y, pad=False)
    zc = sum(zc)/80000
    vec[3] = zc
    # 5 Tempo
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    vec[4] = tempo    
    # 6 Mean Onset strenght
    onset_env = librosa.onset.onset_strength(y=y, sr=sr, aggregate=np.median)
    n_ons = len(librosa.onset.onset_detect(y=y, sr=sr, onset_envelope = onset_env))       
    vec[5] = np.mean(onset_env)    
    # 7 Average spectral centroid
    sc = librosa.feature.spectral_centroid(y, sr=sr)[0]
    msc = np.mean(sc)
    vec[6] = msc
    # 8 Mean Spectral contrast
    spec_cont = librosa.feature.spectral_contrast(y, sr=sr)
    vec[7] = np.mean(spec_cont)
    # 9 Mean spectral bandwidth
    spec_band = librosa.feature.spectral_bandwidth(y+0.01, sr=sr)[0]
    spec_band = sum(spec_band)/len(spec_band)
    vec[8] = spec_band
    # 10 Max spectral roll-off
    srof = librosa.feature.spectral_rolloff(y+0.01, sr=sr,  roll_percent=0.85)[0]
    ma_srof =  np.max(srof)
    vec[9] = ma_srof
    # 11 Min spectral roll-off
    srof = librosa.feature.spectral_rolloff(y+0.01, sr=sr,  roll_percent=0.15 )[0]
    mi_srof =  np.mean(np.ma.masked_equal(srof,0))
    vec[10] = mi_srof        
    #12 Mel frequency
    mfccs = librosa.feature.mfcc(y, sr)    
    aver_mfccs = float(sum(mfccs[0])/len(mfccs[0]))
    vec[11] = aver_mfccs
    descri_dat.append(vec)
    
dat = pd.DataFrame(descri_dat)
dat.shape
dat.head

dat['filenames'] = files 

label = ['none']*len(files)

for i in range(0,len(files)):
    strin = str(files[i])
    if strin.find('bat') == 0:
        label[i] = 'batida'
    else:
        label[i] = 'picada'

dat['label'] = label

dat.columns = ['min_sig',
               'max_sig',
               'rms',
               'zcr',
               'tempo', 
               'num_ons',       
               'aver_sc',
               'spec_cont',
               'spec_band',               
               'max_roll',
               'min_roll',
               'mfc1',
               'filename',
               'label']

os.chdir('C:\\Users\\eu\\Documents\\estudar\\Python\\Audio Classification')            
dat.to_csv('audio_descri.txt', sep='\t', index=False)   