from wave_helper import load_wave , save_wave
from copy import deepcopy
import numpy as np
import math

INCREASEVOLUMEFACTOR = 1.2
DECREASEVOLUMEFACTOE = float(1/1.2)
INTERVAL = 125
MAXSANPLERATE = 32767
MINSAMPLERATE =-32768
FULLPAIR = 2
SAMPLERATE = 2000
MAXVOLUME  = 32767
MINVOLUME  = -32768
DOUBLE = 2
LASTITEM = -1
ZERORATE = 0
QUITENOTEVALUE = 0
ONEPARAMETE = 1
FIRSTMASSAGE = 0
FUNCTIONINDEX = 1
TWOSEQ = 2
SEQUANCEINDEX = 1
FRISTITEM = 0
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
MESSAGE_MEREGE_INTERFACE = "enter files"
MESSAGE_SAVE_INTERFACE = "insert file name"


def normal(wave_seq):
    '''
    function which normalete the values as intgers
    between [-32768 ,32767]
    '''
    ret_seq, pair = [], []
    for wave in wave_seq_gen(wave_seq):
        if len(pair) == FULLPAIR:
            ret_seq.append(pair)
            pair = []
        wave = min(MAXSANPLERATE, wave)
        wave = max(MINSAMPLERATE, wave)
        wave = int(wave)
        pair.append(wave)
    return ret_seq

def wave_seq_gen(wave_seq):
    '''
        genrate a sequence of wave without give
        importance to the his order in the tuple
    '''
    for leftwave, rightwave in wave_seq :
        yield leftwave
        yield rightwave


def acceleration(wave_data):
        '''
            return a wave sequence which has half
            length of the input sequence, and contain
            only the odd items in the orignal sequence.
        '''
        _ , wave_seq = wave_data
        ret_seq , pair = [ ] , []
        for index ,wave in enumerate(wave_seq_gen(wave_seq)) :
            # the indexes in the form  i+2, i+ 3, 4i+2, 4i+3, 8i+2, 8i+3
            # we wereusing here magic numbers in purpose, otherwise the
            # code is less understandable.
            if index % 4 >= 2 :
                if len( pair ) == FULLPAIR :
                    ret_seq.append(  pair  )
                    pair = [ ]
                pair.append(wave)
        return _ , normal(ret_seq)


def slow(wave_data):
    '''
        return a wave sequence which has double
        length of the input sequence, and each
        eaven iten is the average of two adjacented
        in the orignal sequence.
    '''
    _ , wave_seq = wave_data
    ret_seq , pair = [ ] , []
    for index , wave in enumerate(wave_seq_gen(wave_seq)) :
        if len( pair ) == FULLPAIR :
            ret_seq.append(  pair  )
            if len (ret_seq) > 0 :
                pair = [ (x + y) / 2 for x , y in zip(pair, ret_seq[LASTITEM])]
            ret_seq.append(  pair  )
            pair = [ ]
        pair.append(wave)

    return _ , normal(ret_seq)


def inversion(wave_data):
    '''
        returns a wave sequence which is the
        reversed of sequance of the given input sequence.
    '''
    _ , wave_seq = wave_data
    wave_seq_inverted = wave_seq[::LASTITEM]
    return _ , normal(wave_seq_inverted)


def dimming_filter(wave_data):
    '''
        returns a wave sequence which is the
        reversed of sequance of the given input sequence.
    '''
    def calulate_average( _list, new_item  ):
        '''
            inserting new item to the list and drop other one
            than returns the average of the list,
            this method allows us to calculte the average of tree adjacented
            waves in an allegiant way.
        '''
        _list.pop(FRISTITEM)
        _list.append( new_item )
        return sum(_list) / len(_list)

    _ , wave_seq = wave_data
    dimmed_wave_seq = list()
    prevx , prevy = wave_seq[0]
    new_seq = []

    # allegiant soulotion for the first end case,
    # the first item in the list is the average of
    # the two first elements in the list.
    # so we insert to the fist place in the list
    # the average of the first and the second elements
    # than in main loop when we do the general calculting and
    # we will get the excepted resoult without separating to
    # cases.
    prevsx = [ wave_seq[0][i] for i in range(2)]
    prevsx = [ sum(prevsx)/2 ] + prevsx
    prevsy = [wave_seq[0][i] for i in range(2)]
    prevsy = [sum(prevsy) / 2] + prevsy

    for index, pair in enumerate(wave_seq[1:]):
        dimmed_wave_seq.append([])
        for prevs , wave in zip( [ prevsx , prevsy] , pair ):
            dimmed_wave_seq[LASTITEM].append(
                calulate_average(prevs , wave))

    # the second end case, again we inserting the
    # average of the two lasts waves in the sequance.
    dimmed_wave_seq.append([])
    for prevs in [ prevsx , prevsy] :
        dimmed_wave_seq[LASTITEM].append(
            calulate_average(prevs, sum(prevs[1:])/2))

    return _, normal(dimmed_wave_seq)



def stretch_volume(wave_data, factor):
    '''
        multiplies all the itmes in the list by
        given factor.
    '''
    _ , wave_seq = wave_data
    ret_seq , pair = [ ] , []
    for wave in wave_seq_gen(wave_seq) :
        if len( pair ) == 2 :
            ret_seq.append(  pair  )
            pair = [ ]
        pair.append(wave)

    return _ , normal(ret_seq)


def increase_volume(wave_data):
    '''
        returns the a sequence which, each value is
        multiplies by 1.2
    '''
    return stretch_volume(wave_data, INCREASEVOLUMEFACTOR)


def decrease_volume(wave_data):
    '''
        returns the a sequence which, each value is
        multiplies by 1/1.2
    '''
    return stretch_volume(wave_data, DECREASEVOLUMEFACTOE)



def sample_rate_i(i, frequency):
    '''
        returns the volume relates to the time, and the
        frequency.
    '''
    if frequency == QUITENOTEVALUE:
        return ZERORATE

    sample_per_cycle = SAMPLERATE / frequency
    return int(  MAXVOLUME * math.sin( math.pi * 2 * i / sample_per_cycle ))


def composite_txt_file(filename):
    '''
        returns a wave sequance from a file input.
    '''
    def load_wave_seq(filename):
        '''
            loading the file and initialize a list of tuples.
        '''
        openfile = open(filename, 'r').read()
        notes_list = list()
        for i , note in enumerate(openfile.split()):
            if i%2 == 0:
                notes_list.append([])
            notes_list[LASTITEM].append(note)
        return notes_list

    ret = []
    for ( note_char , ticks) in load_wave_seq(filename):
        note = NOTES[note_char]
        ret += [ [sample_rate_i( i , note )] * DOUBLE
            for i in range( int(ticks) * INTERVAL) ]
    return ret

def merge(wave_seq1 , wave_seq2):
    '''
        returns the merge of two diffrent sequances.
    '''
    if len(wave_seq1) > len(wave_seq2):
        return merge( wave_seq2, wave_seq1 )
    ret = [ ]
    wave_seq1 += deepcopy(wave_seq2[len(wave_seq1):])
    for waves_tuple1 , waves_tuple2  in zip(wave_seq1 ,wave_seq2 ):
        ret.append([])
        for x , y in zip(  waves_tuple1 , waves_tuple2 ):
            ret[LASTITEM].append( (x + y) / 2  )
    return normal( ret )

# the sequance which want to edit
GLOBAL_CURRENT_SEQ = None
def getinput_and_call(_function , argslen):
    '''
        getting input from the user,
        than calling to a function,
        finaly sending the user for the 'saving menue'
    '''
    if argslen == 0:
        resoult = _function(GLOBAL_CURRENT_SEQ)
    else :
        args = [input() for _ in range(argslen)]
        resoult = _function(*args)
    menu(SAVEMENU , params=resoult)

def proxy(_function , load_wave=load_wave):
    '''
        returns a pointer for function whith a specific parameters.
        it is allows me to convert the function
        f(X , Y)  to g(Y) when i know what is X.
    '''
    def _proxy():
        global GLOBAL_CURRENT_SEQ
        if GLOBAL_CURRENT_SEQ is None:
            return getinput_and_call(
             lambda _path :
              _function( load_wave(_path)) , ONEPARAMETE)
        else :
            # the case which we allready have choose a file.
            return getinput_and_call( _function , 0)
    return _proxy


def merge_user_interface():
    '''
        the user interface which handle the merging opthion.
    '''
    print(MESSAGE_MEREGE_INTERFACE)
    wave_seqs = [load_wave(input())[SEQUANCEINDEX] for _ in range(TWOSEQ)]
    return merge( *wave_seqs  )


def save_file(resoult):
    '''
        saving wave sequance as file.
    '''
    print(MESSAGE_SAVE_INTERFACE)
    _file_name = input()
    frame_rate , wave_seq = resoult
    save_wave( frame_rate , wave_seq , _file_name)

    global GLOBAL_CURRENT_SEQ
    GLOBAL_CURRENT_SEQ = None

    menu(MAINMENU)

def not_save(resoult):
    global GLOBAL_CURRENT_SEQ
    GLOBAL_CURRENT_SEQ = resoult
    
    menu( EDITMENU )

#########################################################################
#------------------------Menus------------------------------------------#
#########################################################################
'''
    we aren`t able to enter the menus to the MAGIC NUMBERS section,
    because they are contains pointers to functions which needed to
    defined first.
'''
SAVEMENU = {
    0 : (" do you want to save the file ?" ,    None                    ),
    1 : ("yes : "  ,                            save_file               ),
    2 : ("no  : " ,                             not_save                )
}


EDITMENU = {
    0 : ("blabla" , None),
    1 : ("increase_volume : "  ,    proxy(increase_volume  )) ,
    2 : ("decrease_volume : " ,     proxy(decrease_volume  )) ,
    3 : ("accelerate " ,            proxy(acceleration     )) ,
    4 : ("slow : "  ,               proxy(slow             )) ,
    5 : ("dimming_filter : " ,      proxy(dimming_filter   )) ,
    6 : ("inversion : "      ,      proxy(inversion        ))
}


MAINMENU = {
    0 : ("choose opthion", None),
    1 : ( "change wave file" , lambda : menu(EDITMENU) ),
    2 : ( "merges wave files" , merge_user_interface ),
    3 : ( "compose wave files" , lambda : proxy( composite_txt_file )),
    4 : ( "exit" , lambda : print( "goodbye" ) )

}

def menu( _menu , params=None ):
    '''
        one function to master all menus,
        iterate over
    '''
    print (_menu[FIRSTMASSAGE][FIRSTMASSAGE])
    for opthion , ( message , _function ) in _menu.items():
        # if not opthion -> FIRSTMASSAGE - case.
        if opthion :
            print( str(opthion) + "." + message )

    if params is not None:
        _menu[int(input())][FUNCTIONINDEX](params)
    else :
        _menu[int(input())][FUNCTIONINDEX]()


if __name__ == '__main__':
    menu( MAINMENU )

    #save_wave(a, b, 'dimmed.wav')
