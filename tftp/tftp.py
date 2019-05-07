import tftpy
import timeit
obj = {}
server = 'localhost'
port = 69
try:
	client = tftpy.TftpClient(server, port)
	obj['status'] = 'Up'
	start = timeit.timeit()
	client.download('test.txt', 'test.txt')
	end = timeit.timeit()
	obj['download_time'] = format(abs(end - start), ".8f")
except:
	obj['status'] = 'Down'
	obj['download_time'] = '--'
str = """
		\\begin{itemize}\n
		\\item status: """ + obj['status'] + """\n
		\\item download time: """ + obj['download_time'] + """\n
		\\end{itemize}
	"""
print(str)