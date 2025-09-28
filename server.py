from socket import *
import json
import threading

# slags konstanter
serverName = 'localhost'
serverPort = 7

pf = []
count = 0

def create_chunks():
    chunks = []
    words = []
    
    #åbner 
    with open("webster-dictionary.txt", "r", encoding="utf-8") as dictionary:
        #for hver linje i filen tilføjer jeg ordet til listen word
        for line in dictionary:
            word = line.strip()
            words.append(word)
                
            #er der 5000 ord i listen så tilføjer jeg den listen til chunks, og tømmer words listen
            if len(words) == 10000:
                chunks.append(words)
                words = []
                #tilføjer den sidste chunk med de ord der er tilbage
    if words:
        chunks.append(words)
        print(f"Final chunk {len(chunks)} created with {len(words)} words")
    
    return chunks

chunks = create_chunks()


def get_chunk(chunks):
    return chunks.pop(0)




def handle_client(connectionSocket, addr):
    global count 
    #en forbindelse
    try:
        print(f"Ny forbindelse fra {addr}")
        
        # Modtag besked fra client
        message = connectionSocket.recv(1024)
        # Lav et svar (eksempel)
        dmessage = message.decode()
        if dmessage.strip() == "chunk":
            chunk_send = get_chunk(chunks)
            count = count + 1    
            response_json = json.dumps(chunk_send)
            data = (response_json + '\n').encode('utf-8')
            connectionSocket.sendall(data)
        else:
            passwords = message.decode()
            AddResult(passwords)
            chunk_send = get_chunk(chunks)
            count = count + 1    
            response_json = json.dumps(chunk_send)
            data = (response_json + '\n').encode('utf-8')
            connectionSocket.sendall(data)
            for i in pf:
                print(i)
        
            
    except Exception as e:
        print(f"Fejl med client {addr}: {e}")
    finally:
        connectionSocket.close()
        print(f"Forbindelse til {addr} lukket")


def AddResult(result):
    pf.append(result)
    return pf
             
#laver threaded TCP server               
serverSocket = socket(AF_INET, SOCK_STREAM) # Stream = tcp
serverSocket.bind((serverName, serverPort))
serverSocket.listen(5)  # Kan håndtere op til 5 ventende forbindelser
print(f"Threaded server klar på {serverName}:{serverPort}")

try:
    while True:
        # Accepter ny client forbindelse
        connectionSocket, addr = serverSocket.accept()
        
        # Start en ny thread for hver client
        client_thread = threading.Thread(
            target=handle_client, 
            args=(connectionSocket, addr)
        )
        client_thread.daemon = True  # Thread dør når main program slutter
        client_thread.start()
finally:
    serverSocket.close() 
    if (count >= 32):
        for i in pf:
            print(i)

