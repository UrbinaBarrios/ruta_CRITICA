import tkinter as tk
from tkinter import *
from tkinter import messagebox
import networkx as nx
import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt

info = [] #Array dict para las actividades


sucesores =[] #array aux suscesores
predecesores = [] #array aux predecesores
lista_id = [] #revisar id repetidos

G = nx.DiGraph() # Creación del grafo


	# <------------------------------- INICIALIZA LOS INPUTS Y BOTONES DE GRAFO Y DATA ----------------------------->
root= tk.Tk()

canvas1 = tk.Canvas(root, width=400, height=400, relief='raised')
canvas1.pack()

label1 = tk.Label(root, text='Camino de rutas crtíticas')
label1.config(font=('helvetica', 14))
canvas1.create_window(200, 25, window=label1)

label2 = tk.Label(root, text='Ingrese la identificacion:')
label2.config(font=('helvetica', 10))
canvas1.create_window(100, 75, window=label2)

entry1 = tk.Entry(root) 
canvas1.create_window(250, 75, window=entry1)

label3 = tk.Label(root, text='Ingrese la descripción:')
label3.config(font=('helvetica', 10))
canvas1.create_window(100, 125, window=label3)

entry2 = tk.Entry(root) 
canvas1.create_window(250, 125, window=entry2)

label4 = tk.Label(root, text='Ingrese los predecesores:')
label4.config(font=('helvetica', 10))
canvas1.create_window(100, 175, window=label4)

entry3 = tk.Entry(root) 
canvas1.create_window(250, 175, window=entry3)

label5 = tk.Label(root, text='Ingrese la duración:')
label5.config(font=('helvetica', 10))
canvas1.create_window(100, 225, window=label5)

entry4 = tk.Entry(root) 
canvas1.create_window(250, 225, window=entry4)


def getStart():
    aux_node = dict( ID = "Z", descripcion = "Auxiliar de inicio", duracion = 0, predecesor = None, start_node = True, finish_node = False)
    cont = 0
    start_ID=""

    while start_ID =="":
        for p in predecesores:
            #Cuenta cuántos nodos sin predecesor hay
            if p[1] == "":
                cont+=1
        
        if cont > 1:
            for i in range(len(predecesores)):
                #convierte el nodo auxiliar en la prelacion de los nodos sin prelacion
                if predecesores[i][1] == "":
                    predecesores[i]= (predecesores[i][0], "Z")
                    for d in info:
                        if d['ID'] == predecesores[i][0]:
                            d['predecesor'] = ["Z"]
            
            #agrega el nodo auxiliar a info
            info.append(aux_node)
            start_ID = 'Z'
        
        elif cont <=1:
            for i in range(len(predecesores)):
                if predecesores[i][1] == "":
                    start_ID = predecesores[i][0]

            for j in range(len(info)):
                if info[j]["ID"] == start_ID:
                    info[j]["start_node"] = True
                    info[j]["predecesor"] = None

        else:
            print('Error, no hay nodos sin prelación')
    

    return start_ID

def create_sucesores(predecesores):
    sucesores =[]
    ids = []
    for p in predecesores:
        ids.append(p[0])

    ids = list(dict.fromkeys(ids))
    for id in ids:
            sucesores.append((id, []))

    for tup in predecesores:
        for i in range(len(sucesores)):
            if not tup[1] == "":
                if tup[1] == sucesores[i][0]:
                    sucesores[i][1].append(tup[0])

    return sucesores

def getFinish():
    aux_node = dict( ID = "X", descripcion = "Auxiliar de inicio", duracion = 0, start_node= False, finish_node = True )
    cont = 0
    end_ID=""
    sucesores = create_sucesores(predecesores)


    while end_ID =="":
        for p in sucesores:
            #Cuenta cuántos nodos sin sucesor hay
            if len(p[1]) == 0:
                cont+=1
        
        if cont > 1:
            for i in range(len(sucesores)):
                #convierte el nodo auxiliar en el sucesor de los nodos sin sucesor
                if len(sucesores[i][1]) == 0:
                    sucesores[i]= (sucesores[i][0], ["X"])
            
            #agrega el nodo auxiliar a info
            info.append(aux_node)
            end_ID = "X"
        
        elif cont <=1:
            for i in range(len(sucesores)):
                if len(sucesores[i][1]) == 0:
                    end_ID = sucesores[i][0]

            for j in range(len(info)):
                if info[j]["ID"] == end_ID:
                    info[j]["finish_node"] = True

        else:
            print('Error, no hay nodos sin sucesor')
    
    print(sucesores)
    return end_ID

def agregar_nodo(): #validacion y agregar inputs a array info
    
    if entry1.get() in lista_id: #validacion duplicado
        messagebox.showinfo(message="El ID esta duplicado", title="Error")
        return
    if not entry1.get().isalpha() or len(entry1.get()) > 1: #validacion id invalido
        messagebox.showinfo(message="El ID es invalido", title="Error")
        return 
    if not entry4.get().isnumeric(): #validacion duracion invalida 
        messagebox.showinfo(message="La duracion debe ser un numero", title="Error")
        return         
    else:
        nuevo_nodo = dict( ID = entry1.get().upper(), descripcion = entry2.get(), duracion = int(entry4.get()), predecesor = entry3.get().upper().split(","), start_node = False, finish_node = False) #crea dict
        info.append(nuevo_nodo) #append en info
        lista_id.append(entry1.get().upper()) #append para validacion de id duplicado
        if len(entry3.get()) > 1: #split para tabla predecesores
            temp = entry3.get().split(",")
            for id in temp:
                predecesores.append((entry1.get().upper(),id.upper())) #append predecesores 
        else:
            predecesores.append((entry1.get().upper(),entry3.get().upper())) #append predecesores
        
        label3 = tk.Label(root, text='Actividad agregada', font=('helvetica', 10)) #label actividad agregada 
        canvas1.create_window(200, 350, window=label3)

        print(info)
        print(predecesores)

        
def generar_ruta():  

    
    #Nodos de inicio
    start_node = getStart()
    finish_node = getFinish()
    print(info)

    for item in info:
        # Agregamos el nodo al grafo
        G.add_node(item['ID'], pos=(0,0))

        # Asignamos atributos al nodo creado
        G.nodes[item['ID']]['ID'] = item['ID']
        G.nodes[item['ID']]['descripcion'] = item['descripcion']
        G.nodes[item['ID']]['start_node'] = item['start_node']
        G.nodes[item['ID']]['finish_node'] = item['finish_node']
		# Teniendo una lista de sucesores y predecesores por nodo, podemos aplicar ForwardPass y BacwardPass
		# en el algoritmo de la ruta crítica.
        G.nodes[item['ID']]['predecesor'] = item['predecesor']
        G.nodes[item['ID']]['sucesor'] = []

        # Asignamos los atributos que nos permitirán encontrar la ruta crítica
        G.nodes[item['ID']]['D'] = item['duracion'] # Corresponde a la duración de la actividad
        G.nodes[item['ID']]['ES'] = 0 # Corresponde al Early Start (Inicio más temprano)
        G.nodes[item['ID']]['EF'] = 0 # Corresponde al Early Finish (Inicio más tardío)
        G.nodes[item['ID']]['LS'] = 0 # Corresponde al Late Start (Culminación más temprana)
        G.nodes[item['ID']]['LF'] = math.inf # Corresponde al Late Finish (Culminación más tardía)
        G.nodes[item['ID']]['H'] = 0 # Corresponde a la Holgura de la actividad
        G.nodes[item['ID']]['posx'] = 0
        G.nodes[item['ID']]['posy'] = 0
    
    # Se agregan las aristas al grafo y se crean los sucesores de cada nodo
    for node in G.nodes():
        if G.nodes[node]['predecesor'] != None:
            for predecesor in G.nodes[node]['predecesor']:
               G.add_edge(predecesor, node, weight = G.nodes[predecesor]['D'])
                # Al nodo predecesor le asignamos su sucesor
               G.nodes[predecesor]['sucesor'].append(G.nodes[node]['ID'])

	# Iniciamos el algoritmo de la ruta crítica
    
    # Primero aplicamos el ForwardPass, donde usaremos la lista de actividades sucesoras que hay en cada actividad
    for node in G.nodes():
        G.nodes[node]['EF'] = G.nodes[node]['ES'] + G.nodes[node]['D']

        for sucesor in list(G.nodes[node]['sucesor']):
            if G.nodes[node]['EF'] > G.nodes[sucesor]['ES']:
                G.nodes[sucesor]['ES'] = G.nodes[node]['EF']
                G.nodes[sucesor]['EF'] = G.nodes[sucesor]['ES'] + G.nodes[sucesor]['D']
        if G.nodes[node]['predecesor'] != None:
            for predecesor in list(G.nodes[node]['predecesor']):
                if G.nodes[predecesor]['EF'] > G.nodes[node]['ES']:
                    G.nodes[node]['ES'] = G.nodes[predecesor]['EF']
                    G.nodes[node]['EF'] = G.nodes[node]['ES'] + G.nodes[node]['D']

        if G.nodes[node]['finish_node'] == True:
            G.nodes[node]['LF'] = G.nodes[node]['EF']

    #Ahora aplicamos el BackwardPass, donde usaremos la lista de actividades predecesoras que hay en cada actividad           
    while G.nodes[start_node]['start_node'] != False:

        for node in G.nodes():
            if G.nodes[node]['finish_node'] == True:
                G.nodes[node]['LS'] = G.nodes[node]['LF'] - G.nodes[node]['D']
                G.nodes[node]['finish_node'] = False
                
                if G.nodes[node]['predecesor'] != None:
                    for predecesor in list(G.nodes[node]['predecesor']):
                        if G.nodes[node]['LS'] < G.nodes[predecesor]['LF']:
                            G.nodes[predecesor]['LF'] = G.nodes[node]['LS']
                            G.nodes[predecesor]['LS'] = G.nodes[predecesor]['LF'] - G.nodes[predecesor]['D']
                        G.nodes[predecesor]['finish_node'] = True

                        
                       
                if  G.nodes[node] == G.nodes[start_node]:
                    G.nodes[node]['start_node'] = False
    
    # Calculo de la holgura de cada actividad
    for node in G.nodes():
        G.nodes[node]['H'] = G.nodes[node]['LS'] - G.nodes[node]['ES']

    #Obtener camíno de la ruta crítica en orden
    critical_path = []
    inicio_CP = start_node
    critical_path.append(inicio_CP)

    while G.nodes[inicio_CP] != G.nodes[finish_node]:
        for sucesor in list(G.nodes[inicio_CP]['sucesor']):
            if G.nodes[sucesor]['H'] == 0:
                inicio_CP = G.nodes[sucesor]['ID']
                critical_path.append(inicio_CP)
    # <----------------------------------------- WINDOW POP UP ---------------->
    def mostrar_grafo():
        color_map = []
        for node in G.nodes():
            G.nodes[node]['pos_asign'] = False
            if G.nodes[node]['H'] == 0:
                color_map.append(('#fe2f65'))
            else:
                color_map.append(('#39b5f0'))

        # Establecer posición de los nodos
        for node in G.nodes():
            if G.nodes[node] == start_node:
                G.nodes[node]['pos_asign'] = True
            acum_y = 0
            for sucesor in list(G.nodes[node]['sucesor']):
                if G.nodes[sucesor]['pos_asign'] == False:
                    G.nodes[sucesor]['posx'] = G.nodes[node]['posx'] + 2
                    G.nodes[sucesor]['posy'] = G.nodes[node]['posy'] - acum_y
                    G.nodes[sucesor]['pos'] = (G.nodes[sucesor]['posx'], G.nodes[sucesor]['posy'])
                    acum_y = acum_y + 0.5
                    G.nodes[sucesor]['pos_asign'] = True


        # Obtener posición de los nodos del grafo
        pos = nx.get_node_attributes(G,'pos')

        options_arrow = {
            'width': 2,
            'arrowstyle': '-|>',
            'arrowsize': 12,
        }

        dias = []
        for i in range(G.nodes[start_node]['ES'], G.nodes[finish_node]['EF']):
            dia = 'día ' + str(i)
            dias.append(dia)

        mapeado = range(len(dias))

        # Configurar la forma de dibujar el grafo
        nx.draw_networkx_nodes(G, pos, node_color = color_map, node_size=500)
        nx.draw_networkx_edges(G, pos, alpha=0.6, edge_color='black', arrows=True, **options_arrow)
        nx.draw_networkx_labels(G, pos, font_size=6, font_family='sans-serif')
        plt.xticks(mapeado, dias) 
        plt.title('Actividades de la Ruta Crítica (Nodos en Rojo)')
        plt.show()
    def open_popup():
        top = Toplevel(root)
        top.geometry("1024x600")
            # Título del Reporte
        label_act = tk.Label(top, fg="#a60338", text="Reporte de Actividades", font=("verdana", 12)).place(x=190, y=15)

        # LEYENDA
        terminos = tk.Label(top, fg="#a60338", text="Terminos usados en el reporte", font=("verdana", 10)).place(x=790, y=70)
        termino_D = tk.Label(top, fg="#2d2da7", text="D: Duración", font=("verdana", 10)).place(x=790, y=100)
        termino_ES = tk.Label(top, fg="#2d2da7", text="ES:", font=("verdana", 10)).place(x=790, y=130)
        termino_ES1 = tk.Label(top, fg="#2d2da7", text="Early Start (Inicio más temprano)", font=("verdana", 7)).place(x=820, y=130)
        termino_EF = tk.Label(top, fg="#2d2da7", text="EF:", font=("verdana", 10)).place(x=790, y=160)
        termino_EF1 = tk.Label(top, fg="#2d2da7", text="Early Finish (Inicio más tardío)", font=("verdana", 7)).place(x=820, y=160)
        termino_LS = tk.Label(top, fg="#2d2da7", text="LS:", font=("verdana", 10)).place(x=790, y=190)
        termino_LS1 = tk.Label(top, fg="#2d2da7", text="Late Start (Culminación más temprana)", font=("verdana", 7)).place(x=820, y=190)
        termino_LF = tk.Label(top, fg="#2d2da7", text="LF:", font=("verdana", 10)).place(x=790, y=220)
        termino_LF1 = tk.Label(top, fg="#2d2da7", text="Late Finish (Culminación más tardía)", font=("verdana", 7)).place(x=820, y=220)
        termino_H = tk.Label(top, fg="#2d2da7", text="H: Holgura", font=("verdana", 10)).place(x=790, y=250)


        # TABLA DE REPORTE
        label_act = tk.Label(top, fg="#2d2da7", text="| Actividad", font=("verdana", 10)).place(x=20, y=50)
        label_des = tk.Label(top, fg="#2d2da7", text="| Descripción", font=("verdana", 10)).place(x=100, y=50)
        label_pre = tk.Label(top, fg="#2d2da7", text="| Predecesor", font=("verdana", 10)).place(x=220, y=50)
        label_suc = tk.Label(top, fg="#2d2da7", text="| Sucesor", font=("verdana", 10)).place(x=320, y=50)
        label_D = tk.Label(top, fg="#2d2da7", text="| D", font=("verdana", 10)).place(x=420, y=50)
        label_ES = tk.Label(top, fg="#2d2da7", text="| ES", font=("verdana", 10)).place(x=480, y=50)
        label_EF = tk.Label(top, fg="#2d2da7", text="| EF", font=("verdana", 10)).place(x=540, y=50)
        label_LS = tk.Label(top, fg="#2d2da7", text="| LS", font=("verdana", 10)).place(x=600, y=50)
        label_LF = tk.Label(top, fg="#2d2da7", text="| LF", font=("verdana", 10)).place(x=660, y=50)
        label_H = tk.Label(top, fg="#2d2da7", text="| H", font=("verdana", 10)).place(x=720, y=50)


        # Cada registro completa de cada actividad
        pos_y = 50
        aux_predecesor =  {}
        aux_sucesor = {}
        for node in G.nodes():
            pos_y += 50
            if G.nodes[node]['predecesor'] == None:
                aux_predecesor = '--'
            else:
                aux_predecesor = str(G.nodes[node]['predecesor'])
            if len(G.nodes[node]['sucesor']) == 0:
                aux_sucesor = '--'
            else:
                aux_sucesor = str(G.nodes[node]['sucesor'])

            tk.Label(top, fg="#292931", text="| " + str(node), font=("verdana", 10)).place(x=20, y=pos_y)
            tk.Label(top, fg="#292931", text="| " + str(G.nodes[node]['descripcion']), font=("verdana", 7)).place(x=100, y=pos_y)
            tk.Label(top, fg="#292931", text="| " + aux_predecesor, font=("verdana", 10)).place(x=220, y=pos_y)
            tk.Label(top, fg="#292931", text="| " + aux_sucesor, font=("verdana", 10)).place(x=320, y=pos_y)
            tk.Label(top, fg="#292931", text="| " + str(G.nodes[node]['D']) + " días", font=("verdana", 10)).place(x=420, y=pos_y)
            tk.Label(top, fg="#292931", text="| " + str(G.nodes[node]['ES']) + " días", font=("verdana", 10)).place(x=480, y=pos_y)
            tk.Label(top, fg="#292931", text="| " + str(G.nodes[node]['EF']) + " días", font=("verdana", 10)).place(x=540, y=pos_y)
            tk.Label(top, fg="#292931", text="| " + str(G.nodes[node]['LS']) + " días", font=("verdana", 10)).place(x=600, y=pos_y)
            tk.Label(top, fg="#292931", text="| " + str(G.nodes[node]['LF']) + " días", font=("verdana", 10)).place(x=660, y=pos_y)
            tk.Label(top, fg="#292931", text="| " + str(G.nodes[node]['H']) + " días", font=("verdana", 10)).place(x=720, y=pos_y)
            
        pos_y += 50
        btn_mostrar_grafo_CP = tk.Button(top, bg='#d15b70', text="Mostrar Grafo de la Ruta Crítica", command = mostrar_grafo, font=("verdana", 10)).place(x=780, y=500)

    open_popup()


button1 = tk.Button(text='Agregar', command=agregar_nodo, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(100, 300, window=button1)

button2 = tk.Button(text='Generar ruta critica', command=generar_ruta, bg='blue', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(200, 300, window=button2)           


root.mainloop()