## Wymagania (bez tego nie zadziała):

- VPN do sieci AGH (http://panel.agh.edu.pl/docs/openvpn/) jeżeli jestecie poza

- Zainstalujcie biblioteki z requirements.txt. Żeby zainstalować:
 


Na Linuxie:

```bash
 pip install -r requirements.txt
 ```
 


Na Windowsie:

1. Move to the directory with the used interpreter python.exe.

2. Run:
 ```bash
 python.exe -m pip install -r path_to_requirements.txt
 ```
 


W środku są cztery ważne funkcje:
- BRVprintad() - wypisuje wykrywane urządzenia do nagrywania
- BRVgetreply_canraise() - nagrywa (samo wykrywa koniec wypowiedzi) i zwraca
	całe wypowiedziane zdanie (patrz grammars/grammar.abnf),
	lub 'NO COMMAND DETECTED', jeśli nic nie wykryło
- BRVgetreply_cannotraise() - to samo, co powyższa, ale możliwe są jedynie
	komendy "Czekam" i "Pass".
	Przeznaczone do wykrywania komend, kiedy nie można już podbić stawki
- BRVrecorder() - prosi o wypowiadanie komend i zapisuje nagrania do testów


Przykładowe ich użycie jest w pliku runner.py

Program działa poprawnie u mnie na pythonie 3.6 (inne wersje nie były testowane)
Jak wyskakują błędy, to pewnie nie zainstalowalicie bibliotek z requirements.txt