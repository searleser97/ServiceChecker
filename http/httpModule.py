import http.client, time, sys, threading

general_result = None
general_size = None

def getHTTPConnection(ip = "www.google.com", isThread = False):

    global general_result, general_size

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
        totalSize = None

    # print(dns_answer)
    # print(totalSize)

    end = time.time()

    finalTime = round(end - start, 2)

    if not isThread:
        print (" \\begin{itemize}" +
            " \\item target: " + str(ip) +
            " \\item status: " + ("Down" if (not totalSize) else "Up") +            
            " \\item tiempo de respuesta: " + str(finalTime) + 
            " \\item bytes recibidos: " + str(totalSize) + 
            " \\item ancho de banda: " + str(round((totalSize / finalTime) / (10 ** 6), 6)) + 
            " \\end{itemize}")
    
    else:
        general_size = totalSize

def getHTTPConnectionMultipleclients(ip = "www.google.com", numberOfClients = 20):
    start = time.time()
    threads = [threading.Thread(target=getHTTPConnection, args=(ip, True)) for _ in range(numberOfClients)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    end = time.time()
    print (" \\begin{itemize}" +
        " \\item target: " + str(ip) +
        " \\item status: " + ("Down" if (not general_size) else "Up") +            
        " \\item tiempo de respuesta de " + str(numberOfClients) + " clientes: " + str(round(end - start, 2)) + 
        " \\item bytes recibidos: " + str(general_size) + 
        " \\item ancho de banda: " + str(round((general_size / (end - start)) / (10 ** 6), 6)) + 
        " \\end{itemize}")



getHTTPConnection(ip = "www.google.com")
# getHTTPConnectionMultipleclients(ip = "www.google.com", numberOfClients = 10)