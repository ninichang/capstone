from dtw import * ;  import numpy as np ; from scipy.io.wavfile import read ; import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean ;  from fastdtw import fastdtw ;  import sounddevice as sd
from os.path import dirname, join as pjoin ;  from scipy.io import wavfile ; import scipy.io; import os
import glob ; import webrtcvad;import statistics;from dtwalign import dtw as dtwalign ;import contextlib ; 
import collections ; import contextlib;import sys; import wave

# vad = webrtcvad.Vad()

capstone_dir = "/Users/ninismacbook/other_docs/Y4S1/capstone" ; blocksize = 18000

def make_samples(file1, seg1_1, seg1_2, file2, seg2_1, seg2_2):
    
    file1_path = capstone_dir + "/downsampled/" + file1 ; file2_path = capstone_dir + "/downsampled/" + file2

    samplerate, query = wavfile.read(file1_path) ; samplerate, ref = wavfile.read(file2_path)

    query_sample = query[int(samplerate*seg1_1): int(samplerate*seg1_2)]
    ref_sample = ref[int(samplerate*seg2_1): int(samplerate*seg2_2)]
    
    return query_sample, ref_sample, samplerate

def play_samples(query_sample, ref_sample, samplerate):
    sd.play(query_sample, samplerate = samplerate, blocksize=blocksize, blocking=True)
    sd.play(ref_sample, samplerate = samplerate, blocksize=blocksize, blocking=True);



def get_word_xy(file, time, seg1_1, seg1_2):
    
    file_path = capstone_dir + "/downsampled/" + file
    
    samplerate, query = wavfile.read(file_path)
    query_sample = query[int(samplerate*seg1_1): int(samplerate*seg1_2)]    

    coord = (time - seg1_1)/(seg1_2 - seg1_1) * len(query_sample)
    return coord


def plot_word(alignment, file1, time1, seg1_1, seg1_2, file2, time2, seg2_1, seg2_2):
    plt.figure(figsize=(20, 10)) ; file1_path = capstone_dir + "/downsampled/" + file1
    
    samplerate, query = wavfile.read(file1_path) ; query_sample = query[int(samplerate*seg1_1): int(samplerate*seg1_2)]    
        
    plt.plot(alignment.index1, alignment.index2)
    plt.axvline(x = get_word_xy(file1, time1, seg1_1, seg1_2), color = 'r')
    plt.hlines(y = get_word_xy(file2, time2, seg2_1, seg2_2), xmin = 0, xmax = len(query_sample), color = 'r')    




def plot_alignment(file1, seg1_1, seg1_2, file2, seg2_1, seg2_2, alignment):
    alignment.plot(type="threeway"); 
    print('DTW distance: ', alignment.distance)
    stretch_output = stretch(file1, seg1_1, seg1_2, file2, seg2_1, seg2_2, alignment)
    print('Stretching for speech: ', stretch_output[0])
    print('Stretching for pause: ', stretch_output[1])  
    print('Stretching for not aligned portion: ', stretch_output[2])          


def alignment_err(path, file1, file2, seg1_1, seg1_2, seg2_1, seg2_2, time1_lst, time2_lst, xlabel, ylabel):
    colors = ['red', 'g', 'b', 'm', 'brown', '#d89743', 'grey', 'c', 'orange', 'g', 'b', 'm', 'red']
    err = 0
    for i in range(len(time1_lst)):
        x_axis = get_word_xy(file1, time1_lst[i], seg1_1, seg1_2)
        y_axis = get_word_xy(file2, time2_lst[i], seg2_1, seg2_2)
        plt.axvline(x_axis, color = colors[i])
        plt.hlines(y_axis, 0, x_axis+6000, color = colors[i])
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        warp_x = np.where(path[0] == round(x_axis))[0][0]
        warp_y = np.where(path[1] == round(y_axis))[0][0]
        e = np.abs(warp_x - x_axis) + np.abs(warp_y - y_axis)
#         print(warp_x, x_axis)
#         print(warp_y, y_axis)
#         print(e)
        err = err + e
    print('Avg err: ' + str(err/len(time1_lst)))