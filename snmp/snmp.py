import sys
sys.path.append('./tools')
import time
import tools.information as info
import tools.network as nt
import os

path = '/home/san/Documents/ESCOM/Redes3/ServiceChecker/'

class Service:
    def __init__(self, name, ip, port, community='public'):
        self.name = name
        self.ip = ip
        self.port = port
        self.community = community


services = [
    Service('mail', 'localhost', 161),
    Service('tftp', 'localhost', 161),
    Service('ssh', 'localhost', 161),
    Service('dns', 'localhost', 161),
    Service('http', 'localhost', 161)
]


def main():
    threads = []
    while True:
        for service in services:
            # info.createPredictionsDbs(
            #     cpudb='out/cpu' + service.name,
            #     ramdb='out/ram' + service.name,
            #     hdddb='out/hdd' + service.name
            # )

            info.generateAllPredictions(
                service.community,
                service.ip,
                service.port,
                service_name=service.name,
                cpudb='out/cpu' + service.name,
                ramdb='out/ram' + service.name,
                hdddb='out/hdd' + service.name
            )

            print(service.name, "Done")
        os.system('ltx ' + path + 'TitlePage.tex')
        os.system('ltx ' + path + 'main.tex')
        print('Report Generated')


if __name__ == '__main__':
    main()
