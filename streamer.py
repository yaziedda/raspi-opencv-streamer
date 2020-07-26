import cv2
import numpy
import socket
import struct
import threading
# from io import BytesIO
from PIL import Image
import io

class Streamer(threading.Thread):

    def __init__(self, hostname, port):
        threading.Thread.__init__(self)

        self.hostname = hostname
        self.port = port
        self.running = False
        self.streaming = False
        self.jpeg = None

    def run(self):

        # server_socket = socket.socket()
        # server_socket.bind(('0.0.0.0', 8000))
        # server_socket.listen(0)

        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print('Socket created')

        # s.bind((self.hostname, self.port))
        # print('Socket bind complete')

        # payload_size = struct.calcsize("L")

        # s.listen(10)
        # print('Socket now listening')

        # self.running = True

        # while self.running:

        #     print('Start listening for connections...')

        #     conn, addr = s.accept()
        #     print("New connection accepted.")

        #     while True:

        #         data = conn.recv(payload_size)

        #         if data:
        #             # Read frame size
        #             msg_size = struct.unpack("L", data)[0]

        #             # Read the payload (the actual frame)
        #             data = b''
        #             while len(data) < msg_size:
        #                 missing_data = conn.recv(msg_size - len(data))
        #                 if missing_data:
        #                     data += missing_data
        #                 else:
        #                     # Connection interrupted
        #                     self.streaming = False
        #                     break

        #             # Skip building frame since streaming ended
        #             if self.jpeg is not None and not self.streaming:
        #                 continue

        #             # Convert the byte array to a 'jpeg' format
        #             memfile = BytesIO()
        #             memfile.write(data)
        #             memfile.seek(0)
        #             frame = numpy.load(memfile)

                    # ret, jpeg = cv2.imencode('.jpg', frame)
                    # self.jpeg = jpeg

                    # self.streaming = True
        #         else:
        #             conn.close()
        #             print('Closing connection...')
        #             self.streaming = False
        #             self.jpeg = None
        #             break

        # # print('Exit thread.')
        # server_socket = socket.socket()
        # server_socket.bind((self.hostname, self.port))
        # server_socket.listen(0)

        # # Accept a single connection and make a file-like object out of it
        # connection = server_socket.accept()[0].makefile('rb')
        # try:
        #     while True:
        #         # Read the length of the image as a 32-bit unsigned int. If the
        #         # length is zero, quit the loop
        #         image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        #         if not image_len:
        #             break
        #         # Construct a stream to hold the image data and read the image
        #         # data from the connection
        #         image_stream = BytesIO()
        #         image_stream.write(connection.read(image_len))
        #         # Rewind the stream, open it as an image with PIL and do some
        #         # processing on it
        #         image_stream.seek(0)
        #         image = Image.open(image_stream).convert('RGB')
        #         # print('Image is %dx%d' % image.size)
        #         # image.verify()
        #         # print('Image is verified')
        #         print(image)

        #         frame = numpy.array(image) 
        #         print(frame)
        #         # Convert RGB to BGR 
        #         ret, jpeg = cv2.imencode('.jpg', frame)

                # self.jpeg = jpeg

                # self.streaming = True
        # Accept a single connection and make a file-like object out of it
        # connection = server_socket.accept()[0].makefile('rb')
        # try:
        #     while True:
        #         # Read the length of the image as a 32-bit unsigned int. If the
        #         # length is zero, quit the loop
        #         image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        #         if not image_len:
        #             break
        #         # Construct a stream to hold the image data and read the image
        #         # data from the connection
        #         image_stream = io.BytesIO()
        #         image_stream.write(connection.read(image_len))
        #         # Rewind the stream, open it as an image with PIL and do some
        #         # processing on it
        #         image_stream.seek(0)
        #         image = Image.open(image_stream)
        #         print('Image is %dx%d' % image.size)
        #         image.verify()
        #         print('Image is verified')
        # finally:
        #     connection.close()
        #     server_socket.close()
        server_socket = socket.socket()
        server_socket.bind(('0.0.0.0', 8000))  
        server_socket.listen(0)
        print("Listening")
        connection = server_socket.accept()[0].makefile('rb')
        try:
            img = None
            while True:
                image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
                if not image_len:
                    break
                image_stream = io.BytesIO()
                image_stream.write(connection.read(image_len))
                image_stream.seek(0)
                image = Image.open(image_stream)
                im = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)

                ret, jpeg = cv2.imencode('.jpg', im)
                self.jpeg = jpeg

                self.streaming = True
            #     cv2.imshow('Video',im)
            #     if cv2.waitKey(1) & 0xFF == ord('q'):
            #        break
            # cv2.destroyAllWindows()
        finally:
            connection.close()
            server_socket.close()


    def stop(self):
        self.running = False

    def get_jpeg(self):
        return self.jpeg.tobytes()
