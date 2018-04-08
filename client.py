import socket
import pickle
import poker
import zasady
import warnings
from threading import Thread
import pyaudio

warnings.simplefilter("ignore")

KONIEC = False


class CzatKlient(Thread):
    def __init__(self, host, port):
        Thread.__init__(self)
        self.host = host
        self.port = port

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        print(">>Polaczono z czatem serwera.")

        p = pyaudio.PyAudio()
        CHUNK = 512
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 20000

        # for sending data
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        # for receiving data
        stream2 = p.open(format=FORMAT,
                         channels=CHANNELS,
                         rate=RATE,
                         output=True,
                         frames_per_buffer=CHUNK)

        data2 = 'a'
        while data2 != '':
            if KONIEC:
                break

            try:  # sending data
                data = stream.read(CHUNK)
                s.sendall(data)
            except KeyboardInterrupt:
                break
            except:
                pass

            try:  # receiving data
                data2 = s.recv(1024)
                if not data2:
                    break
                stream2.write(data2)
            except KeyboardInterrupt:
                break
            except:
                pass

        stream.stop_stream()
        stream.close()
        p.terminate()
        s.close()

        print(">>Zakonczono czat glosowy.")


class GraKlient(Thread):
    def __init__(self, host, port):
        Thread.__init__(self)
        self.host = host
        self.port = port

    def run(self):
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.connect((self.host, self.port))

        print(mySocket.recv(1024).decode())
        # zasady.zasadygry()
        # mySocket.send(''.encode())

        while True:
            paczka = mySocket.recv(1024)
            if not paczka:
                break
            paczka = pickle.loads(paczka)

            print(paczka.akcja_info)
            print(paczka.stol_info)

            if paczka.wymagana_odp:
                # wczytanie akcji gracza, więcej w poker.py
                odp = poker.wczytaj_poprawna_odp(paczka.min_stawka,
                                                 paczka.maks_stawka,
                                                 paczka.liczba_podbic)

                mySocket.send(pickle.dumps(poker.PaczkaDoSerwera(odp)))

        mySocket.close()
        global KONIEC
        KONIEC = True
        print('>>Zakonczono polaczenie gry.')


def Main():
    host = input('>>Podaj IP serwera (0 aby wybrac domyslne): ')
    if str(host) == '0':
        host = "127.0.0.1"
    port = 5000

    watekC = CzatKlient(host, port)
    watekG = GraKlient(host, port)

    watekC.start()
    watekG.start()

    watekC.join()
    watekG.join()


if __name__ == '__main__':
    Main()
