import tkinter as tk
from tkinter import ttk, messagebox
import json

# Banco em memória (pode ser depois um SQLite ou salvar em JSON)
with open('links.json') as f:
    links_salvos = json.load(f)

# Função para adicionar URL
def salvar_link():
    url = entrada_url.get().strip()
    if url:
        if url not in links_salvos:
            links_salvos.append(url)
            with open('links.json', 'w') as f:
                json.dump(links_salvos, f)
            atualizar_tabela()
            entrada_url.delete(0, tk.END)  # Limpa o input
        else:
            messagebox.showinfo("Info", "Este link já foi adicionado.")
    else:
        messagebox.showwarning("Atenção", "Digite uma URL válida!")

# Atualiza a tabela de links
def atualizar_tabela():
    for row in tabela.get_children():
        tabela.delete(row)
    for idx, link in enumerate(links_salvos, start=1):
        tabela.insert("", "end", values=(idx, link))

# Criar a janela
root = tk.Tk()
root.title("Gerenciador de Links")
root.geometry("600x400")

# Frame para o input e botão
frame_top = tk.Frame(root)
frame_top.pack(pady=10)

# Input de URL
entrada_url = tk.Entry(frame_top, width=50)
entrada_url.pack(side=tk.LEFT, padx=(10, 5))

# Botão de salvar
botao_salvar = tk.Button(frame_top, text="Salvar", command=salvar_link)
botao_salvar.pack(side=tk.LEFT, padx=(5, 10))

# Tabela de links
colunas = ("#ID", "URL")
tabela = ttk.Treeview(root, columns=colunas, show="headings")
tabela.heading("#ID", text="ID")
tabela.heading("URL", text="URL")
tabela.column("#ID", width=50, anchor="center")
tabela.column("URL", width=500, anchor="w")
tabela.pack(expand=True, fill="both", pady=10)

for idx, link in enumerate(links_salvos, start=1):
    tabela.insert("", "end", values=(idx, link))

# Executa a janela
root.mainloop()
