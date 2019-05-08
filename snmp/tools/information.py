import sys
import time
import rrdt
import rrdtool
import network as nt
import threading as thr

sys.path.append('./data')
agents_db = './data/agents.txt'
tcp_db = './data/rd/tcp'
snmp_db = './data/rd/snmp'
icmp_db = './data/rd/icmp'
udp_db = './data/rd/udp'
traffic_db = './data/rd/traffic'
cpu_db = './data/rd/cpu'
hdd_db = './data/rd/hdd'
ram_db = './data/rd/ram'
abe_db = './data/rd/aberration'

def getAgents():
    agents = []
    with open(agents_db) as file:
        for agent in file:
            info = agent.split(' ')
            if not nt.hasConexion(info[0]):
                info[-1] = 'DOWN'
            agents.append(info)
    return agents

def addAgent(agent):
    with open(agents_db, 'a') as file:
        file.write(agent + '\n')

def deleteAgent(agent_id):
    with open(agents_db, "r") as file:
        lines = file.readlines()
        with open(agents_db, "w") as new_file:
            for line in lines:
                if line.split(' ')[0] == agent_id:
                    pass
                else:
                    new_file.write(line)

def getAgentOS(community, ip, port):
    return nt.getOS(community, ip, port)

def getAgentLocation(community, ip, port):
    return nt.getLocation(community, ip, port)

def getAgentName(community, ip, port):
    return nt.getName(community, ip, port)

def getAgentUptime(community, ip, port):
    return nt.getUpTime(community, ip, port)

def getAgentInterfaces(community, ip, port):
    return nt.getInterfaces(community, ip, port)

def generateAllTraffic(community, ip, port):
    rrdt.createRRDDatabase(tcp_db)
    rrdt.createRRDDatabase(snmp_db)
    rrdt.createRRDDatabase(icmp_db)
    rrdt.createRRDDatabase(udp_db)
    rrdt.createRRDDatabase(traffic_db)

    thr.Thread(target=__generateGeneralTraffic, args=(community, ip, port,'getInputTCPTraffic', 'getOutputTCPTraffic', tcp_db), daemon=True).start()
    thr.Thread(target=__generateGeneralTraffic, args=(community, ip, port,'getInputSNMPTraffic', 'getOutputSNMPTraffic', snmp_db), daemon=True).start()
    thr.Thread(target=__generateGeneralTraffic, args=(community, ip, port,'getInputICMPTraffic', 'getOutputICMPTraffic', icmp_db), daemon=True).start()
    thr.Thread(target=__generateGeneralTraffic, args=(community, ip, port,'getInputUDPTraffic', 'getOutputUDPTraffic', udp_db), daemon=True).start()
    thr.Thread(target=__generateGeneralTraffic, args=(community, ip, port,'getInputTraffic', 'getOutputTraffic', traffic_db), daemon=True).start()
    thr.Thread(target=__generateAllImages, daemon=True).start()

def __generateGeneralTraffic(community, ip, port, inputMethod, outputMethod, db):
    total_input_traffic = 0
    total_output_traffic = 0
    while True:
        try:
            total_input_traffic = int(getattr(nt,inputMethod,)(community, ip, port))
        except ValueError:
            total_input_traffic = 0
        try:
            total_output_traffic = int(getattr(nt,outputMethod,)(community, ip, port))
        except ValueError:
            total_output_traffic = 0
        value = "N:" + str(total_input_traffic) + ':' + str(total_output_traffic)
        rrdt.updateAndDumpRRDDatabase(db, value)
        time.sleep(5)

def __generateAllImages():
    current_time = str(int(time.time()))
    while True:
        rrdt.createRRDImage(tcp_db, current_time, "Equipo 12 tcp")
        rrdt.createRRDImage(snmp_db, current_time, "Equipo 12 snmp")
        rrdt.createRRDImage(icmp_db, current_time, "Equipo 12 icmp")
        rrdt.createRRDImage(udp_db, current_time, "Equipo 12 udp")
        rrdt.createRRDImage(traffic_db, current_time, "Equipo 12 traffic")
        time.sleep(30)

def createPredictionsDbs(cpudb, ramdb, hdddb):
    global cpu_db
    global ram_db
    global hdd_db
    cpu_db = cpudb
    ram_db = ramdb
    hdd_db = hdddb
    rrdt.createPredictionDatabase(cpu_db)
    rrdt.createPredictionDatabase(ram_db)
    rrdt.createPredictionDatabase(hdd_db)

def generateAllPredictions(community, ip, port, service_name='http', cpudb=None, ramdb=None, hdddb=None):
    global cpu_db
    global ram_db
    global hdd_db
    cpu_db = cpudb
    ram_db = ramdb
    hdd_db = hdddb
    __generateGeneral(community, ip, port,'getUnixCPU', cpu_db)
    __generateGeneral(community, ip, port,'getUnixHDD', hdd_db)
    __generateGeneral(community, ip, port,'getUnixAvaliableRam', ram_db, 'getUnixTotalRam')
    __generatePredictionImages()
    __generateInfoAsTex(community, ip, port, service_name)
    # cpu = thr.Thread(target=__generateGeneral, args=(community, ip, port,'getUnixCPU', cpu_db), daemon=True)
    # hdd = thr.Thread(target=__generateGeneral, args=(community, ip, port,'getUnixHDD', hdd_db), daemon=True)
    # ram = thr.Thread(target=__generateGeneral, args=(community, ip, port,'getUnixAvaliableRam', ram_db, 'getUnixTotalRam'), daemon=True)
    # imgs = thr.Thread(target=__generatePredictionImages, daemon=True)
    # infoAsTex = thr.Thread(target=__generateInfoAsTex, args=(community, ip, port, service_name), daemon=True)
    # return [cpu, hdd, ram, imgs, infoAsTex]

def generateAllAberrations(community, ip, port):
    rrdt.createAberrationDatabase(abe_db)
    thr.Thread(target=__generateGeneral, args=(community,ip, port,'getCustomOID',abe_db), daemon=True).start()
    thr.Thread(target=__generateAberrationImages, daemon=True).start()

def __generateGeneral(community, ip, port, method, db, method2=None):
    if method2:
        try:
            snmp_total_value = int(getattr(nt,method2)(community, ip, port))
        except ValueError:
            snmp_total_value = 0
    if True:
        if method2:
            try:
                snmp_pre_value = snmp_total_value - int(getattr(nt,method)(community, ip, port))
                snmp_value = (snmp_pre_value * 100) // snmp_total_value
            except ValueError:
                snmp_value = 0
        else:
            try:
                snmp_value = int(getattr(nt,method)(community, ip, port))
            except ValueError:
                snmp_value = 0
        value = "N:" + str(snmp_value)
        rrdt.updateAndDumpRRDDatabase(db, value)
        # time.sleep(1)

def __generatePredictionImages():
    current_time = str(int(time.time()))
    if True:
        rrdt.createRRDPredictionImage(cpu_db, current_time, "CPU", "25", "50", "75")
        rrdt.createRRDPredictionImage(ram_db, current_time, "RAM", "25", "50", "75")
        rrdt.createRRDPredictionImage(hdd_db, current_time, "HDD", "25", "50", "75")
        # time.sleep(30)

def __generateAberrationImages():
    while True:
        rrdt.createAberrationImage(abe_db)
        time.sleep(30)

def __generateInfoAsTex(community, ip, port, service_name):
    path = '/home/san/Documents/ESCOM/Redes3/ServiceChecker/snmp/'
    if True:
        print(service_name)
        uptime = nt.getUpTime(community, ip, port)
        interfaces = nt.getInterfaces(community, ip, port)
        so = nt.getOS(community, ip, port).replace('_', '\\_').replace('#', '\\#')
        print(service_name + ": ", uptime, interfaces, so)
        with open(path + service_name + '_stats.tex', 'w') as f:
            f.write('\\begin{itemize}\n')
            f.write('\\item \\textbf{Sistema Operativo:} ' + so + '\n')
            f.write('\\item \\textbf{Tiempo de actividad del sensor:} ' + str(uptime) + '\n')
            f.write('\\item \\textbf{Numero de interfaces:} ' + str(len(interfaces)) + '\n')
            f.write('\\end{itemize}' + '\n')
            plots = (""
            "\\begin{figure}[!htb]\n"
            "\\minipage{0.33\\textwidth}\n"
                "\\includegraphics[width=\\linewidth]{" + path + "out/cpu" + service_name + "/trafico.png}\n"
                "\\caption{CPU}\n"
            "\\endminipage\\hfill\n"
            "\\minipage{0.33\\textwidth}\n"
                "\\includegraphics[width=\\linewidth]{" + path + "out/hdd" + service_name + "/trafico.png}\n"
                "\\caption{Disco Duro}\n"
            "\\endminipage\\hfill\n"
            "\\minipage{0.33\\textwidth}%\n"
                "\\includegraphics[width=\\linewidth]{" + path + "out/ram" + service_name + "/trafico.png}\n"
                "\\caption{Memoria Ram}\n"
            "\\endminipage\n"
            "\\end{figure}\n"
            "\\FloatBarrier\n")
            f.write(plots)
        # time.sleep(5)
    