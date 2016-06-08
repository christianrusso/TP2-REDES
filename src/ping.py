#! /usr/bin/env python
from scapy.all import *
from math import sqrt
import socket
import sys

MAX_TTL = 30
MSS = 1460
RWIN = 64

def estimateRTT_on_ping(host):
  ipdst = socket.gethostbyname(host)
  alphas = [0.15, 0.30, 0.50]
  ns = [10, 70, 150]

  # Inicialializo el dict con los resultados (n, alpha) => [(ertt_1, rtt_1), ..., (ertt_n, rtt_n)]
  estimatedRTT = dict()
  packetLossProb = dict()
  throughput = dict()

  for alpha in alphas:
    estimatedRTT[alpha] = dict()
    packetLossProb[alpha] = dict()
    throughput[alpha] = dict()
    for n in ns:
      estimatedRTT[alpha][n] = []
      packetLossProb[alpha][n] = 0
      throughput[alpha][n] = 0
    #endfor
  #endfor


  for n in ns:
    replies = 0

    # Envio los n paquetes echo-request
    for k in range(0, n):
      t0 = time.time()
      ans = sr1(IP(dst=ipdst, ttl=MAX_TTL) / ICMP(), timeout=2, verbose=0)
      rtt = (time.time() - t0) * 1000

      if (ans != None):
        replies += 1

        for alpha in alphas:
          if (replies > 1):
            prevERTT = estimatedRTT[alpha][n][-1][0]
          else:
            prevERTT = 0
          #endif
          eRTT = alpha * prevERTT + (1 - alpha) * rtt
          estimatedRTT[alpha][n].append((eRTT, rtt))
        #endfor
      #endif
    #endfor

    for alpha in alphas:
      PktLossProb = 1 - float(replies) / n
      packetLossProb[alpha][n] = PktLossProb
      RTT = estimatedRTT[alpha][n][-1][0]

      if (PktLossProb != 0):  # Si no es cero, uso la formula de Mathis: 1460/(rtt*sqrt(loss)) kbytes/s if rtt in ms
        throughput[alpha][n] = MSS / (RTT * sqrt(float(PktLossProb)))
      else:                   # Si es cero uso, ReceiveWindowSize / RTT kbytes/s if RWIN in kbytes
        throughput[alpha][n] = (RWIN / float(RTT)) * 1000
    #endfor
  #endfor

  # Imprimo los resultados
  for n in ns:
    for alpha in alphas:
      print "ERTT\tRTT"
      for ertt, rtt in estimatedRTT[alpha][n]:
        print "%.2f\t%.2f" % (ertt, rtt)
      print "PktLossProb para alpha: %s y n: %s = %s" % (alpha, n, packetLossProb[alpha][n])
      print "Throughput para alpha: %s y n: %s = %s" % (alpha, n, throughput[alpha][n])
      print "-----------------"

if __name__ == '__main__':
    host_destino = sys.argv[1]
    estimateRTT_on_ping(host_destino)
