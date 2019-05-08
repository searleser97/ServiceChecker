import tftpy
import timeit
obj = {}
server = 'localhost'
port = 70
i=0
while i<5:
	f = open (str(i)+'test.txt','w')
	f.write("prueba pedorra %d"%i)
	f.close
	try:
		client = tftpy.TftpClient(server, port)
		obj['status'] = 'Up'
		start = timeit.timeit()
		client.upload(str(i)+'test.txt', str(i)+'test.txt')
		end = timeit.timeit()
		obj['upload_time'] = format(abs(end - start), ".8f")
		start = timeit.timeit()
		client.download(str(i)+'test.txt', str(i)+'test.txt')
		end = timeit.timeit()
		obj['download_time'] = format(abs(end - start), ".8f")
	except:
		obj['status'] = 'Down'
		obj['download_time'] = '--'
		obj['upload_time'] = '--'
	i+=1
str = """
		\\begin{itemize}\n
		\\item statut: """ + obj['status'] + """\n
		\\item temp de telechargement: """ + obj['download_time'] + """ s\n
		\\item nombre de fichiers: """ + str(i) + """\n
		\\item temp de charge: """ + obj['upload_time'] + """ s\n
		\\item nombre de fichiers: """ + str(i) + """\n
		\\end{itemize}
	"""
print(str)
