from model.model import Model

modello_prova = Model()

#print(modello_prova.lista_attori)
#print(modello_prova.idMapActor.keys())

#ATTIVO IL GRAFO
modello_prova.build_grafo(7,10)
print(modello_prova.num_nodi())
print(modello_prova.num_archi())
#print(modello_prova.ex_crea_dizionario_idActor_idFIlm(7,10).keys())
#print(modello_prova.attore_grado_maggiore())
##print(modello_prova.attore_con_peso_maggiore())
#print(modello_prova.cinque_archi_peso_maggiore())
#lista = modello_prova.cinque_archi_peso_maggiore()
#for tupla in lista:
  #  print(f"------------------------ {tupla[0]}")
#print(modello_prova._grafo.nodes())
#print(modello_prova.attore_anziano())
print(modello_prova.attore_giovane())

attore1 = modello_prova.attore_giovane()
print(modello_prova.crea_albero(attore1,3))