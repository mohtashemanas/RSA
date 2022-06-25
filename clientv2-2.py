import socket
import pickle
import rsa
state=-1
HEADERSIZE = 10
ccno="1234567890"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect((socket.gethostname(), 1243))
s.connect(('localhost', 1243))
while True:
    full_msg = b''
    new_msg = True
    while True:
        msg = s.recv(150)
        if new_msg:
            #print("new msg len:",msg[:HEADERSIZE])
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        #print(f"full message length: {msglen}")

        full_msg += msg



        #print(len(full_msg))

        if len(full_msg)-HEADERSIZE == msglen:
            print("Public key received")
            #print(full_msg[HEADERSIZE:])
            bob_pub=pickle.loads(full_msg[HEADERSIZE:])
            print(bob_pub)
            #print(pickle.loads(full_msg[HEADERSIZE:]))
            new_msg = True
            full_msg = b""
        if state==-1:
            productId = input("Give the id of the product you want to buy (integer from 1 to 5) 1. Apple, 2. Orange, 3. Grapes, 4. Banana, 5. Guava: ")
            message1=productId.encode('utf8')
            crypto = rsa.encrypt(message1, bob_pub)
            # msg = pickle.dumps(ccno)
            msg = pickle.dumps(crypto)
            msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8') + msg
        # print(msg)
            s.send(msg)
            print("Encrypted product id sent to server")
            state = 0
        if state ==0:
            ccno = input("Enter your credit card number: ")
            message1 = ccno.encode('utf8')
            crypto = rsa.encrypt(message1, bob_pub)
            #msg = pickle.dumps(ccno)
            msg= pickle.dumps(crypto)
            msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8') + msg
            #print(msg)
            s.send(msg)
            print("Encrypted credit card number sent to server")
            state=1

        if state == 1:
            otp = input("Enter your OTP: ")
            print(otp)
            #msg = pickle.dumps(otp)
            msg = pickle.dumps(rsa.encrypt(otp.encode('utf8'), bob_pub))
            msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8') + msg
            #print(msg)
            s.send(msg)
            print("Encrypted OTP sent to server")

