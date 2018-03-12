import BRVfunctions
import gra
import warnings
import zasady

warnings.simplefilter("ignore")

BRVfunctions.printad()
zasady.zasadygry()

def main():
    print("Gra Texas Hold'em Poker sterowany głosowo dla 2 graczy. Zapraszamy do gry!")

    texas_holdem = gra.Gra()
    texas_holdem.uruchom()


if __name__ == "__main__":
    main()
