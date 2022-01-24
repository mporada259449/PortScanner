import socket
from PyQt6.QtCore import QThread, pyqtSignal

class Scanner(QThread):
    #implementacja skanera portów, podczas uruchamiania tworzy osbny wątek
    progress = pyqtSignal(int)
    def __init__(self):
        QThread.__init__(self)
        self.host = []  #lista hastów
        self.portStart = 0  #pierwszy port
        self.portStop = 0  #ostatni port
        self.connectionTime = 0.01  #maksymalny czas oczikwania na połączenie
        self.saveAll = False  #flaga przechowująca informacje czy zapisywane są wszystkie porty czy tylko otwarte
        self.dataCheck = True  #flaga przechowojąca informacje czy wszystkie podane dane są prawidłowe
        self.ports = {}  #słownik ze znanymi portami
        self.results = []  #wyniki działania skanera

    def run(self):
        #główna funkcja skanujaca porty w podanym przedziale
        if not self.dataCheck:
            #jeśli dane sa nieprawidłowe przerwij działanie
            return
        socket.setdefaulttimeout(self.connectionTime)
        for host in self.host:
            #główna pętla po wszystkich hoostach
            if self.saveAll:
                self.results.append("Ports for host "+host)
            else:
                self.results.append("Opened ports for host " + host)
            for port in range(self.portStart, self.portStop+1):
                #pętala po przedzialne portów
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    #nawiązanie połączenia
                    connection = sock.connect((host, port))
                    if not connection:
                        #jeśli nawiązano połączenie
                        if port in self.ports.keys():
                            #jeśli port o danym numerze jest jest portam znanej usługi dodaje do wyników numer portu i jego usługe
                            self.results.append(str(port)+" open "+self.ports[port])
                        else:
                            #jeśli nie dodaj tylko numer portu
                            self.results.append(str(port)+" open")
                except socket.timeout:
                    #jeśli skończył się czas na nawiązanie połączenia
                    if self.saveAll:
                        #jeśli w programie zapisywane są wszystkie porty zapisz port jako zamknięty
                        if port in self.ports.keys():
                            self.results.append(str(port)+" closed "+self.ports[port])
                        else:
                            self.results.append(str(port)+" closed")
                except ConnectionRefusedError:
                    #odmowa nawiązania połączenia
                    self.results.append("connection refused")
                    break
                sock.close()
                #emitowanie sygnału z wątku
                self.progress.emit(self.portStop-self.portStart-port)


    def setStartPort(self, n):
        #ustawienie portu startu
        self.portStart = n

    def setStopPort(self, n):
        #ustwanie portu stopu
        if self.portStart <= n:
            self.portStop = n
            self.dataCheck = True
        else:
            #jeśli się nie udało ustaw flagę sprawdzającą poprawność danych jako False
            self.results.append("wrong port set")
            self.dataCheck = False

    def setHost(self, host):
        #ustawnienie listy hostów do przeskanowania
        hosts = host.split(", ")
        self.results.clear()
        try:
            #pobranie adresu IP hostów
            self.host = [socket.gethostbyname(x) for x in hosts]
            self.dataCheck = True
        except socket.gaierror:
            # jeśli się nie udało ustaw flagę sprawdzającą poprawność danych jako False
            self.results.append("wrong address")
            self.dataCheck = False

    def setSave(self):
        #zdacydowanie czy przechowywac wszystkie porty czy tylko otwarte

        self.saveAll = False
        if self.portStop - self.portStart <= 20:
            # przechowywane są wszytkie porty tylko jeśli sknowanych jest mniej niż 20 portów dla każdego hosta
            self.saveAll = True

    def getResults(self):
        return self.results

    def knownPorts(self):
        # odczytanie znanych hostów z pliku "ports.txt"
        if len(self.ports.keys())!=0:
            #jeżeli słownik został już stworzony zakończ
            return
        file = open("ports.txt", 'r')
        for line in file:
            idx = line.find(" ")
            self.ports[int(line[:idx])] = line[idx+1:-1]
        file.close()



