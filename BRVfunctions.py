# -*- coding: utf-8 -*-
"""BRVfunctions v1.9"""
"""Script by BaronVladziu"""

def printad(): #funkcja do wypisywania znalezionych mikrofonow
    import pyaudio
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
    return 
    
def takeSecond(elem): #funkcja pobierajaca drugi element listy
    return elem[1]
    
def get_results(responses): #funkcja do zwracania wyników
    from techmo_sarmata_pyclient.service.asr_service_pb2 import ResponseStatus
    if responses is None:
        return
    data = list();
    for response in responses:
        for n, res in enumerate(response.results):
            transcript = " ".join([word.transcript for word in res.words])
            inter = res.semantic_interpretation.split()
            if len(inter) > 0:
                if inter[0] == "Stawiam":
                    if len(inter) > 1:
                        data.append([transcript, res.confidence, res.semantic_interpretation])
                else:
                    data.append([transcript, res.confidence, res.semantic_interpretation])
    return [ResponseStatus.Name(response.status), data]

def getReply(canRaise):
    import pyaudio
    import wave
    from techmo_sarmata_pyclient.utils.wave_loader import load_wave
    from techmo_sarmata_pyclient.service.sarmata_settings import SarmataSettings
    from techmo_sarmata_pyclient.service.sarmata_recognize import SarmataRecognizer
    from address_provider import AddressProvider
    import os
    import numpy
    
    FORMAT = pyaudio.paInt16
    MAX_VALUE = 32767
    CHANNELS = 1
    RATE = 44100
    CHUNK = 2048
    WAVE_OUTPUT_FILENAME = "temp.wav"
    DISTRUST_FACTOR = 0.1
    TOO_LOUD_LIMIT = 0.99
    TOO_QUIET_LIMIT = 0.4
     
    audio = pyaudio.PyAudio()
    
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    walkingMean = 0
    time = 0
    frames = []
    print("nagrywanie...")
    
    while time < 20:
        data = stream.read(CHUNK)
        frames.append(data)
        chunkMean = numpy.average(numpy.abs(numpy.fromstring(data, dtype=numpy.int16)))
        if chunkMean < walkingMean:
            time += 1
        else:
            time = 0
        walkingMean = (walkingMean+(0.01*chunkMean))/1.01
    print("nagrywanie zakończone")
    
    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
     
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    
    #check volume of recording
    maxValue = 0
    for chunk in frames:
        for value in numpy.abs(numpy.fromstring(chunk, dtype=numpy.int16)):
            if value > maxValue:
                maxValue = value
    if maxValue < MAX_VALUE * TOO_QUIET_LIMIT:
        print("Zbyt cichy sygnał")
    elif maxValue > MAX_VALUE * TOO_LOUD_LIMIT:
        print("Zbyt głośny sygnał")
    
    #analyze
    #if __name__ == '__main__':
    ap = AddressProvider()
    wave_file = "temp.wav"
    if canRaise == True: 
        grammar_file = "grammars/grammar_canraise.abnf"
    else:
        grammar_file = "grammars/grammar_cannotraise.abnf"
    address = ap.get("sarmata")
    
    audio = load_wave(wave_file)
    
    settings = SarmataSettings()
    session_id = os.path.basename(wave_file)
    settings.set_session_id(session_id)
    settings.load_grammar(grammar_file)
    
    recognizer = SarmataRecognizer(address)
    results = recognizer.recognize(audio, settings)
    player_answer_list = get_results(results)
    
    length = len(player_answer_list[1]);
    if length == 0:
        return 'NO COMMAND DETECTED'
    sortedAnswerList = sorted(player_answer_list[1], key=takeSecond, reverse=True)
    #print(sortedAnswerList)
    if sortedAnswerList[0][1] < 2*DISTRUST_FACTOR:
        return 'NO COMMAND DETECTED'
    if length >= 2:
        if sortedAnswerList[0][1] - DISTRUST_FACTOR < sortedAnswerList[1][1]:
            return 'NO COMMAND DETECTED'
        if canRaise == True:
            words = sortedAnswerList[0][2].split()
            if words[0] == 'Stawiam':
                sum = 0
                for i in range(len(words)):
                    if i > 0:
                        sum = sum + int(words[i])
                return 'Stawiam ' + str(sum)
    return sortedAnswerList[0][2]

def getreply_canraise():
    return getReply(True)

def getreply_cannotraise():   
    return getReply(False)
