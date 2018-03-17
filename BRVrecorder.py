#Script by BaronVladziu

import BRVfunctions

imie= input('Podaj swoje imię: ')
mikrofon=input('Podaj swoj mikrofon: ')
#Test funkcji BRVfunctions.getreply_canraise() - wszystko
print("\nNa ekranie pojawią się komendy, co masz mówić. Zastosuj się do nich, proszę :)")
commands = list()
commands.append("CZEKAM")
commands.append("PASS")
commands.append("VA BANQUE")
commands.append("DOKLADAM")
commands.append("WYCOFUJE SIE")
commands.append("STAWIAM 10")
commands.append("STAWIAM 20")
commands.append("STAWIAM 30")
commands.append("STAWIAM 40")
commands.append("STAWIAM 50")
commands.append("STAWIAM 60")
commands.append("STAWIAM 70")
commands.append("STAWIAM 80")
commands.append("STAWIAM 90")
commands.append("STAWIAM 100")
commands.append("STAWIAM 200")
commands.append("STAWIAM 300")
commands.append("STAWIAM 400")
commands.append("STAWIAM 500")
commands.append("STAWIAM 600")
commands.append("STAWIAM 700")
commands.append("STAWIAM 800")
commands.append("STAWIAM 900")
commands.append("STAWIAM 1000")

for cmd in commands:
    for i in range(1, 4):
        print("\nPowiedz " + cmd)
        BRVfunctions.record(imie + "-" + mikrofon + "-" + cmd + "-" + str(i) + ".wav", False)
