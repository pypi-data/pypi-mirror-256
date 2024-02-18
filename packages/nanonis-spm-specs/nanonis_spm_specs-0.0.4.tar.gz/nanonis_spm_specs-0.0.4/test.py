import nanonis_spm_specs
import socket

TCP_IP = '10.0.0.37'
TCP_PORT = 6501
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((TCP_IP, TCP_PORT))



n = nanonis_spm_specs.Nanonis(socket)

#TEST COMMAND
n.DataLog_Open()
