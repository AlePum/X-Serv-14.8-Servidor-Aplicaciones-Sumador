import socket

class webApp:
    """Root of a hierarchy of classes implementing web applications
    This class does almost nothing. Usually, new classes will
    inherit from it, and by redefining "parse" and "process" methods
    will implement the logic of a web application in particular.
    """

    def parse (self, request):
        """Parse the received request, extracting the relevant information."""

        return None

    def process (self, parsedRequest):
        """Process the relevant elements of the request.
        Returns the HTTP code for the reply, and an HTML page.
        """

        return ("200 OK", "<html><body><h1>It works!</h1></body></html>")

    def __init__ (self, hostname, port):
        """Initialize the web application."""

        # Create a TCP objet socket and bind it to a port
        mySocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mySocket.bind((hostname, port))

        # Queue a maximum of 5 TCP connection requests
        mySocket.listen(5)

        # Accept connections, read incoming data, and call
        # parse and process methods (in a loop)
        primero = None
        while True:
            print 'Waiting for connections'
            (recvSocket, address) = mySocket.accept()
            print 'HTTP request received (going to parse and process):'
            request = recvSocket.recv(2048)
            print request
            try:
                parsedRequest = self.parse (request)
            except IndexError:
                continue
            except ValueError:
                recvSocket.send("HTTP/1.1 200 OK\r\n\r\n" +
                            "<html><body><h1>Pon numeros</h1></body></html>\r\n")
                continue
            (returnCode, htmlAnswer, primero) = self.process (parsedRequest, primero)
            print 'Answering back...'
            recvSocket.send("HTTP/1.1 " + returnCode + " \r\n\r\n"
                              + htmlAnswer + "\r\n")
            recvSocket.close()

class Sumador(webApp):
    def parse(self,request):
        numero = int(request.split()[1][1:])
        return numero

    def process(self, parsedRequest, primero):
        if primero == None:
            primero  = parsedRequest
            htmlAnswer = ("<html><body><h1>" + "Primer sumando: " + str(primero) +
                        "</p>" + "Dame otro" + "</body></html>")
        else:
            resultado = str(primero + parsedRequest)
            htmlAnswer = ( "<html><body><h1>" + "Primer sumando: " + str(primero) +
                        "</p>" + "Segundo sumando: " + str(parsedRequest) +
                        "</p>" + "El resultado es: " + str(resultado) +
                        "</body></html>")
            primero = None
        return("HTTP/1.1 200 OK", htmlAnswer, primero)

if __name__ == "__main__":
    testWebApp = Sumador("localhost", 1234)
