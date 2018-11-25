from wave_helper import load_wave , save_wave
from copy import deepcopy
import numpy as np
import math


def normal(wave_seq):
    ret_seq, pair = [], []
    for wave in wave_seq_gen(wave_seq):
        if len(pair) == 2:
            ret_seq.append(pair)
            pair = []
        wave = min(32767, wave)
        wave = max(-32768, wave)
        wave = int(wave)
        pair.append(wave)
    return ret_seq

def wave_seq_gen(wave_seq):
    for leftwave, rightwave in wave_seq :
        yield leftwave
        yield rightwave


def acceleration(wave_data):
        _ , wave_seq = wave_data
        ret_seq , pair = [ ] , []
        for index ,wave in enumerate(wave_seq_gen(wave_seq)) :
            if index % 4 >= 2 :
                if len( pair ) == 2 :
                    ret_seq.append(  pair  )
                    pair = [ ]
                pair.append(wave)
        return _ , normal(ret_seq)


def slow(wave_data):
    _ , wave_seq = wave_data
    ret_seq , pair = [ ] , []
    for index , wave in enumerate(wave_seq_gen(wave_seq)) :
        if len( pair ) == 2 :
            if index % 4 == 3 :
                ret_seq.append(  pair  )
            pair = [ ]
        pair.append(wave)
    return _ , normal(ret_seq)


def inversion(wave_data):
    _ , wave_seq = wave_data
    wave_seq_inverted = wave_seq[::-1]
    return _ , normal(wave_seq_inverted)


def dimming_filter(wave_data):


    def calulate_average( _list, new_item  ):
        _list.pop(0)
        _list.append( new_item )
        return sum(_list) / len(_list)

    _ , wave_seq = wave_data
    dimmed_wave_seq = list()
    prevx , prevy = wave_seq[0]
    new_seq = []

    prevsx = [ wave_seq[0][i] for i in range(2)]
    prevsx = [ sum(prevsx)/2 ] + prevsx
    prevsy = [wave_seq[0][i] for i in range(2)]
    prevsy = [sum(prevsy) / 2] + prevsy

    for index, pair in enumerate(wave_seq[1:]):
        dimmed_wave_seq.append([])
        for prevs , wave in zip( [ prevsx , prevsy] , pair ):
            dimmed_wave_seq[-1].append(
                calulate_average(prevs , wave))

    dimmed_wave_seq.append([])
    for prevs in [ prevsx , prevsy] :
        dimmed_wave_seq[-1].append(
            calulate_average(prevs, sum(prevs[1:])/2))

    return _, normal(dimmed_wave_seq)



def stretch_volume(wave_data, factor):
    _ , wave_seq = wave_data
    ret_seq , pair = [ ] , []
    for wave in wave_seq_gen(wave_seq) :
        if len( pair ) == 2 :
            ret_seq.append(  pair  )
            pair = [ ]
        pair.append(wave)

    return _ , normal(ret_seq)


def increase_volume(wave_data):
    return stretch_volume(wave_data, 1.2)


def decrease_volume(wave_data):
    return stretch_volume(wave_data, 1/1.2)

SAMPLERATE = 2000
MAXVOLUME  = 32767
MINVOLUME  = -32768

NOTES = {

    'A' : 440,
    'B' : 494,
    'C' : 523,
    'D' : 587,
    'E' : 659,
    'F' : 698,
    'G' : 784,
    'Q' : 0
}


def sample_rate_i(i, frequency):
    if frequency == 0:
        return  0

    sample_per_cycle = SAMPLERATE / frequency
    return int(  MAXVOLUME * math.sin( math.pi * 2 * i / sample_per_cycle ))


def composite_txt_file(filename):

    def load_wave_seq(filename):
        openfile = open(filename, 'r').read()
        notes_list = list()
        for i , note in enumerate(openfile.split()):
            if i%2 == 0:
                notes_list.append([])
            notes_list[-1].append(note)
        return notes_list

    for ( note_char , ticks) in load_wave_seq(filename):
        note = NOTES[note_char]
        return [ [sample_rate_i( i , note )] * 2
        for i in range( int(ticks) * 125) ]

def merge(wave_seq1 , wave_seq2):
    if len(wave_seq1) > len(wave_seq2):
        return merge( wave_seq2, wave_seq1 )
    ret = [ ]
    wave_seq1 += deepcopy(wave_seq2[len(wave_seq1):])
    for waves_tuple1 , waves_tuple2  in zip(wave_seq1 ,wave_seq2 ):
        ret.append([])
        for x , y in zip(  waves_tuple1 , waves_tuple2 ):
            ret[-1].append( (x + y) / 2  )
    return normal( ret )


if __name__ == '__main__':
    D = load_wave( "./wav Samples/batman_theme_x.wav")
    #print(list(D))
    print(D[1][0])
    D = increase_volume(D)
    print(D[1][0])

    D = [ 0 , [ [ i ,  i ] for i in range(10)] ]
    a, b = dimming_filter(D)
    print(b)

    a = composite_txt_file('tt1.txt')
    b = composite_txt_file('tt2.txt')
    print( merge(a , b ))


    #save_wave(a, b, 'dimmed.wav')
