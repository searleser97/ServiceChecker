import dns.resolver
import socket, time, threading

general_result = None

def getIPbyURI(targetURI = 'localhost', port = None, resolverDNS = "127.0.0.1", isThread = False):
    '''
        this function takes the passed target and optional port and does a dns
        lookup. it returns the ips that it finds to the caller.

        :param targetURI:  the URI that you'd like to get the ip address(es) for
        :type targetURI:   string
        :param port:    which port do you want to do the lookup against?
        :type port:     integer
        :param resolverDNS:  the IP direction to use as a resolver, similar to include into resolv.conf
        :type resolverDNS:   string
        :returns latexString:   string with latex code with the information of the consult
        :rtype latexString:     string

    '''

    global general_result

    customResolver = dns.resolver.Resolver()
    customResolver.nameservers = [resolverDNS]

    if not port:
        port = 443

    start = time.time()

    result = list()

    try:
        # get the dns resolutions for this domain
        dns_answer = customResolver.query(targetURI)
        result = [ip.address for ip in dns_answer]
    except dns.resolver.NXDOMAIN as e:
        # the domain does not exist so dns resolutions remain empty
        result = list()
        pass
    except dns.resolver.NoAnswer as e:
        # the resolver is not answering so dns resolutions remain empty
        result = list()
        pass

    # print(dns_answer)
    # print(result)

    end = time.time()

    if not isThread:
        print (" \\begin{itemize}" +
            " \\item URI: " + str(targetURI) +
            " \\item IP associata: " + 
            ("Caduto" if (not result) else ("\\begin{itemize}" + " \\item " + " \\item ".join(result) + " \\end{itemize}")) +
            " \\item Tempo di risposta: " + str(round(end - start, 2)) + 
            " \\end{itemize}")
    
    else:
        general_result = result

def getIPbyURIMultipleclients(targetURI = 'localhost', port = None, resolverDNS = "127.0.0.1", numberOfClients = 20):
    start = time.time()
    threads = [threading.Thread(target=getIPbyURI, args=(targetURI, port, resolverDNS, True)) for _ in range(numberOfClients)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    end = time.time()
    print (" \\begin{itemize}" +
            " \\item URI: " + str(targetURI) +
            " \\item IP associata: " + 
            ("Caduto" if (not general_result) else ("\\begin{itemize}" + " \\item " + " \\item ".join(general_result) + " \\end{itemize}")) +
            " \\item Tempo di risposta di " + str(numberOfClients) + " clienti: " + str(round(end - start, 2)) + 
            " \\end{itemize}")



getIPbyURI(targetURI = 'aula1pc1.test.try', resolverDNS = "127.0.0.1")
# getIPbyURIMultipleclients(targetURI = 'aula1pc1.test.try', resolverDNS = "127.0.0.1", numberOfClients = 1000)