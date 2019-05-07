import sys
sys.path.append('./tools')

import tools.information as info
import tools.network as nt

class Service:
  def __init__(self, name, ip, port, community='public'):
    self.name = name
    self.ip = ip
    self.port = port
    self.community = community

services = [
  # Service('mail', 'localhost', 161),
  # Service('tftp', 'localhost', 161),
  # Service('ssh', 'localhost', 161),
  # Service('dns', 'localhost', 161),
  Service('http', 'localhost', 161)
]

def main():
  for service in services:
    uptime = nt.getUpTime(service.community, service.ip, service.port)
    interfaces = nt.getInterfaces(service.community, service.ip, service.port)
    so = 'Linux'

    with open(service.name + '_stats.tex', 'w') as f:
      f.write('\\begin{itemize}\n')
      f.write('\\item \\textbf{Sistema Operativo:} ' + so + '\n')
      f.write('\\item \\textbf{Tiempo de actividad del sensor:} ' + str(uptime) + '\n')
      f.write('\\item \\textbf{Numero de interfaces:} ' + str(len(interfaces)) + '\n')
      f.write('\\end{itemize}' + '\n')
    
    info.generateAllPredictions(
      service.community,
      service.ip,
      service.port,
      cpudb='out/cpu' + service.name,
      ramdb='out/ram' + service.name,
      hdddb='out/hdd' + service.name
    )

if __name__ == '__main__':
  main()