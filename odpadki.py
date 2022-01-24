'''def setData(self):
        while True:
            try:
                address = input("Set host: ")
                self.host.append(socket.gethostbyname(address))
                answer = input("next host?(y/n): ")
                if answer == "n":
                    break
            except socket.gaierror:
                print("Name or service not known")
        while True:
            try:
                self.portStart = int(input("Set starting port(min: 1): "))
                if self.portStart < 1 or self.portStart > 65535:
                    raise TypeError
                break
            except TypeError:
                print("Invalid port")
            except ValueError:
                print("It isn't a number")
        while True:
            try:
                self.portStop = int(input("Set stoping port(max: 65535): "))
                if self.portStop > 65535 or self.portStop < 1 or self.portStart > self.portStop:
                    raise TypeError
                break
            except TypeError:
                print("Invalid port")
            except ValueError:
                print("It isn't a number")

        if self.portStop-self.portStart <= 20:
            self.displayAll = True

        self.knownPorts()


            def scan(self):
        socket.setdefaulttimeout(self.connectionTime)
        for host in self.host:
            print("Ports for host ", host)
            self.results.append("Ports for host "+host)
            for port in range(self.portStart, self.portStop+1):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    connection = sock.connect((host, port))
                    if not connection:
                        if port in self.ports.keys():
                            self.results.append(str(port)+" open "+self.ports[port])
                            print(port, " open", self.ports[port])
                        else:
                            print(port, " open")
                            self.results.append(str(port)+" open")
                except socket.timeout:
                    if self.displayAll:
                        print(port, " close")
                        if port in self.ports.keys():
                            self.results.append(str(port)+" closed "+self.ports[port])
                        else:
                            self.results.append(str(port)+" closed")
                sock.close()

        return self.results

    '''