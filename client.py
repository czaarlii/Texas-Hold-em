import socket
import pickle
import poker
import zasady
import warnings

warnings.simplefilter("ignore")

def Main():
    host = '127.0.0.1'
    port = 5000

    mySocket = socket.socket()
    mySocket.connect((host, port))
    print(mySocket.recv(1024).decode())
    #zasady.zasadygry()

    paczka = poker.PaczkaDoKlienta()
    while True:

        paczka = pickle.loads(mySocket.recv(1024))

        if not paczka:
            break

        print(paczka.akcja_info)
        print(paczka.stol_info)

        if paczka.wymagana_odp:

            # wczytanie akcji gracza, więcej w poker.py
            odp = poker.wczytaj_poprawna_odp(paczka.min_stawka,
                                             paczka.maks_stawka,
                                             paczka.liczba_podbic)

            mySocket.send(pickle.dumps(poker.PaczkaDoSerwera(odp)))

    mySocket.close()


if __name__ == '__main__':
    Main()
