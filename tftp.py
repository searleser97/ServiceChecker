import tftpy
import timeit
obj = {}
try:
	client = tftpy.TftpClient('localhosts', 69)
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
		\\item interpretacion: OK\n
		\\item download time: """ + obj['download_time'] + """
		\\end{itemize}
	"""
print(str)