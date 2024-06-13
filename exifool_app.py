import tkinter as tk  # Importa o módulo tkinter para criar interfaces gráficas
from tkinter import filedialog, messagebox  # Importa funções específicas do tkinter para diálogos de arquivos e mensagens
import subprocess  # Importa o módulo subprocess para executar comandos externos
import os  # Importa o módulo os para manipulação de caminhos de arquivos e diretórios

def select_folder():
    # Abre um diálogo para o usuário selecionar uma pasta e retorna o caminho da pasta selecionada
    folder_path = filedialog.askdirectory()
    if folder_path:
        # Se uma pasta foi selecionada, atualiza o campo de entrada com o caminho da pasta
        folder_entry.delete(0, tk.END)  # Limpa o campo de entrada
        folder_entry.insert(0, folder_path)  # Insere o caminho da pasta no campo de entrada

def extract_metadata():
    # Obtém o caminho da pasta do campo de entrada
    folder_path = folder_entry.get()
    if not folder_path:
        # Exibe uma mensagem de aviso se nenhuma pasta foi selecionada
        messagebox.showwarning("Cuidado", "Não Escolheu Pasta!")
        return
    
    if not os.path.isdir(folder_path):
        # Exibe uma mensagem de erro se o caminho selecionado não é uma pasta válida
        messagebox.showerror("Erro", "Pasta escolhida Não Existe!")
        return

    combined_metadata = ""  # Inicializa uma string para armazenar os metadados combinados
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)  # Obtém o caminho completo do arquivo
            try:
                # Executa o comando exiftool para extrair os metadados do arquivo
                result = subprocess.run(['exiftool', file_path], capture_output=True, text=True, check=True)
                # Adiciona os metadados extraídos à string combined_metadata
                combined_metadata += f"File: {file_path}\n{result.stdout}\n\n"
            except subprocess.CalledProcessError as e:
                # Exibe uma mensagem de erro se houver um problema ao executar o exiftool
                messagebox.showerror("Erro", f"Erro Executar ExifTool {file_path}: {e}")

    if combined_metadata:
        # Se metadados foram extraídos, chama a função save_metadata para salvar os metadados
        save_metadata(combined_metadata)
        # Limpa o campo de entrada da pasta
        folder_entry.delete(0, tk.END)
    else:
        # Exibe uma mensagem informativa se nenhum metadado foi extraído
        messagebox.showinfo("Aviso", "Não metadata extraido.")

def save_metadata(metadata):
    # Abre um diálogo para o usuário selecionar onde salvar os metadados extraídos
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if save_path:
        # Se um caminho de salvamento foi selecionado, escreve os metadados no arquivo
        with open(save_path, 'w') as f:
            f.write(metadata)
        # Exibe uma mensagem de sucesso após salvar os metadados
        messagebox.showinfo("Sucesso", f"Metadata Salvo Para {save_path}")

# Configuração da janela principal
root = tk.Tk()  # Cria a janela principal
root.title("App MetaDados")  # Define o título da janela
root.geometry("600x350")  # Define o tamanho da janela

# Frame para seleção de pasta
frame = tk.Frame(root)  # Cria um frame dentro da janela principal
frame.pack(pady=20)  # Adiciona um padding ao redor do frame

folder_label = tk.Label(frame, text="Escolhe Uma Pasta:")  # Cria um rótulo para o campo de seleção de pasta
folder_label.pack(side=tk.LEFT, padx=5)  # Adiciona o rótulo ao frame com um padding lateral

folder_entry = tk.Entry(frame, width=40)  # Cria um campo de entrada para o caminho da pasta
folder_entry.pack(side=tk.LEFT, padx=5)  # Adiciona o campo de entrada ao frame com um padding lateral

folder_button = tk.Button(frame, text="Pesquisa", command=select_folder)  # Cria um botão para abrir o diálogo de seleção de pasta
folder_button.pack(side=tk.LEFT, padx=5)  # Adiciona o botão ao frame com um padding lateral

# Botão para extrair metadados
extract_button = tk.Button(root, text="Executar Metadata", command=extract_metadata)  # Cria um botão para iniciar a extração de metadados
extract_button.pack(pady=20)  # Adiciona o botão à janela principal com um padding vertical

root.mainloop()  # Inicia o loop principal da interface gráfica
