import socket, time

def getIPbyURI(target = 'localhost', port = None):
    '''
        this function takes the passed target and optional port and does a dns
        lookup. it returns the ips that it finds to the caller.

        :param target:  the URI that you'd like to get the ip address(es) for
        :type target:   string
        :param port:    which port do you want to do the lookup against?
        :type port:     integer
        :returns ips:   all of the discovered ips for the target
        :rtype ips:     list of strings

    '''
    
    socket.setdefaulttimeout(10)

    if not port:
        port = 443

    start = time.time()

    try:
        result = list(map(lambda x: x[4][0], socket.getaddrinfo('{}.'.format(target),port,type=socket.SOCK_STREAM)))

    except:
        result = list()

    print(result)

    end = time.time()

    return (" \\begin{itemize}" +
            " \\item URI: " + str(target) +
            " \\item IP associata: " + 
            ("Caduto" if (not result) else ("\\begin{itemize}" + " \\item " + " \\item ".join(result) + " \\end{itemize}")) +
            " \\item Tempo di risposta: " + str(round(end - start, 2)) + 
            " \\end{itemize}")

ips = getIPbyURI(target = 'aula1pc1.test.try')

print (ips)
