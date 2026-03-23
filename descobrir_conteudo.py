"""
Descobrir a Extenção do Arquivo pelo Conteúdo By Jair Lima
Ferramenta para identificar e restaurar extensões de arquivos
pela análise do conteúdo (magic bytes).
"""

import os
import sys
import argparse
import magic

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading

# Mapeamento de MIME types para extensões comuns
MIME_TO_EXT = {
    # Documentos
    "application/pdf": ".pdf",
    "application/msword": ".doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "application/vnd.ms-excel": ".xls",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
    "application/vnd.ms-powerpoint": ".ppt",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx",
    "application/rtf": ".rtf",
    "application/vnd.oasis.opendocument.text": ".odt",
    "application/vnd.oasis.opendocument.spreadsheet": ".ods",
    "application/epub+zip": ".epub",
    # Imagens
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif",
    "image/bmp": ".bmp",
    "image/webp": ".webp",
    "image/tiff": ".tiff",
    "image/svg+xml": ".svg",
    "image/x-icon": ".ico",
    "image/vnd.adobe.photoshop": ".psd",
    # Áudio
    "audio/mpeg": ".mp3",
    "audio/wav": ".wav",
    "audio/x-wav": ".wav",
    "audio/ogg": ".ogg",
    "audio/flac": ".flac",
    "audio/x-flac": ".flac",
    "audio/aac": ".aac",
    "audio/mp4": ".m4a",
    "audio/x-m4a": ".m4a",
    # Vídeo
    "video/mp4": ".mp4",
    "video/x-msvideo": ".avi",
    "video/x-matroska": ".mkv",
    "video/quicktime": ".mov",
    "video/webm": ".webm",
    "video/x-flv": ".flv",
    "video/mpeg": ".mpeg",
    # Compactados
    "application/zip": ".zip",
    "application/x-rar-compressed": ".rar",
    "application/x-rar": ".rar",
    "application/x-7z-compressed": ".7z",
    "application/gzip": ".gz",
    "application/x-tar": ".tar",
    "application/x-bzip2": ".bz2",
    # Executáveis e binários
    "application/x-executable": ".exe",
    "application/x-dosexec": ".exe",
    "application/x-msi": ".msi",
    "application/java-archive": ".jar",
    "application/x-sharedlib": ".dll",
    # Texto
    "text/plain": ".txt",
    "text/html": ".html",
    "text/css": ".css",
    "text/csv": ".csv",
    "text/xml": ".xml",
    "application/json": ".json",
    "application/javascript": ".js",
    "text/x-python": ".py",
    "text/x-c": ".c",
    "text/x-c++": ".cpp",
    "text/x-java": ".java",
    "application/x-shellscript": ".sh",
    # Outros
    "application/x-sqlite3": ".sqlite",
    "application/vnd.sqlite3": ".sqlite",
    "application/x-iso9660-image": ".iso",
    "application/x-font-ttf": ".ttf",
    "font/ttf": ".ttf",
    "font/otf": ".otf",
    "font/woff": ".woff",
    "font/woff2": ".woff2",
}


EXTENSOES_CONHECIDAS = set(MIME_TO_EXT.values()) | {
    ".doc", ".xls", ".ppt", ".odt", ".ods", ".odp",
    ".mp3", ".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv",
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".svg", ".ico",
    ".pdf", ".txt", ".html", ".htm", ".css", ".csv", ".xml", ".json", ".js",
    ".py", ".c", ".cpp", ".java", ".sh", ".bat", ".cmd", ".ps1",
    ".zip", ".rar", ".7z", ".gz", ".tar", ".bz2",
    ".exe", ".msi", ".dll", ".so", ".dylib",
    ".iso", ".img", ".dmg",
    ".ttf", ".otf", ".woff", ".woff2",
    ".sqlite", ".db", ".mdb", ".accdb",
    ".docx", ".xlsx", ".pptx", ".rtf", ".epub",
    ".flac", ".aac", ".ogg", ".wav", ".wma", ".m4a",
    ".webm", ".mpeg", ".mpg", ".ts",
    ".psd", ".ai", ".eps", ".indd",
    ".apk", ".ipa", ".deb", ".rpm",
    ".log", ".ini", ".cfg", ".conf", ".yaml", ".yml", ".toml",
    ".md", ".rst", ".tex", ".bib",
    ".sql", ".jar", ".war", ".class",
    ".swf", ".fla",
    ".tmp", ".bak", ".old",
}


def tem_extensao(nome_arquivo):
    """Verifica se o arquivo possui uma extensão real e conhecida."""
    _, ext = os.path.splitext(nome_arquivo)
    if not ext or len(ext) < 2:
        return False
    ext_lower = ext.lower()
    # Extensão com espaço não é extensão real (ex: ". 02")
    if " " in ext:
        return False
    # Extensão puramente numérica não é extensão real (ex: ".09", ".02")
    if ext[1:].isdigit():
        return False
    # Verificar se é uma extensão conhecida
    if ext_lower in EXTENSOES_CONHECIDAS:
        return True
    # Extensões muito longas (mais de 10 chars) provavelmente não são extensões
    if len(ext) > 10:
        return False
    # Extensões curtas alfanuméricas (2-5 chars) podem ser válidas
    if 2 <= len(ext) <= 6 and ext[1:].isalpha():
        return True
    return False


def detectar_tipo(caminho_arquivo):
    """Detecta o MIME type do arquivo pelo conteúdo (lê bytes diretamente para compatibilidade com Windows e caracteres especiais)."""
    try:
        with open(caminho_arquivo, "rb") as f:
            header = f.read(8192)
        mime = magic.Magic(mime=True)
        return mime.from_buffer(header)
    except Exception:
        return None


def obter_extensao(mime_type):
    """Retorna a extensão correspondente ao MIME type."""
    if not mime_type:
        return None
    if mime_type in MIME_TO_EXT:
        return MIME_TO_EXT[mime_type]
    if mime_type == "application/octet-stream":
        return None
    return None


def varrer_pasta(pasta, recursivo=False):
    """Varre a pasta e retorna lista de arquivos sem extensão com tipo detectado."""
    resultados = []
    if recursivo:
        for raiz, _, arquivos in os.walk(pasta):
            for nome in arquivos:
                caminho = os.path.join(raiz, nome)
                if not tem_extensao(nome):
                    mime = detectar_tipo(caminho)
                    ext = obter_extensao(mime)
                    resultados.append({
                        "caminho": caminho,
                        "nome": nome,
                        "mime": mime or "desconhecido",
                        "extensao": ext,
                    })
    else:
        for item in os.listdir(pasta):
            caminho = os.path.join(pasta, item)
            if os.path.isfile(caminho) and not tem_extensao(item):
                mime = detectar_tipo(caminho)
                ext = obter_extensao(mime)
                resultados.append({
                    "caminho": caminho,
                    "nome": item,
                    "mime": mime or "desconhecido",
                    "extensao": ext,
                })
    return resultados


def renomear_arquivo(caminho, nova_extensao):
    """Renomeia o arquivo adicionando a extensão."""
    novo_caminho = caminho + nova_extensao
    if os.path.exists(novo_caminho):
        base = caminho + nova_extensao
        contador = 1
        while os.path.exists(novo_caminho):
            novo_caminho = f"{caminho}_{contador}{nova_extensao}"
            contador += 1
    os.rename(caminho, novo_caminho)
    return novo_caminho


# ─── Interface gráfica ───

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Descobrir a Extenção do Arquivo pelo Conteúdo By Jair Lima")
        self.geometry("900x600")
        self.minsize(800, 500)
        self.resultados = []
        self._criar_widgets()

    def _criar_widgets(self):
        # Header
        header = tk.Frame(self, bg="#2c3e50", height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(
            header,
            text="Descobrir a Extenção do Arquivo pelo Conteúdo By Jair Lima",
            font=("Segoe UI", 16, "bold"),
            fg="white",
            bg="#2c3e50",
        ).pack(pady=12)

        # Frame de controles
        controles = tk.Frame(self, pady=10, padx=10)
        controles.pack(fill=tk.X)

        tk.Label(controles, text="Pasta:", font=("Segoe UI", 10)).pack(side=tk.LEFT)
        self.var_pasta = tk.StringVar(value=os.getcwd())
        entry_pasta = tk.Entry(controles, textvariable=self.var_pasta, width=50, font=("Segoe UI", 10))
        entry_pasta.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        tk.Button(controles, text="Procurar...", command=self._escolher_pasta).pack(side=tk.LEFT, padx=2)

        self.var_recursivo = tk.BooleanVar(value=False)
        tk.Checkbutton(controles, text="Subpastas", variable=self.var_recursivo).pack(side=tk.LEFT, padx=5)

        tk.Button(
            controles, text="Varrer", command=self._iniciar_varredura,
            bg="#27ae60", fg="white", font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT, padx=15
        ).pack(side=tk.LEFT, padx=5)

        # Tabela de resultados
        frame_tabela = tk.Frame(self, padx=10)
        frame_tabela.pack(fill=tk.BOTH, expand=True)

        colunas = ("selecionar", "arquivo", "pasta", "mime", "extensao")
        self.tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings", selectmode="extended")
        self.tree.heading("selecionar", text="✓")
        self.tree.heading("arquivo", text="Arquivo")
        self.tree.heading("pasta", text="Pasta")
        self.tree.heading("mime", text="Tipo MIME")
        self.tree.heading("extensao", text="Extensão")

        self.tree.column("selecionar", width=30, anchor="center")
        self.tree.column("arquivo", width=200)
        self.tree.column("pasta", width=250)
        self.tree.column("mime", width=200)
        self.tree.column("extensao", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabela, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<ButtonRelease-1>", self._toggle_selecao)

        # Frame de ações
        acoes = tk.Frame(self, pady=10, padx=10)
        acoes.pack(fill=tk.X)

        self.lbl_status = tk.Label(acoes, text="Pronto", font=("Segoe UI", 9), fg="#7f8c8d")
        self.lbl_status.pack(side=tk.LEFT)

        tk.Button(
            acoes, text="Selecionar Todos", command=self._selecionar_todos
        ).pack(side=tk.RIGHT, padx=2)

        tk.Button(
            acoes, text="Desmarcar Todos", command=self._desmarcar_todos
        ).pack(side=tk.RIGHT, padx=2)

        tk.Button(
            acoes, text="Renomear Selecionados", command=self._renomear_selecionados,
            bg="#2980b9", fg="white", font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT, padx=15
        ).pack(side=tk.RIGHT, padx=5)

        self.selecionados = set()

    def _escolher_pasta(self):
        pasta = filedialog.askdirectory(initialdir=self.var_pasta.get())
        if pasta:
            self.var_pasta.set(pasta)

    def _iniciar_varredura(self):
        pasta = self.var_pasta.get()
        if not os.path.isdir(pasta):
            messagebox.showerror("Erro", f"Pasta não encontrada:\n{pasta}")
            return
        self.lbl_status.config(text="Varrendo...", fg="#e67e22")
        self.tree.delete(*self.tree.get_children())
        self.selecionados.clear()
        self.resultados.clear()
        threading.Thread(target=self._varrer, args=(pasta,), daemon=True).start()

    def _varrer(self, pasta):
        resultados = varrer_pasta(pasta, self.var_recursivo.get())
        self.after(0, self._exibir_resultados, resultados)

    def _exibir_resultados(self, resultados):
        self.resultados = resultados
        for i, r in enumerate(resultados):
            pasta_arquivo = os.path.dirname(r["caminho"])
            ext_texto = r["extensao"] if r["extensao"] else "?"
            marcado = "☑" if r["extensao"] else "☐"
            item_id = self.tree.insert("", tk.END, values=(
                marcado, r["nome"], pasta_arquivo, r["mime"], ext_texto
            ))
            if r["extensao"]:
                self.selecionados.add(item_id)

        total = len(resultados)
        identificados = sum(1 for r in resultados if r["extensao"])
        self.lbl_status.config(
            text=f"{total} arquivo(s) sem extensão encontrado(s), {identificados} identificado(s)",
            fg="#27ae60" if identificados > 0 else "#e74c3c"
        )

    def _toggle_selecao(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region != "cell":
            return
        col = self.tree.identify_column(event.x)
        if col != "#1":
            return
        item = self.tree.identify_row(event.y)
        if not item:
            return
        idx = self.tree.index(item)
        if idx >= len(self.resultados) or not self.resultados[idx]["extensao"]:
            return
        valores = list(self.tree.item(item, "values"))
        if item in self.selecionados:
            self.selecionados.discard(item)
            valores[0] = "☐"
        else:
            self.selecionados.add(item)
            valores[0] = "☑"
        self.tree.item(item, values=valores)

    def _selecionar_todos(self):
        for item in self.tree.get_children():
            idx = self.tree.index(item)
            if idx < len(self.resultados) and self.resultados[idx]["extensao"]:
                self.selecionados.add(item)
                valores = list(self.tree.item(item, "values"))
                valores[0] = "☑"
                self.tree.item(item, values=valores)

    def _desmarcar_todos(self):
        self.selecionados.clear()
        for item in self.tree.get_children():
            valores = list(self.tree.item(item, "values"))
            valores[0] = "☐"
            self.tree.item(item, values=valores)

    def _renomear_selecionados(self):
        if not self.selecionados:
            messagebox.showwarning("Aviso", "Nenhum arquivo selecionado.")
            return

        itens_para_renomear = []
        for item in self.selecionados:
            idx = self.tree.index(item)
            if idx < len(self.resultados):
                r = self.resultados[idx]
                if r["extensao"]:
                    itens_para_renomear.append((item, idx, r))

        if not itens_para_renomear:
            messagebox.showwarning("Aviso", "Nenhum arquivo identificado para renomear.")
            return

        msg = f"Renomear {len(itens_para_renomear)} arquivo(s)?\n\n"
        for _, _, r in itens_para_renomear[:10]:
            msg += f"  {r['nome']}  →  {r['nome']}{r['extensao']}\n"
        if len(itens_para_renomear) > 10:
            msg += f"  ... e mais {len(itens_para_renomear) - 10}\n"

        if not messagebox.askyesno("Confirmar", msg):
            return

        sucesso = 0
        erros = 0
        for item, idx, r in itens_para_renomear:
            try:
                novo = renomear_arquivo(r["caminho"], r["extensao"])
                novo_nome = os.path.basename(novo)
                valores = list(self.tree.item(item, "values"))
                valores[0] = "✔"
                valores[1] = novo_nome
                self.tree.item(item, values=valores, tags=("renomeado",))
                sucesso += 1
            except Exception as e:
                valores = list(self.tree.item(item, "values"))
                valores[0] = "✘"
                self.tree.item(item, values=valores, tags=("erro",))
                erros += 1

        self.tree.tag_configure("renomeado", foreground="#27ae60")
        self.tree.tag_configure("erro", foreground="#e74c3c")
        self.selecionados.clear()
        self.lbl_status.config(
            text=f"Concluído: {sucesso} renomeado(s), {erros} erro(s)",
            fg="#27ae60" if erros == 0 else "#e67e22"
        )


def modo_cli(pasta, recursivo=False, automatico=False):
    """Modo linha de comando."""
    print(f"\nDescobrir a Extenção do Arquivo pelo Conteúdo By Jair Lima")
    print(f"Varrendo: {pasta}")
    print(f"Recursivo: {'Sim' if recursivo else 'Não'}\n")

    resultados = varrer_pasta(pasta, recursivo)

    if not resultados:
        print("Nenhum arquivo sem extensão encontrado.")
        return

    print(f"{'Arquivo':<30} {'MIME Type':<50} {'Extensão':<10}")
    print("-" * 90)

    identificados = []
    for r in resultados:
        ext = r["extensao"] if r["extensao"] else "?"
        print(f"{r['nome']:<30} {r['mime']:<50} {ext:<10}")
        if r["extensao"]:
            identificados.append(r)

    print(f"\nTotal: {len(resultados)} arquivo(s), {len(identificados)} identificado(s)")

    if not identificados:
        print("Nenhum arquivo pôde ser identificado.")
        return

    if automatico:
        confirmar = True
    else:
        resp = input("\nDeseja renomear os arquivos identificados? (s/n): ").strip().lower()
        confirmar = resp in ("s", "sim", "y", "yes")

    if confirmar:
        for r in identificados:
            try:
                novo = renomear_arquivo(r["caminho"], r["extensao"])
                print(f"  ✔ {r['nome']}  →  {os.path.basename(novo)}")
            except Exception as e:
                print(f"  ✘ {r['nome']}  →  Erro: {e}")
        print("\nConcluído!")
    else:
        print("Operação cancelada.")


def main():
    parser = argparse.ArgumentParser(
        description="Descobrir a Extenção do Arquivo pelo Conteúdo By Jair Lima: identifica e restaura extensões de arquivos"
    )
    parser.add_argument("pasta", nargs="?", default=None, help="Pasta para varrer (padrão: abre interface gráfica)")
    parser.add_argument("-r", "--recursivo", action="store_true", help="Varrer subpastas")
    parser.add_argument("-y", "--sim", action="store_true", help="Renomear automaticamente sem perguntar")
    parser.add_argument("--cli", action="store_true", help="Forçar modo linha de comando")

    args = parser.parse_args()

    if args.pasta or args.cli:
        pasta = args.pasta or os.getcwd()
        if not os.path.isdir(pasta):
            print(f"Erro: pasta não encontrada: {pasta}")
            sys.exit(1)
        modo_cli(pasta, args.recursivo, args.sim)
    else:
        app = App()
        app.mainloop()


if __name__ == "__main__":
    main()
