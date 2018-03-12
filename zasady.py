
def zasadygry():
    print("\n****ZASADY GRY****\n")
    print("Celem gry jest ułożenie z kart znajdujących się na stole i w ręce gracza układów punktowych, wyższych niż przeciwnika.")
    print("Na stole rozkładane jest 5 kart, w tym na początku 3 odkryte.")
    print("Każdy z graczy otrzymuje do ręki 2 karty.")
    print("Pierwszy gracz stawia 'ciemną' o wysokośi 10 zł.")
    print("\nGracz może w swoim ruchu wykonać kilka akcji:\n")
    print("Dokładam - do położonej już stawki na stole dokładasz pieniądze, by dorównać stawkę")
    print("Stawiam - postawienie kwoty wyższej niż aktualna najwyższa na stole, tzw. przebicie")
    print("Po słowie stawiam nie zapomnij powiedzieć kwoty! Możesz postawić od 10 do 1990 zł, ale tylko wielokrotności liczby 10.")
    print("Va banque (czyt. wabank) - postawienie wszystkich swoich pieniędzy. Masz wtedy gwarantowaną obecność w grze do końca rundy.")
    print("Czekam - jest równoznaczne z bardziej popularnym 'sprawdzam'. Jest to nic innego jak nie postawienie niczego, jeśli nie musisz.")
    print("Pass - użyjesz tej komendy wtedy, gdy chcesz się poddać. Równoznaczne z wygraną drugiego gracza w danej rundzie.")
    print("Wycofuję się - jeśli chcesz opuścić grę. Następuje po nim automatyczne zakończenie gry.\n")
    print("Starszeństwo układów:\n")
    print("1. Poker królewski - as, król, dama, walet, dziesiątka w jednym kolorze.")
    print("2. Poker, czyli strit w kolorze - pięć kolejnych kart w jednym kolorze.")
    print("3. Kareta - cztery karty tej samej wartości.")
    print("4. Ful - trójka i para.")
    print("5. Kolor - pięć dowolnych kart w tym samym kolorze.")
    print("6. Strit - pięć kolejnych kart nie w kolorze.")
    print("7. Trójka - trzy karty tej samej wartości.")
    print("8. Dwie pary - dwa razy po 2 karty tej samej wartości.")
    print("9. Para - dwie karty o tej samej wartości.")
    print("10. Wysoka karta - jeśli nie masz żadnego z powyższych układów lub układy są takie same, wygrywa ten kto ma najwyższą kartę.\n")
    print("Mała podpowiedź: karta oznaczona symbolem T to dziesiątka ;).")
    print("Pamiętaj też o tym, że możesz podbić stawkę, czyli użyć komendy stawiam tylko 2 razy w rundzie.\n")

    input("Jeśli zrozumieliście zasady gry i chcecie rozpocząć - naciśnij ENTER :)")
    return
