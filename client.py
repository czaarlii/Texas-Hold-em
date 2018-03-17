import socket
import pickle
import poker
import zasady


def Main():
    host = '127.0.0.1'
    port = 5000

    mySocket = socket.socket()
    mySocket.connect((host, port))
    print(mySocket.recv(1024).decode())
    #zasady.zasadygry()

    # message = input(" -> ")

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

        # paka = Paczka()
        # mySocket.send(pickle.dumps(paka))
        # data = pickle.loads(mySocket.recv(1024))
        #
        # print('Received from server: ' + str(data.bool))
        #
        # message = input(" -> ")

    mySocket.close()


if __name__ == '__main__':
    Main()





# tLock = thr.Lock()
# dzialaj = True
#
# def odbior(nazwa, sock):
#     while dzialaj:
#         try:
#             tLock.acquire()
#             while True:
#                 dane, adres = sock.recvfrom(1024)
#                 print(str(dane))
#         except:
#             pass
#         finally:
#             tLock.release()
#
#
# host = '127.0.0.1'
# port = 0
#
# serwer = ('127.0.0.1', 4000)
# s = soc.socket(soc.AF_INET, soc.SOCK_DGRAM)
# s.bind((host, port))
#
# rT = thr.Thread(target=odbior, args=('RecvThread', s))
# rT.start()
#
# nick = input("Podaj nick: ")
# info = input(nick + '-> ')
# while info != 'koniec':
#     if info != '':
#         wiad = nick + ": " + info
#         s.sendto(wiad.encode(), serwer)
#         tLock.acquire()
#         info = input(nick + '-> ')
#         tLock.release()
#         time.sleep(0.2)
#
# dzialaj = False
# rT.join()
# s.close()
