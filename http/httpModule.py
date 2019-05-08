import http.client, time, sys

general_result = None

def getHTTPConnection(ip = "www.google.com", isThread = False):

    global general_result

    start = time.time()

    result = None
    totalSize = None

    try:
        # get the dns resolutions for this domainstart = time.time()
        conn = http.client.HTTPConnection("www.google.com")
        conn.request("HEAD", "/index.html")
        res = conn.getresponse()

        # print(res.status, res.reason)
        b = res.getheaders()
        # print(str(sys.getsizeof(b)))
        totalSize = sys.getsizeof(b)
        totalSize *= 8
        # print(str(totalSize))
        # print(str(finalTime))
        # print(str(round((totalSize / finalTime) / (10 ** 6), 6)))

    except:
        result = None

    # print(dns_answer)
    # print(result)

    end = time.time()

    finalTime = round(end - start, 2)

    if not isThread:
        print (" \\begin{itemize}" +
            " \\item target: " + str(ip) +
            " \\item status: " + ("Up" if (not result) else "Down") +            
            " \\item tiempo de respuesta: " + str(finalTime) + 
            " \\item bytes recibidos: " + str(totalSize) + 
            " \\item ancho de banda: " + str(round((totalSize / finalTime) / (10 ** 6), 6)) + 
            " \\end{itemize}")
    
    else:
        general_result = result

# def getHTTPConnectionMultipleclients(targetURI = 'localhost', port = None, resolverDNS = "127.0.0.1", numberOfClients = 20):
#     start = time.time()
#     threads = [threading.Thread(target=getIPbyURI, args=(targetURI, port, resolverDNS, True)) for _ in range(numberOfClients)]
#     [t.start() for t in threads]
#     [t.join() for t in threads]
#     end = time.time()
#     print (" \\begin{itemize}" +
#             " \\item URI: " + str(targetURI) +
#             " \\item IP associata: " + 
#             ("Caduto" if (not general_result) else ("\\begin{itemize}" + " \\item " + " \\item ".join(general_result) + " \\end{itemize}")) +
#             " \\item Tempo di risposta di " + str(numberOfClients) + " clienti: " + str(round(end - start, 2)) + 
#             " \\end{itemize}")



getHTTPConnection(ip = "www.google.com")
# getIPbyURIMultipleclients(targetURI = 'aula1pc1.test.try', resolverDNS = "127.0.0.1", numberOfClients = 1000)