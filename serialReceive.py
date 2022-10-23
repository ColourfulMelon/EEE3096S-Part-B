import serial
import sys
import threading
import csv

#thread to print output to the console
def main():
    print("Enter 'q' to quit, 'a' to activate transmsission, 's' to save data to a csv or 't' to test the connection")
    while(1):
        # Wait until there is data waiting in the serial buffer
        if(serialPort.in_waiting > 0):
            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline()
            # Print the contents of the serial data
            arrOut.append(serialString.decode('Ascii'))
            print(arrOut[len(arrOut)-1])

arrOut = []                                 # Used to hold the data sent through the serial connection in an array
serialString = ""                           # Used to hold data coming over UART
print("Welcome to the LOT PC User Interface")
comNum = input("Please enter the number of the COM port that your LOT reciever is connected to (E.g. 3 for COM3)")
serialPort = serial.Serial(port = "COM" + str(comNum), baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
print("Connected to COM" + str(comNum) + " at 9600 baud")
main_thread = threading.Thread(name='main program', target=main, daemon=True)
active = False

#input handling thread
while True:
    command = input().lower()
    if command == 'q': #quit
        print('Terminating program')
        sys.exit(0)
    elif command == 'a': #activate
        if(not active):
            print('Activating transmission')
            serialPort.writelines("activate")
            active = True
            main_thread.start()
        else:
            print('Transmission already active')
    elif command == 's': #save to csv
        fName = input("Please enter the name of the file you would like to save to (E.g. 'data') for data.csv")
        fLines= input("Please enter how many lines of data you would like to save (E.g. Entering '5' will write the last 5 data points to the file, Press enter to save all)")
        print('Saving data to data.csv')
        if(fLines == ""):
            flines = len(arrOut)
        with open(fName+'.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(arrOut[min(len(arrOut)-fLines,0):])
    elif command == 't': #test connection
        print('Testing serial connection, you should see a response from the LOT reciever')
        serialPort.writelines("test")
        serialString = serialPort.readline()
    else:
        print("Unrecognised command")
        print("Enter 'q' to quit, 'a' to activate transmsission, 's' to save data to a csv or 't' to test the connection")