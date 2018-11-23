from wave_helper import load_wave , save_wave
import numpy as np

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
        return _ , ret_seq

def slow(wave_data):
    _ , wave_seq = wave_data
    ret_seq , pair = [ ] , []
    for index ,wave in enumerate(wave_seq_gen(wave_seq)) :
        if len( pair ) == 2 :
            if index % 4 == 3 :
                
            ret_seq.append(  pair  )
            pair = [ ]
        pair.append(wave)
    return _ , ret_seq

def inversion(wave_data):
    pass

def dimming_filter(wave_data):
    pass

def stretch_volume(wave_data, factor):
    _ , wave_seq = wave_data
    ret_seq , pair = [ ] , []
    for wave in wave_seq_gen(wave_seq) :
        if len( pair ) == 2 :
            ret_seq.append(  pair  )
            pair = [ ]
        wave *= factor
        wave  = min(32767 , wave)
        wave  = max(-32768 , wave)
        wave  = int(wave)
        pair.append(wave)

    return _ , ret_seq


def increase_volume(wave_data):
    return stretch_volume(wave_data, 1.2)

def decrease_volume(wave_data):
    return stretch_volume(wave_data, 1/1.2)

if __name__ == '__main__':
    D = load_wave( "./wav Samples/batman_theme_x.wav")
    #print(list(D))
    print(D[1][0])
    D = increase_volume(D)
    print(D[1][0])
