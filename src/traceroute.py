#! /usr/bin/env python
from scapy.all import *
import math
import socket
import time

PKT_ICMP = 3
MAX_HOPS = 30

def TraceRoute(hostDestino):

  destino = socket.gethostbyname(hostDestino)
  ttl_i = 1
  rtt = []
  llegoDestino = False
  ruta = []

  while (not llegoDestino and ttl_i <= MAX_HOPS):	# Itero hasta llegar al host destino o hasta alcanzar la cota de hops
    rtt.append(0)
    resp = 0
    hops = dict()

    for i in range (0, PKT_ICMP): # Envio PKT_ICMP paquetes por TTL
      t0 = time.time()
      ans = sr1(IP(dst=destino, ttl = ttl_i) / ICMP(), timeout=2, verbose=0) #timeout en segundos
      rtt_i = time.time() - t0

      if (ans != None):
        rtt[ttl_i - 1] += (rtt_i * 1000)
        resp += 1
        if ans.src in hops:
          hops[ans.src] += 1
        else:
          hops[ans.src] = 1
        #endif
      #endif

      if (ans != None and ans.src == destino): # Termino cuando recibo una respuesta del host destino
        llegoDestino = True
      #endif
    #endfor

    if (resp > 0):
      rtt[ttl_i - 1] /= resp # Promedio de los RTT obtenidos para el ttl_i (no diferencia que hop responde)
    #end if

    # Determino el i-esimo hop de la ruta general
    hopRuta = "*"

    for hop in hops:
      if (hopRuta == "*" or hops[hop] > hops[hopRuta]):
        hopRuta = hop

    if (hopRuta != "*"):
      ruta.append((hopRuta, hops[hopRuta]))
    else:
      ruta.append((hopRuta, 0))

    ttl_i += 1

  #endwhile

  totalHops = ttl_i

  # Calculo del RTT promedio
  prom = 0
  for rtt_i in rtt:
    prom += rtt_i

  prom /= totalHops

  # Calculo del Desvio estandar
  desvio = 0
  for rtt_i in rtt:
    desvio += (rtt_i * rtt_i) - prom

  desvio /= totalHops
  desvio = math.sqrt(desvio)

  # Calculo los ZRTT
  zrtt = []
  for rtt_i in rtt:
    zrtt.append((rtt_i - prom) / desvio)

  # Imprimo el traceroute
  print "Destino: %s @ %s" % (hostDestino, destino)
  print "TTL\tRTT\tZRTT\t%Resp\tHOP"
  for ttl in range(0, len(ruta)):
    if (ruta[ttl] == "*"):
      print "%s\t*\t*\t0\t*" % (ttl + 1)
    else:
      print "%s\t%.2f\t%.2f\t%.1f\t%s" % (ttl + 1, rtt[ttl], zrtt[ttl], ruta[ttl][1] / float(PKT_ICMP) * 100, ruta[ttl][0])

  # Armo array de resultados (ip_i, rtt_i, zrtt_i)
  res = []
  for ttl in range(0, len(ruta)):
    if (ruta[ttl][0] != "*"):
      res.append((ruta[ttl][0], rtt[ttl], zrtt[ttl]))

  return res

if __name__ == '__main__':
  host_destino = sys.argv[1]
  TraceRoute(host_destino)
