#!/usr/bin/env python
# coding: utf-8

# In[1]:

import numpy as np ; from scipy.io.wavfile import read ; 
from scipy.io import wavfile ; import scipy.io; 
import statistics; import wave


# # Speech Indicator

# ### Returns time stamp, query, and percentage of speaking duration (w/o first and last pause)

# In "The diagnostic utility of patient-report and speech- language pathologists’ ratings for detecting the early onset of bulbar symptoms due to ALS", pauses are defined as longer than 300 ms.
# 
# 
# Using 20-40ms as frame length for speech analysis: https://www.researchgate.net/publication/224217613_Preference_for_20-40_ms_window_duration_in_speech_analysis

# In[18]:


window_len = 30 # Unit: ms

capstone_dir = "/Users/ninismacbook/other_docs/Y4S1/capstone"


def speech(filename):
    filepath = capstone_dir + "/downsampled/" + filename

    samplerate, query = wavfile.read(filepath)
    length = query.shape[0] / samplerate
    
    abs_q = np.abs(query)
    
    # The range in which we pick the upper and lower bound for voice
    range1 = range(0, int(samplerate*0.1))
    
    time = np.linspace(0., length, query.shape[0])
    
    # Find max and min of the first second to be upper and lower bound of filter
    upper = np.max(query[range1]) ; lower = np.min(query[range1])    
    
    frame_per_window = samplerate * window_len/1000
    
    # Convert all data in the query to absolute values
    plot_q = np.abs(query)
    
    # Rolling average of the window
    for i in range(len(plot_q)):
        if i < frame_per_window/2:
            i1 = 0 ; i2 = i + int(frame_per_window/2)            
        elif i > (len(plot_q) - frame_per_window/2):
            i1 = i - frame_per_window/2 ; i2 = len(query)
        else:
            i1 = i-frame_per_window/2 ; i2 = i+frame_per_window/2
        
        plot_q[i] = np.mean(plot_q[int(i1) : int(i2)])
    
    for i in range(len(plot_q)):
        if plot_q[i] > lower and plot_q[i] < upper:
            plot_q[i] = 0
            plot_q[i] = 0
        else:
            plot_q[i] = 1
    
    # Remove the first and last pause when calculating speak rate
    new_q = plot_q.copy()
    new_q = new_q[np.where(new_q == 1)[0][0] : len(new_q)]
    last_speak = np.where(new_q == 1)[0][len(np.where(new_q == 1)[0])-1]

    # Note: plot_q is for plotting. new_q is the query whose first and last pause are eliminated
    # Use new_q to calculate speech vs non speech percentage
          
    return time, plot_q, sum(new_q)/len(new_q)*100, samplerate



# # Pause Indicator

# ### Returns time stamp, query, and percentage of pause duration (w/o first and last pause)

# In[24]:

def pause(filename):
    filepath = capstone_dir + "/downsampled/" + filename
    
    time = speech(file)[0]
    plot_q = speech(file)[1]
    plot_q = [not elem for elem in plot_q]
    samplerate = speech(file)[3]
    
    return time, plot_q, 100-speech(file)[2], samplerate

