import busLineReaderStat
import json
import sys

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
busLineReaderStat.read('ufscar-laranja-lado.jpg', '80', statFile)
busLineReaderStat.read('expresso-frente-laranja.jpg', '100', statFile)
busLineReaderStat.read('maria-eugenia-laranja-frente-3.jpg', '59', statFile)
sys.exit(0)