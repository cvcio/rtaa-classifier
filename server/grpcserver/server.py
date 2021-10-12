import grpc
import time
import logging
import signal
import sys
from concurrent import futures


class GRPCServer(object):
    @property
    def instance(self):
        return self.__server

    def __init__(self, host="[::]", port=50051):
        options = (("grpc.so_reuseport", 1),)
        self.__host = host
        self.__port = port
        self.__server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=10), options=options
        )
        # signal.signal(signal.SIGINT, self.handleSignals)

    def handleSignals(self, signal, frame):
        """
        signalChannel will receive SIGINT events and gracefully stop the server
        """
        self.Stop()

        logging.info("GRPC Classification Server Stopped")
        sys.exit(0)

    def RegisterService(self, service, method, *args):
        """
        calls add_SERVICE_to_server method
        service -- the service handler to register
        method -- the grpc method that initializes the handler
        """
        method(service(args), self.instance)

    def Serve(self):
        """
        start the service server
        """
        url = f"{self.__host}:{self.__port}"
        logging.debug(f"Starting GRPC Server at {url}")

        self.__server.add_insecure_port(url)
        self.__server.start()
        try:
            while True:
                time.sleep(60 * 60 * 24)
        except KeyboardInterrupt:
            self.Stop()

    def Stop(self):
        """
        stop the service server
        """
        logging.debug("Stopping GRPC Server gracefully")
        self.__server.stop(3)
