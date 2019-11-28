import busLineReaderStat
import json
import sys
import time

# Open enum
with open('jsons/enumLines.json') as linesFile:
    lines = json.load(linesFile)

#for i in range (0, 10):
#    for j in range (1, 107):
#        lineNumber = lines[str(j)]
#        for k in range (1, 5):
#            busLineReaderStat.read(lineNumber+"-"+str(k)+".jpg", lineNumber)
#            print "Interation: "+i+" - Line: "+lineNumber+" - Photo: "+k

statFile = open("stats/"+sys.argv[1]+".csv","w")
statFile.write('Resultado;Local/Cloud;Linha Encontrada;Linha Esperada;Metodo;Tempo\n')

busLineReaderStat.read('18-5.jpg', '18', statFile)

busLineReaderStat.read('60-1.jpg', '60', statFile)

busLineReaderStat.read('81-1.jpg', '81', statFile)

busLineReaderStat.read('77-1.jpg', '77', statFile)

busLineReaderStat.read('100-1.jpg', '100', statFile)
sys.exit(0)