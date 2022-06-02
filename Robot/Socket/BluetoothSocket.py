import socket

MACAddress = E4-AA-EA-BF-F3-74
port = 246924
connection = socket.socket(socket.AF_BLUETOOTH, socket_SOCK_STREAM, socket.BTPROTO_RFCOMM)

connection.bind((MACAddress, port))
connection.listen(1)
try:
	client, address = connection.accept()
	while 1:
		ReceivedData = client.recv(1024)
		if ReceiveData:
			print(ReceiveData)
except:
	print("Closing Socket")
	client.close()
	connection.close()