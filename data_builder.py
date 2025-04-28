import os
import pathlib
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import json

# Caminho da pasta de imagens
IMAGES_FOLDER = './imgs'

# Banco de dados fake (JSON em memória)
if os.path.exists('data/data.json'):
    with open('data/data.json', 'r') as f:
        fake_db = json.load(f)
else:
    fake_db = {
        "PageData": {}
    }

# Função para carregar imagens da pasta
def load_images(folder):
    image_paths = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                image_paths.append(os.path.join(root, file))
    return image_paths

# Função para salvar dados no "banco"
def save_to_album(image_path, album_name):
    # Garante que a coleção exista
    if album_name not in fake_db["PageData"]:
        fake_db["PageData"][album_name] = []
    
    # Salva o documento (como {filename: filepath})
    document = {os.path.basename(image_path): image_path}
    fake_db["PageData"][album_name].append(document)
    messagebox.showinfo("Salvo", f"Imagem salva no álbum '{album_name}'!")
    print(json.dumps(fake_db, indent=2))  # Exibe no console para ver
    data = pathlib.Path('data')
    data.mkdir(exist_ok=True)
    with open(data / 'data.json', 'w') as f:
        json.dump(fake_db, f, indent=2)

# Função para criar um novo álbum
def create_new_album():
    album_name = simpledialog.askstring("Novo Álbum", "Digite o nome do novo álbum:")
    if album_name:
        if album_name not in fake_db["PageData"]:
            fake_db["PageData"][album_name] = []
            album_combobox['values'] = list(fake_db["PageData"].keys())
            album_combobox.set(album_name)  # Define o álbum recém-criado como selecionado
            messagebox.showinfo("Álbum Criado", f"Álbum '{album_name}' criado com sucesso!")
        else:
            messagebox.showwarning("Álbum Existente", f"O álbum '{album_name}' já existe!")

# Funções de navegação
def show_image(index):
    global img_label, img_tk
    if 0 <= index < len(images):
        img = Image.open(images[index])
        img = img.resize((400, 400))  # Redimensiona para caber na janela
        img_tk = ImageTk.PhotoImage(img)
        img_label.config(image=img_tk)
        img_label.image = img_tk

def next_image():
    global current_index
    if current_index < len(images) - 1:
        current_index += 1
        show_image(current_index)

def previous_image():
    global current_index
    if current_index > 0:
        current_index -= 1
        show_image(current_index)

def save_image():
    if images:
        selected_album = album_combobox.get()
        if selected_album:
            save_to_album(images[current_index], selected_album)
        else:
            messagebox.showwarning("Álbum Não Selecionado", "Por favor, selecione um álbum para salvar a imagem.")

# Carrega imagens
images = load_images(IMAGES_FOLDER)
current_index = 0

# UI Tkinter
root = tk.Tk()
root.title("Galeria de Imagens")

# Label para a imagem
img_label = tk.Label(root)
img_label.pack()

# ComboBox para seleção de álbum
album_frame = tk.Frame(root)
album_frame.pack(pady=10)

album_label = tk.Label(album_frame, text="Selecione um álbum:")
album_label.pack(side=tk.LEFT)

# ComboBox com álbuns disponíveis
album_combobox = ttk.Combobox(album_frame, state="readonly", values=list(fake_db["PageData"].keys()))
album_combobox.pack(side=tk.LEFT, padx=10)

# Botão para criar um novo álbum
btn_create_album = tk.Button(album_frame, text="Criar Novo Álbum", command=create_new_album)
btn_create_album.pack(side=tk.LEFT)

# Botões de navegação e salvar
frame = tk.Frame(root)
frame.pack(pady=10)

btn_prev = tk.Button(frame, text="Previous", command=previous_image)
btn_prev.grid(row=0, column=0)

btn_next = tk.Button(frame, text="Next", command=next_image)
btn_next.grid(row=0, column=1)

btn_save = tk.Button(frame, text="Save", command=save_image)
btn_save.grid(row=0, column=2)

# Mostra a primeira imagem
if images:
    show_image(current_index)
else:
    messagebox.showerror("Erro", "Nenhuma imagem encontrada na pasta 'imgs'.")

root.mainloop()
