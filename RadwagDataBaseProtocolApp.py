import socket
import re
import time

#Taking IP/Port numbers from user

print("Please enter IP adress of your device:\n")
IP_number_of_device = input()
print("Please enter the port number of your device:\n")
Port_Number_of_device = int(input())


while True: #endless loop in order to sending commands continously

    time.sleep(5) #delay 

#Server Connections:

    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    IP,PORT = IP_number_of_device,Port_Number_of_device
    connection.connect_ex((IP,PORT))

    def get_sock():
        return connection

    def send_data(message):
        connection.sendall(bytes(message+"\r\n","utf-8"))
        print(connection.sendall(bytes(message,"utf-8")))

    def receive_data():
        data = connection.recv(10485760)
        return (data,"utf-8")

#Commnad Sending:

    def command_send(Command):
        send_data(Command)
        return str(receive_data())

#Error detection

    def detect_error_messages(message):
        if "HI" in message and "kg" in message and "   " in message :
            message = "err"
            return  message
        else:
            return message

#Extracting index value

    def extract_index_value(Command):
        index = re.search(r"<COUNT=(\d+)>", Command)
        count = int(index.group(1))
        return count


#Main Part:
    connection.settimeout(300)
    varCommandCountIndex = 'DBINFO<TABLE=WEIGHMENTS><PARAM=COUNT>CRLF' #Database command for count total index in database
    Command_Response = detect_error_messages(command_send(varCommandCountIndex))

    if Command_Response == "err":
        print("Error was found!!!")
    else:
        Command_Response = extract_index_value(Command_Response)
        Old_Index_Value = Command_Response
    
        Command_Response = detect_error_messages(command_send(varCommandCountIndex))
        if Command_Response == "err":
            print("Error was found")
        else:
            Command_Response = extract_index_value(Command_Response)
            New_Index_Value = Command_Response
            if New_Index_Value != Old_Index_Value:
                varCommandReadLast  = 'DBREADID<TABLE=WEIGHMENTS><KEY={}>CRLF'.format(New_Index_Value)
                Command_Response = detect_error_messages(command_send(varCommandReadLast))
                if Command_Response == "err":
                    print("Error was found")
                else:
                    print("Newly entered database record:\n{}".format(Command_Response))    
                
    


