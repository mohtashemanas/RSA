import socket
import time
import pickle
import rsa
import string
import random
(bob_pub, bob_priv) = rsa.newkeys(512)
HEADERSIZE = 10
state=-1
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.bind((socket.gethostname(), 1243))
s.bind(('0.0.0.0', 1243))
s.listen(5)
new_msg = True
OTP="123"
while True:
    full_msg = b''
    # now our endpoint knows about the OTHER endpoint.
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")

    d = bob_pub     #{1:"hi", 2: "there"}
    msg = pickle.dumps(d)
    msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg
    #print(msg)
    clientsocket.send(msg)
    if state==-1:
        state=0
        msg = clientsocket.recv(200)
        if new_msg:
            # print("new msg len:",msg[:HEADERSIZE])
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        # print(f"full message length: {msglen}")

        full_msg += msg

        # print(len(full_msg))

        if len(full_msg) - HEADERSIZE == msglen:
            print("full msg recvd")
            print(full_msg[HEADERSIZE:])
            prodEncypted = pickle.loads(full_msg[HEADERSIZE:])
            prodUnencrypted = rsa.decrypt(prodEncypted, bob_priv)
            print("Product id decrypted:")
            print(prodUnencrypted.decode('utf8'))
            # print(pickle.loads(full_msg[HEADERSIZE:]))
            new_msg = True
            full_msg = b""
    if state==0:
        state=1
        msg = clientsocket.recv(200)
        if new_msg:
            #print("new msg len:",msg[:HEADERSIZE])
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        #print(f"full message length: {msglen}")

        full_msg += msg

        #print(len(full_msg))

        if len(full_msg)-HEADERSIZE == msglen:
            print("full msg recvd")
            print(full_msg[HEADERSIZE:])
            ccEncypted=pickle.loads(full_msg[HEADERSIZE:])
            ccUnencrypted=rsa.decrypt(ccEncypted, bob_priv)
            print("Credit card number decrypted:")
            print(ccUnencrypted.decode('utf8'))
            #print(pickle.loads(full_msg[HEADERSIZE:]))
            new_msg = True
            full_msg = b""
        OTP = ''.join(random.choices(string.digits, k=6))
        print("Please use this OTP")
        print(OTP)
        if state==1:
            state = 1
            msg = clientsocket.recv(200)
            if new_msg:
                #print("new msg len:", msg[:HEADERSIZE])
                msglen = int(msg[:HEADERSIZE])
                new_msg = False

            #print(f"full message length: {msglen}")

            full_msg += msg

            #print(len(full_msg))

            if len(full_msg) - HEADERSIZE == msglen:
                print("Encrypted OTP received")

                #print(full_msg[HEADERSIZE:])

                ReceivedOTP=pickle.loads(full_msg[HEADERSIZE:])
                print(ReceivedOTP)
                ReceivedOTPDecrypted = rsa.decrypt(ReceivedOTP, bob_priv)
                print("Received OTP")
                print(ReceivedOTPDecrypted)
                new_msg = True
                full_msg = b""
                #ReceivedOTP = str(pickle.loads(full_msg[HEADERSIZE:]))
                if ReceivedOTPDecrypted.decode('ascii') == OTP:
                    print("OTP verified.  Transaction complete")
                else:
                    print("Wrong OTP. Transaction failed.")


