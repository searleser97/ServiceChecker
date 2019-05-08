import dns.resolver
import socket, time

def getIPbyURI(targetURI = 'localhost', port = None, resolverDNS = "127.0.0.1"):
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
    
    socket.setdefaulttimeout(10)

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

    return (" \\begin{itemize}" +
            " \\item URI: " + str(targetURI) +
            " \\item IP associata: " + 
            ("Caduto" if (not result) else ("\\begin{itemize}" + " \\item " + " \\item ".join(result) + " \\end{itemize}")) +
            " \\item Tempo di risposta: " + str(round(end - start, 2)) + 
            " \\end{itemize}")

ips = getIPbyURI(targetURI = 'aula1pc1.test.try', resolverDNS = "127.0.0.1")

print (ips)
