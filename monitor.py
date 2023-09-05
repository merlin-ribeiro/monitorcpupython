import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import psutil
import os
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Função para atualizar os dados da CPU e armazenamento
def atualizar_dados():
    try:
        # Obter informações da CPU
        uso_cpu = psutil.cpu_percent(interval=1)
        label_cpu.config(text=f"Uso da CPU: {uso_cpu:.1f}%", image=cpu_icon)

        # Atualizar gráfico da CPU
        atualizar_grafico_cpu(uso_cpu)

        # Obter informações sobre o armazenamento de todas as partições
        particoes = psutil.disk_partitions()
        for i, particao in enumerate(particoes):
            uso_armazenamento = psutil.disk_usage(particao.mountpoint)
            espaco_usado_gb = uso_armazenamento.used / (1024 ** 3)  # Converter para GB
            espaco_total_gb = uso_armazenamento.total / (1024 ** 3)  # Converter para GB
            label_armazenamento[i].config(
                text=f"Partição {i + 1}: {espaco_usado_gb:.2f}GB / {espaco_total_gb:.2f}GB"
            )
            barra_armazenamento[i]["value"] = (espaco_usado_gb / espaco_total_gb) * 100

        # Agendar a próxima atualização
        root.after(1000, atualizar_dados)
    except KeyboardInterrupt:
        # Lidar com a interrupção manual (Ctrl+C)
        pass

# Função para atualizar o gráfico de uso de CPU
def atualizar_grafico_cpu(uso_cpu):
    dados.append(uso_cpu)
    if len(dados) > 50:
        dados.pop(0)  # Remover os dados mais antigos
    ax.clear()
    ax.plot(range(len(dados)), dados, color='b')
    ax.set_ylim(0, 100)
    ax.set_ylabel('Uso da CPU (%)')
    ax.set_xlabel('Tempo (s)')
    canvas.draw()

# Configuração da janela principal
root = tk.Tk()
root.title("Monitor de CPU e Armazenamento")
root.geometry("800x400")  # Tamanho personalizado da janela

# Ícone da CPU
cpu_image = Image.open("img/cpu_icon.png")
cpu_image = cpu_image.resize((50, 50))
cpu_icon = ImageTk.PhotoImage(cpu_image)

# Rótulo de CPU
label_cpu = ttk.Label(root, text="", font=("Helvetica", 12))
label_cpu.pack()

# Bloco de uso de CPU com gráfico
frame_cpu = ttk.Frame(root)
frame_cpu.pack(fill="both", expand=True, padx=10, pady=10)

# Configurar o gráfico da CPU
fig, ax = plt.subplots(figsize=(6, 2), dpi=80)
canvas = FigureCanvasTkAgg(fig, master=frame_cpu)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill="both", expand=True)
dados = [0] * 50  # Inicializar com 50 pontos zero

# Blocos de armazenamento
frame_armazenamento = ttk.Frame(root)
frame_armazenamento.pack(fill="both", expand=True, padx=10, pady=10)
label_armazenamento = []
barra_armazenamento = []
particoes = psutil.disk_partitions()
for i, particao in enumerate(particoes):
    frame = ttk.Frame(frame_armazenamento)
    frame.pack(fill="x")
    label = ttk.Label(frame, text="", font=("Helvetica", 12))
    label.pack(side="left")
    label_armazenamento.append(label)

    barra = ttk.Progressbar(frame, orient="horizontal", length=200, mode="determinate")
    barra.pack(side="right")
    barra_armazenamento.append(barra)

# Iniciar a atualização dos dados
atualizar_dados()

# Iniciar a interface gráfica
root.mainloop()
