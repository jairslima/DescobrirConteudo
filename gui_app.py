"""Interface grafica do aplicativo."""

from __future__ import annotations

import os
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from core import ResultadoAnalise, renomear_arquivo, varrer_alvo


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Descobrir a Extensao do Arquivo pelo Conteudo By Jair Lima")
        self.geometry("1100x620")
        self.minsize(900, 500)
        self.resultados: list[ResultadoAnalise] = []
        self.selecionados: set[str] = set()
        self._criar_widgets()

    def _criar_widgets(self) -> None:
        header = tk.Frame(self, bg="#2c3e50", height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(
            header,
            text="Descobrir a Extensao do Arquivo pelo Conteudo By Jair Lima",
            font=("Segoe UI", 16, "bold"),
            fg="white",
            bg="#2c3e50",
        ).pack(pady=12)

        controles = tk.Frame(self, pady=10, padx=10)
        controles.pack(fill=tk.X)

        tk.Label(controles, text="Caminho:", font=("Segoe UI", 10)).pack(side=tk.LEFT)
        self.var_alvo = tk.StringVar(value=os.getcwd())
        entry_alvo = tk.Entry(controles, textvariable=self.var_alvo, width=60, font=("Segoe UI", 10))
        entry_alvo.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        tk.Button(controles, text="Arquivo...", command=self._escolher_arquivo).pack(side=tk.LEFT, padx=2)
        tk.Button(controles, text="Pasta...", command=self._escolher_pasta).pack(side=tk.LEFT, padx=2)

        self.var_recursivo = tk.BooleanVar(value=False)
        tk.Checkbutton(controles, text="Subpastas", variable=self.var_recursivo).pack(side=tk.LEFT, padx=5)

        tk.Button(
            controles,
            text="Varrer",
            command=self._iniciar_varredura,
            bg="#27ae60",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=15,
        ).pack(side=tk.LEFT, padx=5)

        frame_tabela = tk.Frame(self, padx=10)
        frame_tabela.pack(fill=tk.BOTH, expand=True)

        colunas = ("selecionar", "arquivo", "pasta", "mime", "extensao", "motivo")
        self.tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings", selectmode="extended")
        self.tree.heading("selecionar", text="X")
        self.tree.heading("arquivo", text="Arquivo")
        self.tree.heading("pasta", text="Pasta")
        self.tree.heading("mime", text="Tipo MIME")
        self.tree.heading("extensao", text="Extensao")
        self.tree.heading("motivo", text="Observacao")

        self.tree.column("selecionar", width=35, anchor="center")
        self.tree.column("arquivo", width=220)
        self.tree.column("pasta", width=280)
        self.tree.column("mime", width=220)
        self.tree.column("extensao", width=90, anchor="center")
        self.tree.column("motivo", width=260)

        scrollbar = ttk.Scrollbar(frame_tabela, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<ButtonRelease-1>", self._toggle_selecao)

        acoes = tk.Frame(self, pady=10, padx=10)
        acoes.pack(fill=tk.X)

        self.lbl_status = tk.Label(acoes, text="Pronto", font=("Segoe UI", 9), fg="#7f8c8d")
        self.lbl_status.pack(side=tk.LEFT)

        tk.Button(acoes, text="Selecionar Todos", command=self._selecionar_todos).pack(side=tk.RIGHT, padx=2)
        tk.Button(acoes, text="Desmarcar Todos", command=self._desmarcar_todos).pack(side=tk.RIGHT, padx=2)
        tk.Button(
            acoes,
            text="Renomear Selecionados",
            command=self._renomear_selecionados,
            bg="#2980b9",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=15,
        ).pack(side=tk.RIGHT, padx=5)

    def _escolher_arquivo(self) -> None:
        atual = Path(self.var_alvo.get())
        inicial = atual.parent if atual.exists() else Path(os.getcwd())
        arquivo = filedialog.askopenfilename(initialdir=inicial)
        if arquivo:
            self.var_alvo.set(arquivo)

    def _escolher_pasta(self) -> None:
        pasta = filedialog.askdirectory(initialdir=self.var_alvo.get())
        if pasta:
            self.var_alvo.set(pasta)

    def _iniciar_varredura(self) -> None:
        alvo = Path(self.var_alvo.get())
        if not alvo.exists():
            messagebox.showerror("Erro", f"Caminho nao encontrado:\n{alvo}")
            return
        self.lbl_status.config(text="Varrendo...", fg="#e67e22")
        self.tree.delete(*self.tree.get_children())
        self.selecionados.clear()
        self.resultados.clear()
        threading.Thread(target=self._varrer, args=(alvo,), daemon=True).start()

    def _varrer(self, alvo: Path) -> None:
        resultados = varrer_alvo(alvo, self.var_recursivo.get())
        self.after(0, self._exibir_resultados, resultados)

    def _exibir_resultados(self, resultados: list[ResultadoAnalise]) -> None:
        self.resultados = resultados
        for indice, resultado in enumerate(resultados):
            extensao = resultado.extensao or "?"
            marcado = "X" if resultado.elegivel else ""
            item_id = str(indice)
            self.tree.insert(
                "",
                tk.END,
                iid=item_id,
                values=(
                    marcado,
                    resultado.nome,
                    str(resultado.caminho.parent),
                    resultado.mime,
                    extensao,
                    resultado.motivo,
                ),
            )
            if resultado.elegivel:
                self.selecionados.add(item_id)

        total = len(resultados)
        identificados = sum(1 for resultado in resultados if resultado.elegivel)
        self.lbl_status.config(
            text=f"{total} analisado(s), {identificados} renomeavel(is)",
            fg="#27ae60" if identificados > 0 else "#e74c3c",
        )

    def _toggle_selecao(self, event: tk.Event) -> None:
        if self.tree.identify_region(event.x, event.y) != "cell":
            return
        if self.tree.identify_column(event.x) != "#1":
            return
        item = self.tree.identify_row(event.y)
        if not item:
            return
        resultado = self.resultados[int(item)]
        if not resultado.elegivel:
            return

        valores = list(self.tree.item(item, "values"))
        if item in self.selecionados:
            self.selecionados.discard(item)
            valores[0] = ""
        else:
            self.selecionados.add(item)
            valores[0] = "X"
        self.tree.item(item, values=valores)

    def _selecionar_todos(self) -> None:
        for item in self.tree.get_children():
            resultado = self.resultados[int(item)]
            if resultado.elegivel:
                self.selecionados.add(item)
                valores = list(self.tree.item(item, "values"))
                valores[0] = "X"
                self.tree.item(item, values=valores)

    def _desmarcar_todos(self) -> None:
        self.selecionados.clear()
        for item in self.tree.get_children():
            valores = list(self.tree.item(item, "values"))
            valores[0] = ""
            self.tree.item(item, values=valores)

    def _renomear_selecionados(self) -> None:
        if not self.selecionados:
            messagebox.showwarning("Aviso", "Nenhum arquivo selecionado.")
            return

        itens_para_renomear = []
        for item in sorted(self.selecionados, key=int):
            resultado = self.resultados[int(item)]
            if resultado.elegivel and resultado.extensao:
                itens_para_renomear.append((item, resultado))

        if not itens_para_renomear:
            messagebox.showwarning("Aviso", "Nenhum arquivo identificado para renomear.")
            return

        msg = f"Renomear {len(itens_para_renomear)} arquivo(s)?\n\n"
        for _, resultado in itens_para_renomear[:10]:
            msg += f"  {resultado.nome} -> {resultado.nome}{resultado.extensao}\n"
        if len(itens_para_renomear) > 10:
            msg += f"  ... e mais {len(itens_para_renomear) - 10}\n"

        if not messagebox.askyesno("Confirmar", msg):
            return

        sucesso = 0
        erros = 0
        for item, resultado in itens_para_renomear:
            try:
                novo = renomear_arquivo(resultado.caminho, resultado.extensao)
                self.resultados[int(item)] = ResultadoAnalise(
                    caminho=novo,
                    nome=novo.name,
                    mime=resultado.mime,
                    extensao=resultado.extensao,
                    elegivel=False,
                    motivo=f"renomeado para {novo.name}",
                )
                valores = list(self.tree.item(item, "values"))
                valores[0] = "OK"
                valores[1] = novo.name
                valores[2] = str(novo.parent)
                valores[5] = f"renomeado para {novo.name}"
                self.tree.item(item, values=valores, tags=("renomeado",))
                sucesso += 1
            except Exception as exc:  # pragma: no cover - depende do filesystem real
                valores = list(self.tree.item(item, "values"))
                valores[0] = "ERRO"
                valores[5] = str(exc)
                self.tree.item(item, values=valores, tags=("erro",))
                erros += 1

        self.tree.tag_configure("renomeado", foreground="#27ae60")
        self.tree.tag_configure("erro", foreground="#e74c3c")
        self.selecionados.clear()
        self.lbl_status.config(
            text=f"Concluido: {sucesso} renomeado(s), {erros} erro(s)",
            fg="#27ae60" if erros == 0 else "#e67e22",
        )


def executar_gui() -> None:
    app = App()
    app.mainloop()
