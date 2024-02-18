import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 4000))
sock.sendall(
    b"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin et tempus lectus. Sed a bibendum elit, sit amet tempor quam. Curabitur ac commodo sapien. Quisque sollicitudin laoreet augue, ut blandit sem efficitur eu. Curabitur vulputate risus felis, vel porta magna sagittis eu. Etiam convallis ex id blandit aliquet. Ut mollis elit et lectus placerat, et euismod purus pellentesque.",

)
print(sock.recv(1024))
