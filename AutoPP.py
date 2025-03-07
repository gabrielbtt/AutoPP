import os
import sys
import subprocess
import customtkinter as ctk
from tkinter import filedialog, messagebox

def resource_path(relative_path):
    """Obtém o caminho absoluto para recursos (funciona no executável)"""
    try:
        # PyInstaller cria uma pasta temporária
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))  # Diretório do script
    
    path = os.path.join(base_path, relative_path)
    print(f"Tentando carregar ícone de: {path}")  # Para debug
    return path

# Configuração do tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Criar janela
root = ctk.CTk()
root.title("AutoPP")
root.geometry("500x400")

# Defina o ícone da janela
icon_path = resource_path("LogoAutoPP16.ico")
if os.path.exists(icon_path):  # Verifica se o ícone existe
    root.iconbitmap(icon_path)
else:
    print(f"Ícone não encontrado em: {icon_path}")

def escolher_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        pasta_entry.delete(0, "end")
        pasta_entry.insert(0, pasta)
        verificar_repositorio(pasta)  # Verifica se é um repositório Git e atualiza a interface

def verificar_repositorio(pasta):
    """Verifica se a pasta é um repositório Git e oculta/exibe o campo da URL conforme necessário"""
    is_git_repo = os.path.exists(os.path.join(pasta, ".git"))
    
    if not is_git_repo:
        try:
            subprocess.run(["git", "init"], cwd=pasta, check=True)
            messagebox.showinfo("Repositório Criado", "A pasta não era um repositório Git. Git inicializado automaticamente!")
        except subprocess.CalledProcessError:
            messagebox.showerror("Erro", "Falha ao inicializar o repositório Git!")
    
    atualizar_interface(is_git_repo)  # Atualiza a interface para exibir ou ocultar a URL

def atualizar_interface(is_git_repo):
    """Mostra ou esconde o campo da URL dependendo se o repositório já está inicializado"""
    if is_git_repo:
        repo_label.pack_forget()
        repo_entry.pack_forget()
    else:
        repo_label.pack(anchor="w")
        repo_entry.pack(pady=5)

def executar_git(comando):
    pasta = pasta_entry.get()
    repo_url = repo_entry.get()
    commit_msg = commit_entry.get()

    if not pasta:
        messagebox.showerror("Erro", "Escolha a pasta do repositório!")
        return

    verificar_repositorio(pasta)  # Garante que o repositório foi inicializado
    os.chdir(pasta)

    try:
        # Verifica se já existe um remoto configurado
        result = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True)
        tem_origin = "origin" in result.stdout

        # Se não houver um remoto e a URL não foi informada, exibe erro
        if not tem_origin and not repo_url:
            messagebox.showerror("Erro", "O repositório não tem um remoto configurado.\nPor favor, insira a URL do repositório!")
            return

        # Se não houver um remoto e o usuário forneceu uma URL, adiciona o origin
        if not tem_origin and repo_url:
            subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)

        if comando == "push":
            if not commit_msg:
                messagebox.showerror("Erro", "Digite uma mensagem de commit!")
                return

            subprocess.run(["git", "add", "."], check=True)

            # Verifica se há algo para commitar
            status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
            if not status.stdout.strip():
                messagebox.showinfo("Sem mudanças", "Nenhuma alteração detectada para commit.")
                return

            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "branch", "-M", "main"], check=True)
            subprocess.run(["git", "push", "-u", "origin", "main"], check=True)

        elif comando == "pull":
            subprocess.run(["git", "pull", "origin", "main"], check=True)

        messagebox.showinfo("Sucesso", f"Git {comando} realizado com sucesso!")

    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro", f"Falha ao executar git {comando}!\n\nDetalhes:\n{e}")

def forcar_pull():
    """Força o pull, descartando todas as alterações locais"""
    pasta = pasta_entry.get()
    
    if not pasta:
        messagebox.showerror("Erro", "Escolha a pasta do repositório!")
        return
    
    resposta = messagebox.askyesno(
        "Confirmação",
        "Isso descartará todas as suas mudanças locais!\nTem certeza que deseja continuar?"
    )

    if resposta:
        try:
            os.chdir(pasta)
            subprocess.run(["git", "reset", "--hard", "HEAD"], check=True)
            subprocess.run(["git", "pull", "origin", "main"], check=True)
            messagebox.showinfo("Sucesso", "Força de pull realizada com sucesso!")
        except subprocess.CalledProcessError:
            messagebox.showerror("Erro", "Falha ao forçar o pull!")

# Layout
frame = ctk.CTkFrame(root, fg_color="transparent")
frame.pack(pady=20, padx=20, fill="both", expand=True)

ctk.CTkLabel(frame, text="Pasta do Repositório:").pack(anchor="w")
pasta_entry = ctk.CTkEntry(frame, width=400)
pasta_entry.pack(pady=5)
ctk.CTkButton(frame, text="Escolher Pasta", command=escolher_pasta).pack(pady=5)

# Campo da URL (inicialmente oculto)
repo_label = ctk.CTkLabel(frame, text="URL do Repositório:")
repo_entry = ctk.CTkEntry(frame, width=400)

ctk.CTkLabel(frame, text="Mensagem de Commit:").pack(anchor="w")
commit_entry = ctk.CTkEntry(frame, width=400)
commit_entry.pack(pady=5)

btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
btn_frame.pack(pady=10)

ctk.CTkButton(btn_frame, text="Baixar", command=lambda: executar_git("pull"), fg_color="green").pack(side="left", padx=10)
ctk.CTkButton(btn_frame, text="Enviar", command=lambda: executar_git("push"), fg_color="blue").pack(side="right", padx=10)

# Botão para Forçar Pull
ctk.CTkButton(frame, text="Descartar Local", command=forcar_pull, fg_color="red").pack(pady=10)

# Inicialmente esconde a URL
atualizar_interface(False)

root.mainloop()