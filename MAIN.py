import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import networkx as nx
import math
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['toolbar'] = 'None'

info = []  # Array dict para las actividades

sucesores = []  # array aux suscesores
predecesores = []  # array aux predecesores
lista_id = []  # revisar id repetidos

G = nx.DiGraph()  # Creación del grafo

def getStart():
    aux_node = dict(ID="Z", descripcion="Auxiliar de inicio", duracion=0,
                    predecesor=None, start_node=True, finish_node=False)
    cont = 0
    start_ID = ""

    while start_ID == "":
        for p in predecesores:
            # Cuenta cuántos nodos sin predecesor hay
            if p[1] == "":
                cont += 1

        if cont > 1:
            for i in range(len(predecesores)):
                # convierte el nodo auxiliar en la prelacion de los nodos sin prelacion
                if predecesores[i][1] == "":
                    predecesores[i] = (predecesores[i][0], "Z")
                    for d in info:
                        if d['ID'] == predecesores[i][0]:
                            d['predecesor'] = ["Z"]

            # agrega el nodo auxiliar a info
            info.insert(0, aux_node)
            # info.append(aux_node)
            start_ID = 'Z'

        elif cont <= 1:
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
    sucesores = []
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
    aux_node = dict(ID="X", descripcion="Auxiliar de inicio",
                    duracion=0, predecesor=[], start_node=False, finish_node=True)
    cont = 0
    end_ID = ""
    sucesores = create_sucesores(predecesores)

    while end_ID == "":
        for p in sucesores:
            # Cuenta cuántos nodos sin sucesor hay
            if len(p[1]) == 0:
                cont += 1

        if cont > 1:
            for i in range(len(sucesores)):
                # convierte el nodo auxiliar en el sucesor de los nodos sin sucesor
                if len(sucesores[i][1]) == 0:
                    sucesores[i] = (sucesores[i][0], ["X"])
                    # Se agrega los predecesores al nodo auxiliar
                    aux_node["predecesor"].append(sucesores[i][0])

            # agrega el nodo auxiliar a info
            info.append(aux_node)
            end_ID = "X"

        elif cont <= 1:
            for i in range(len(sucesores)):
                if len(sucesores[i][1]) == 0:
                    end_ID = sucesores[i][0]

            for j in range(len(info)):
                if info[j]["ID"] == end_ID:
                    info[j]["finish_node"] = True

        else:
            print('Error, no hay nodos sin sucesor')

    # print(sucesores)
    print(info)
    return end_ID


def agregar_nodo():  # validacion y agregar inputs a array info

    if id_input.get() in lista_id:  # validacion duplicado
        messagebox.showinfo(message="El ID esta duplicado", title="Error")
        return
    if not id_input.get().isalpha() or len(id_input.get()) > 1:  # validacion id invalido
        messagebox.showinfo(message="El ID es invalido", title="Error")
        return

    if not dur_input.get().isnumeric():  # validacion duracion invalida
        messagebox.showinfo(
            message="La duracion debe ser un numero", title="Error")
        return
    else:
        nuevo_nodo = dict(ID=id_input.get().upper(), descripcion=desc_input.get(), duracion=int(dur_input.get(
        )), predecesor=pred_input.get().upper().split(","), start_node=False, finish_node=False)  # crea dict

        if len(pred_input.get()) > 1:  # split para tabla predecesores
            temp = pred_input.get().split(",")
            for id in temp:
                if id not in lista_id:
                    messagebox.showinfo(
                        message='No existe el nodo '+id + ' en la red', title="Error")
                    return

            for id in temp:
                # append predecesores
                predecesores.append((id_input.get().upper(), id.upper()))
        else:
            # append predecesores

            if pred_input.get().upper() == '':
                predecesores.append(
                    (id_input.get().upper(), pred_input.get().upper()))
            elif pred_input.get().upper() not in lista_id:
                messagebox.showinfo(
                    message='No existe el nodo '+pred_input.get().upper() + ' en la red', title="Error")
                return
            else:
                predecesores.append(
                    (id_input.get().upper(), pred_input.get().upper()))
        info.append(nuevo_nodo)  # append en info
        # append para validacion de id duplicado
        lista_id.append(id_input.get().upper())
        
        success_text = tk.Label(root, text='La actividad ha sido agregada exitosamente.', font=('helvetica', 10))  # Texto de actividad agregada
        success_text.grid(pady = 8, row = 7, column = 0, columnspan = 2)

        # Se limpian los inputs
        id_input.delete(0, 'end')
        desc_input.delete(0, 'end')
        pred_input.delete(0, 'end')
        dur_input.delete(0, 'end')

        print(info)
        print(predecesores)


def generar_ruta():

    # Nodos de inicio
    start_node = getStart()
    finish_node = getFinish()
    print(info)

    for item in info:
        # Agregamos el nodo al grafo
        G.add_node(item['ID'], pos=(0, 0))

        # Asignamos atributos al nodo creado
        G.nodes[item['ID']]['ID'] = item['ID']
        G.nodes[item['ID']]['descripcion'] = item['descripcion']
        G.nodes[item['ID']]['start_node'] = item['start_node']
        G.nodes[item['ID']]['finish_node'] = item['finish_node']
        # Teniendo una lista de sucesores y predecesores por nodo, podemos aplicar ForwardPass y BacwardPass
        # en el algoritmo de la ruta crítica.
        print(item['predecesor'])
        G.nodes[item['ID']]['predecesor'] = item['predecesor']
        G.nodes[item['ID']]['sucesor'] = []

        # Asignamos los atributos que nos permitirán encontrar la ruta crítica
        # Corresponde a la duración de la actividad
        G.nodes[item['ID']]['D'] = item['duracion']
        # Corresponde al Early Start (Inicio más temprano)
        G.nodes[item['ID']]['ES'] = 0
        # Corresponde al Early Finish (Inicio más tardío)
        G.nodes[item['ID']]['EF'] = 0
        # Corresponde al Late Start (Culminación más temprana)
        G.nodes[item['ID']]['LS'] = 0
        # Corresponde al Late Finish (Culminación más tardía)
        G.nodes[item['ID']]['LF'] = math.inf
        # Corresponde a la Holgura de la actividad
        G.nodes[item['ID']]['H'] = 0
        G.nodes[item['ID']]['posx'] = 0
        G.nodes[item['ID']]['posy'] = 0

    # Se agregan las aristas al grafo y se crean los sucesores de cada nodo
    for node in G.nodes():
        if G.nodes[node]['predecesor'] != None:
            for predecesor in G.nodes[node]['predecesor']:
                G.add_edge(predecesor, node, weight=G.nodes[predecesor]['D'])
                # Al nodo predecesor le asignamos su sucesor
                G.nodes[predecesor]['sucesor'].append(G.nodes[node]['ID'])

    # Iniciamos el algoritmo de la ruta crítica

    # Primero aplicamos el ForwardPass, donde usaremos la lista de actividades sucesoras que hay en cada actividad
    for node in G.nodes():
        G.nodes[node]['EF'] = G.nodes[node]['ES'] + G.nodes[node]['D']

        for sucesor in list(G.nodes[node]['sucesor']):
            if G.nodes[node]['EF'] > G.nodes[sucesor]['ES']:
                G.nodes[sucesor]['ES'] = G.nodes[node]['EF']
                G.nodes[sucesor]['EF'] = G.nodes[sucesor]['ES'] + \
                    G.nodes[sucesor]['D']
        if G.nodes[node]['predecesor'] != None:
            for predecesor in list(G.nodes[node]['predecesor']):
                if G.nodes[predecesor]['EF'] > G.nodes[node]['ES']:
                    G.nodes[node]['ES'] = G.nodes[predecesor]['EF']
                    G.nodes[node]['EF'] = G.nodes[node]['ES'] + \
                        G.nodes[node]['D']

        if G.nodes[node]['finish_node'] == True:
            G.nodes[node]['LF'] = G.nodes[node]['EF']

    # Ahora aplicamos el BackwardPass, donde usaremos la lista de actividades predecesoras que hay en cada actividad
    while G.nodes[start_node]['start_node'] != False:

        for node in G.nodes():
            print(G.nodes[node]['ID'])
            if G.nodes[node]['finish_node'] == True:
                G.nodes[node]['LS'] = G.nodes[node]['LF'] - G.nodes[node]['D']
                print(G.nodes[node]['LS'], G.nodes[node]['ID'])
                G.nodes[node]['finish_node'] = False

                if G.nodes[node]['predecesor'] != None:
                    for predecesor in list(G.nodes[node]['predecesor']):
                        if G.nodes[node]['LS'] < G.nodes[predecesor]['LF']:
                            G.nodes[predecesor]['LF'] = G.nodes[node]['LS']
                            G.nodes[predecesor]['LS'] = G.nodes[predecesor]['LF'] - \
                                G.nodes[predecesor]['D']
                        G.nodes[predecesor]['finish_node'] = True

                if G.nodes[node] == G.nodes[start_node]:
                    if (G.nodes[node]['ID'] == 'Z'):
                        G.nodes[node]['LS'] = G.nodes[node]['ES']
                        G.nodes[node]['LF'] = G.nodes[node]['EF']

                    G.nodes[node]['start_node'] = False

    # Calculo de la holgura de cada actividad
    for node in G.nodes():
        G.nodes[node]['H'] = G.nodes[node]['LS'] - G.nodes[node]['ES']

    # Obtener camíno de la ruta crítica en orden
    critical_path = []
    inicio_CP = start_node
    critical_path.append(inicio_CP)

    while G.nodes[inicio_CP] != G.nodes[finish_node]:
        for sucesor in list(G.nodes[inicio_CP]['sucesor']):
            if G.nodes[sucesor]['H'] == 0:
                inicio_CP = G.nodes[sucesor]['ID']
                critical_path.append(inicio_CP)

    # <----------------------------------------- WINDOW POP UP ---------------->
    ax = plt.gca()

    def mostrar_grafo():
        G.nodes()
        color_map = []
        for node in G.nodes():
            G.nodes[node]['pos_asign'] = False
            if G.nodes[node]['H'] == 0:
                color_map.append(('#dcf763'))
            else:
                color_map.append(('#bfb7b6'))

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

                # Añadir detalles
                node_info = []
                node_info.append(['ES', G.nodes[sucesor]['ES']])
                node_info.append(['EF', G.nodes[sucesor]['EF']])
                node_info.append(['LS', G.nodes[sucesor]['LS']])
                node_info.append(['LF', G.nodes[sucesor]['LF']])
                node_info.append(['H', G.nodes[sucesor]['H']])
                node_info.append(['D', G.nodes[sucesor]['D']])
                
                annotation_text = '\n'.join(f'{info[0]}: {info[1]}' for info in node_info)
                ax.annotate(annotation_text, xy=(G.nodes[sucesor]['posx'], G.nodes[sucesor]['posy']), xytext=(-60, 40), textcoords='offset points', arrowprops=dict(arrowstyle="wedge", fc="#848c8e"), bbox=dict(boxstyle="round", fc="#f1f2ee"))

        # Obtener posición de los nodos del grafo
        pos = nx.get_node_attributes(G, 'pos')

        options_arrow = {
            'width': 2,
            'arrowstyle': '-|>',
            'arrowsize': 12,
        }

        # Configurar la forma de dibujar el grafo
        nx.draw_networkx_nodes(G, pos, node_color=color_map, node_size=500)
        nx.draw_networkx_edges(G, pos, alpha=0.6, edge_color='black', arrows=True, **options_arrow)
        nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')
        plt.box(False)
        plt.subplots_adjust(bottom=0, top=0.7)
        plt.show()


    def open_popup():
        top = Toplevel(root)
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('Treeview.Heading', background = '#dcf763')

        # Texto de tabla
        table_text = Label(top, text="Tabla", font=("verdana", 16, "bold"))
        table_text.grid(pady = 8, row = 0, column = 0, columnspan = 2)

        # Creación de tabla
        table_frame = Frame(top)
        table_frame.grid(pady = 16, padx = 8, row = 2, column = 0, columnspan = 2)
        table = ttk.Treeview(table_frame, column = ('id', 'desc', 'pred', 'suc', 'dur', 'es', 'ef', 'ls', 'lf', 'h'), show = 'headings', height = 8, selectmode = 'none')

        table.column('id', width = 60, anchor = CENTER)
        table.column('desc', width = 180, anchor = CENTER)
        table.column('pred', width = 120, anchor = CENTER)
        table.column('suc', width = 120, anchor = CENTER)
        table.column('dur', width = 60, anchor = CENTER)
        table.column('es', width = 60, anchor = CENTER)
        table.column('ef', width = 60, anchor = CENTER)
        table.column('ls', width = 60, anchor = CENTER)
        table.column('lf', width = 60, anchor = CENTER)
        table.column('h', width = 80, anchor = CENTER)

        table.heading('id', text='ID')
        table.heading('desc', text='Descripción')
        table.heading('pred', text='Predecesores')
        table.heading('suc', text='Sucesores')
        table.heading('dur', text='Duración')
        table.heading('es', text='ES')
        table.heading('ef', text='EF')
        table.heading('ls', text='LS')
        table.heading('lf', text='LF')
        table.heading('h', text='Holgura')

        table.pack()

        # Se inserta cada actividad en la tabla
        for node in G.nodes():
            if(G.nodes[node]['predecesor'] == None):
                activity_pred = '-'
            else:
                activity_pred = G.nodes[node]['predecesor']
            
            if(not G.nodes[node]['sucesor']):
                activity_suc = '-'
            else:
                activity_suc = G.nodes[node]['sucesor']

            table.insert('', 'end', values = (node, 
            G.nodes[node]['descripcion'], activity_pred, activity_suc, 
            G.nodes[node]['D'], G.nodes[node]['ES'], G.nodes[node]['EF'], G.nodes[node]['LS'], 
            G.nodes[node]['LF'], G.nodes[node]['H']))

        show_button = Button(top, bg='#848c8e', text="Mostrar Grafo", command=mostrar_grafo, font=("verdana", 12))
        show_button.grid(pady = 8, row = 3, column = 0, columnspan = 2)

    open_popup()

# <------------------------------- INICIALIZA LOS INPUTS Y BOTONES DE GRAFO Y DATA ----------------------------->
root = tk.Tk()

root.title("CPM")
root.geometry('+600+200')

# Título 
title = Label(root, text = "CPM", font=("Helvetica", 16, "bold"))
title.grid(pady = 8, row = 0, column = 0, columnspan = 10)

# Input de identificación
id_label = Label(root, text = "Ingrese ID: ", font=('helvetica', 10))
id_label.grid(padx = 8, pady = 4, row = 1, column = 0)

id_input = Entry(root)
id_input.grid(padx = 8, row = 1, column = 1)

# Input de descripción
desc_label = Label(root, text = "Ingrese la descripción: ", font=('helvetica', 10))
desc_label.grid(padx = 8, pady = 4, row = 2, column = 0)

desc_input = Entry(root)
desc_input.grid(padx = 8, row = 2, column = 1)

# Input de predecesores
pred_label = Label(root, text = "Ingrese los predecesores: ", font=('helvetica', 10))
pred_label.grid(padx = 8, pady = 4, row = 3, column = 0)

pred_input = Entry(root)
pred_input.grid(padx = 8, row = 3, column = 1)

# Input de duración
dur_label = Label(root, text = "Ingrese la duración: ", font=('helvetica', 10))
dur_label.grid(padx = 8, pady = 4, row = 4, column = 0)

dur_input = Entry(root)
dur_input.grid(padx = 8, row = 4, column = 1)

add_button = Button(text = "Agregar Actividad", width = 16, command = agregar_nodo, bg = '#848c8e', fg = 'black', font = ('helvetica', 12))
add_button.grid(pady = 8, row = 5, column = 0, columnspan = 2)

generate_button = Button(text= "Realizar CPM", width = 16, command = generar_ruta, bg = '#dcf763', fg= 'black', font = ('helvetica', 12))
generate_button.grid(pady = 4, row = 6, column = 0, columnspan = 2)

root.mainloop()