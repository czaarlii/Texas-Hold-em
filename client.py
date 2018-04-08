import socket
import pickle
import poker
import zasady
import warnings

warnings.simplefilter("ignore")


def Main():
    host = input('>>Podaj IP serwera (0 aby wybrac domyslne): ')
    if str(host) == '0':
        host = "127.0.0.1"
    port = 5000

    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.connect((host, port))
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
    print('>>Zakonczono polaczenie.')


if __name__ == '__main__':
    Main()
