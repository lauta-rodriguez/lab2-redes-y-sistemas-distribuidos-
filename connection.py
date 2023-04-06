# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Copyright 2014 Carlos Bederián
# $Id: connection.py 455 2011-05-01 00:32:09Z carlos $

import socket
from constants import *
from base64 import b64encode
from commands import *


class Connection(object):
    """
    Conexión punto a punto entre el servidor y un cliente.
    Se encarga de satisfacer los pedidos del cliente hasta
    que termina la conexión.
    """

    def __init__(self, socket, directory):
        self.socket = socket
        self.directory = directory
        self.is_connected = True

    def read_line(self, buffer):
        """
        Lee una línea del socket, y se queda con el segmento del buffer hasta EOL.
        """

        while (not EOL in buffer) or (len(buffer) > MAX_BUFFER):
            buffer += self.socket.recv(BUFFER_SIZE).decode("ascii")

        if len(buffer) > MAX_BUFFER:
            return None, buffer

        line, buffer = buffer.split(EOL, 1)
        return line, buffer

    def send(self, code, response):
        # encode the response to base64
        response = b64encode(response.encode())
        # send the response to the client
        self.socket.send(response)

    def parse_command(self, line):
        """
        Parsea la linea y devuelve un codigo y una lista de argumentos
        """
        pass

    def handle(self):
        """
        Atiende eventos de la conexión hasta que termina.
        """
        buffer = ""
        while self.is_connected:
            # En line: una linea que termina con EOL, en buffer: resto del byte stream
            line, buffer = self.read_line(buffer)
            if not line:
                # El line es muy largo (más que MAX_BUFFER), (i.e., no pudimos leer una linea valida)
                # Antes de cerrar la conexión, enviamos un mensaje de error
                self.send(BAD_REQUEST, error_messages[BAD_REQUEST])
                self.socket.close()
                self.is_connected = False
                break

            # TODO: Parseamos la linea y extraemos un codigo y una lista de argumentos
            # devolver en response un string que contenga todos los argumentos
            # separados por espacios
            # enviar la respuesta al cliente

            if buffer == "":
                # No hay mas datos en el buffer, cerramos la conexión
                self.socket.close()
                self.is_connected = False
