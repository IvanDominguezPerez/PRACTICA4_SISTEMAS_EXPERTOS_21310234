import random
import tkinter as tk
from tkinter import messagebox

# Definimos los personajes, locaciones y armas
personajes = [
    {"nombre": "Carlos", "profesion": "Chef"},
    {"nombre": "Mariana", "profesion": "Doctora"},
    {"nombre": "Fernando", "profesion": "Detective"},
    {"nombre": "Lucia", "profesion": "Actriz"},
    {"nombre": "Ricardo", "profesion": "Empresario"}
]

locaciones = ["Casa", "Hotel", "Cocina", "Sala de Juegos", "Biblioteca"]
armas = ["Cuchillo", "Pistola", "Cuerda", "Veneno", "Tubo de Plomo"]

# Historias para cada asesinato
historias_casos = {
    "Carlos": [
        "Mariana estaba celosa de la fama culinaria de Carlos y decidió que era su momento de venganza.",
        "Fernando había descubierto un secreto oscuro de Carlos y temía que lo expusiera.",
        "Lucia odiaba a Carlos por un incidente público en el que él la avergonzó frente a todos.",
        "Ricardo perdió un negocio importante por culpa de Carlos y decidió que debía pagar por ello."
    ],
    "Mariana": [
        "Carlos estaba molesto con Mariana por difamar su restaurante con malas críticas.",
        "Fernando descubrió que Mariana estaba involucrada en actividades ilegales y quiso silenciarla.",
        "Lucia culpaba a Mariana por haberle arruinado un papel importante debido a una negligencia médica.",
        "Ricardo pensó que Mariana había traicionado su confianza en un acuerdo financiero importante."
    ],
    "Fernando": [
        "Carlos se sintió traicionado por Fernando cuando este decidió investigar sus actividades.",
        "Mariana pensó que Fernando estaba demasiado cerca de descubrir sus oscuros secretos.",
        "Lucia creía que Fernando estaba tratando de manipularla para obtener información personal.",
        "Ricardo estaba furioso porque Fernando había interferido en uno de sus tratos importantes."
    ],
    "Lucia": [
        "Carlos nunca perdonó a Lucia por robarle la receta secreta que le había dado fama.",
        "Mariana estaba celosa del éxito de Lucia y decidió acabar con su carrera de una vez por todas.",
        "Fernando descubrió que Lucia tenía conexiones con un criminal que él estaba investigando.",
        "Ricardo había perdido una gran suma de dinero por culpa de Lucia y su influencia en los medios."
    ],
    "Ricardo": [
        "Carlos estaba arruinado por las decisiones comerciales de Ricardo y quiso vengarse.",
        "Mariana perdió una inversión importante debido a las acciones de Ricardo y no pudo soportarlo más.",
        "Fernando descubrió que Ricardo estaba involucrado en negocios turbios y lo quería fuera del camino.",
        "Lucia quería vengarse de Ricardo por una traición amorosa que la dejó devastada."
    ]
}

# Historias para confirmación o negación de paraderos, ajustadas para dar sentido lógico
def generar_historias_paraderos(sospechosos, culpable_nombre):
    paraderos = []
    for sospechoso in sospechosos:
        if sospechoso["nombre"] == culpable_nombre:
            paraderos.append(f"Nadie puede confirmar el paradero de {sospechoso['nombre']} durante el crimen.")
        else:
            locacion_pista = random.choice(locaciones)
            paraderos.append(f"{sospechoso['nombre']} afirma que estaba en la {locacion_pista} durante el crimen.")
    return paraderos

# Función para iniciar una partida
def iniciar_partida():
    # Elegir al azar el caso en el que un personaje es asesinado
    asesinado = random.choice(personajes)
    sospechosos = [p for p in personajes if p != asesinado]
    culpable = random.choice(sospechosos)
    arma = random.choice(armas)
    locacion = random.choice(locaciones)

    # Guardar la solución
    solucion = {
        "culpable": culpable["nombre"],
        "arma": arma,
        "locacion": locacion,
        "asesinado": asesinado["nombre"]
    }
    
    historias = historias_casos[asesinado["nombre"]]
    paraderos = generar_historias_paraderos(sospechosos, culpable["nombre"])
    return solucion, sospechosos, historias, paraderos

# Función para hacer preguntas y obtener pistas
hacer_pregunta_intentos = 5

def hacer_pregunta(sospechosos, historias, paraderos, resultado_label, intentos_label):
    global hacer_pregunta_intentos

    def mostrar_resultado(texto):
        global hacer_pregunta_intentos
        resultado_label.config(text=texto)
        hacer_pregunta_intentos -= 1
        intentos_label.config(text=f"Intentos restantes: {hacer_pregunta_intentos}")
        if hacer_pregunta_intentos <= 0:
            messagebox.showinfo("Sin intentos", "Lo siento, se te han acabado los intentos.")

    def preguntar_que_hacian():
        resultado = "\n".join([f"{sospechoso['nombre']} ({sospechoso['profesion']}): {historias[i]}" for i, sospechoso in enumerate(sospechosos)])
        mostrar_resultado(resultado)

    def preguntar_donde_estaban():
        resultado = "\n".join([f"{sospechoso['nombre']} estaba en la {random.choice(locaciones)}." for sospechoso in sospechosos])
        mostrar_resultado(resultado)

    def preguntar_arma_cercana():
        resultado = "\n".join([f"Cerca de {sospechoso['nombre']} había un(a) {random.choice(armas)}." for sospechoso in sospechosos])
        mostrar_resultado(resultado)

    def confirmar_paradero():
        resultado = "\n".join(paraderos)
        mostrar_resultado(resultado)

    # Crear botones para opciones
    botones_frame = tk.Frame(root)
    botones_frame.pack(pady=10)

    tk.Button(botones_frame, text="Qué estaban haciendo", command=preguntar_que_hacian).pack(side=tk.LEFT, padx=5)
    tk.Button(botones_frame, text="Dónde estaban", command=preguntar_donde_estaban).pack(side=tk.LEFT, padx=5)
    tk.Button(botones_frame, text="Arma cercana", command=preguntar_arma_cercana).pack(side=tk.LEFT, padx=5)
    tk.Button(botones_frame, text="Confirmar paradero", command=confirmar_paradero).pack(side=tk.LEFT, padx=5)

# Función para manejar la acusación del jugador
def hacer_acusacion(solucion):
    def procesar_acusacion():
        sospechoso = sospechoso_entry.get()
        arma = arma_entry.get()
        locacion = locacion_entry.get()

        if sospechoso == solucion["culpable"] and arma == solucion["arma"] and locacion == solucion["locacion"]:
            messagebox.showinfo("Resultado", "¡Felicidades! Has resuelto el crimen correctamente.")
        else:
            messagebox.showinfo("Resultado", "La acusación es incorrecta. Sigue investigando.")
        acusacion_ventana.destroy()

    # Crear ventana de acusación
    acusacion_ventana = tk.Toplevel(root)
    acusacion_ventana.title("Hacer una acusación")

    tk.Label(acusacion_ventana, text="¿Quién es el culpable?").pack(pady=5)
    sospechoso_entry = tk.Entry(acusacion_ventana)
    sospechoso_entry.pack(pady=5)

    tk.Label(acusacion_ventana, text="¿Cuál fue el arma utilizada?").pack(pady=5)
    arma_entry = tk.Entry(acusacion_ventana)
    arma_entry.pack(pady=5)

    tk.Label(acusacion_ventana, text="¿Dónde ocurrió el crimen?").pack(pady=5)
    locacion_entry = tk.Entry(acusacion_ventana)
    locacion_entry.pack(pady=5)

    tk.Button(acusacion_ventana, text="Hacer acusación", command=procesar_acusacion).pack(pady=10)

# Función principal para jugar
def main():
    global root, hacer_pregunta_intentos
    root = tk.Tk()
    root.title("Simulador de Clue")

    def nueva_partida():
        global hacer_pregunta_intentos
        hacer_pregunta_intentos = 5

        for widget in root.winfo_children():
            widget.destroy()

        # Reiniciar etiquetas y componentes
        solucion, sospechosos, historias, paraderos = iniciar_partida()

        resultado_label = tk.Label(root, text=f"El asesinado es: {solucion['asesinado']}", justify=tk.LEFT, font=("Helvetica", 12))
        resultado_label.pack(pady=10)

        intentos_label = tk.Label(root, text=f"Intentos restantes: {hacer_pregunta_intentos}", font=("Helvetica", 12))
        intentos_label.pack(pady=5)

        hacer_pregunta(sospechosos, historias, paraderos, resultado_label, intentos_label)

        tk.Button(root, text="Hacer una acusación", command=lambda: hacer_acusacion(solucion)).pack(pady=10)
        tk.Button(root, text="Nueva partida", command=nueva_partida).pack(pady=10)

    nueva_partida()
    root.mainloop()

if __name__ == "__main__":
    main()
