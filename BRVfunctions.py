# -*- coding: utf-8 -*-
"""Script by BaronVladziu"""

#funkcja do wypisywania znalezionych mikrofonow
def printad():
    import pyaudio
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
    return 

#funkcja pobierajaca drugi element listy
def takeSecond(elem):
    return elem[1]

#funkcja do zwracania wyników
def get_results(responses):
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

#funkcja do nagrywania i analizy pliku audio
def getreply_canraise():
    import pyaudio
    import wave
    from techmo_sarmata_pyclient.utils.wave_loader import load_wave
    from techmo_sarmata_pyclient.service.sarmata_settings import SarmataSettings
    from techmo_sarmata_pyclient.service.sarmata_recognize import SarmataRecognizer
    from address_provider import AddressProvider
    import os
    import numpy
    
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    WAVE_OUTPUT_FILENAME = "temp.wav"
     
    audio = pyaudio.PyAudio()
     
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    mn = 0
    frames = []
    print("nagrywanie...")

    i = 0
    while i < 20:
        data = stream.read(CHUNK)
        frames.append(data)
        mn2 = numpy.average(numpy.abs(numpy.fromstring(data, dtype=numpy.int16)))
        if mn2 < mn:
            i += 1
        else:
            i = 0
        mn = (mn+(0.01*mn2))/1.01
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
    
    
    #analyze
    #if __name__ == '__main__':
    ap = AddressProvider()
    wave_file = "temp.wav"
    grammar_file = "grammars/grammar_canraise.abnf"
    address = ap.get("sarmata")
    
    audio = load_wave(wave_file)
    
    settings = SarmataSettings()
    session_id = os.path.basename(wave_file)
    settings.set_session_id(session_id)
    settings.load_grammar(grammar_file)
    
    recognizer = SarmataRecognizer(address)
    results = recognizer.recognize(audio, settings)
    
    player_answer_list = get_results(results)
    if len(player_answer_list[1]) == 0:
        return 'NO COMMAND DETECTED'
    elif sorted(player_answer_list[1], key=takeSecond, reverse=True)[0][1] < 0.2:
        return 'NO COMMAND DETECTED'
    words = sorted(player_answer_list[1], key=takeSecond, reverse=True)[0][2].split()
    if words[0] == 'Stawiam':
        sum = 0
        for i in range(len(words)):
            if i > 0:
                sum = sum + int(words[i])
        return 'Stawiam ' + str(sum)
    return sorted(player_answer_list[1], key=takeSecond, reverse=True)[0][2]

def getreply_cannotraise():
    import pyaudio
    import wave
    from techmo_sarmata_pyclient.utils.wave_loader import load_wave
    from techmo_sarmata_pyclient.service.sarmata_settings import SarmataSettings
    from techmo_sarmata_pyclient.service.sarmata_recognize import SarmataRecognizer
    from address_provider import AddressProvider
    import os
    import numpy
    
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 2048
    WAVE_OUTPUT_FILENAME = "temp.wav"
     
    audio = pyaudio.PyAudio()
     
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    mn = 0
    frames = []
    print("nagrywanie...")

    i = 0
    while i < 20:
        data = stream.read(CHUNK)
        frames.append(data)
        mn2 = numpy.average(numpy.abs(numpy.fromstring(data, dtype=numpy.int16)))
        if mn2 < mn:
            i += 1
        else:
            i = 0
        mn = (mn+(0.01*mn2))/1.01
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
    
    
    #analyze
    #if __name__ == '__main__':
    ap = AddressProvider()
    wave_file = "temp.wav"
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
    if len(player_answer_list[1]) == 0:
        return 'NO COMMAND DETECTED'
    elif sorted(player_answer_list[1], key=takeSecond, reverse=True)[0][1] < 0.2:
        return 'NO COMMAND DETECTED'
    return sorted(player_answer_list[1], key=takeSecond, reverse=True)[0][2]
