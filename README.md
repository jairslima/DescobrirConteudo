# Descobrir a Extensao do Arquivo pelo Conteudo By Jair Lima

Ferramenta para identificar e restaurar extensoes de arquivos perdidas, analisando o conteudo binario (magic bytes) de cada arquivo para determinar seu tipo real.

## O problema

Arquivos podem perder suas extensoes por diversos motivos: transferencias interrompidas, renomeacoes acidentais, downloads corrompidos, backups mal formatados. Sem a extensao, o sistema operacional nao sabe qual programa usar para abrir o arquivo.

## A solucao

Este programa varre uma pasta ou analisa um arquivo especifico, encontra arquivos sem extensao (ou com extensao falsa/numerica), analisa os primeiros bytes do conteudo para identificar o tipo real e renomeia adicionando a extensao correta.

## Instalacao

### Opcao 1: Executavel Windows
Baixe o `DescobrirConteudo.exe` da secao [Releases](../../releases) e execute diretamente.

### Opcao 2: Rodar com Python
```bash
pip install -r requirements.txt
python descobrir_conteudo.py
```

## Uso

### Escopo de execucao

A execucao **nao e global por padrao**.

- Com Python, voce roda a partir da pasta do projeto: `python descobrir_conteudo.py`
- Com o executavel, voce roda pelo caminho completo ou a partir da pasta onde esta o `DescobrirConteudo.exe`
- So passa a ser "global" se voce adicionar a pasta do executavel ao `PATH` do Windows, ou criar um atalho/comando proprio

### Parametros aceitos

O aplicativo aceita como alvo:

- **um arquivo sem extensao**
- **uma pasta**

Se o alvo for um arquivo, ele analisa apenas aquele arquivo.
Se o alvo for uma pasta, ele varre os arquivos da pasta e, com `-r`, inclui subpastas.

### Interface grafica
```bash
python descobrir_conteudo.py
```
1. Selecione um arquivo ou pasta
2. Marque "Subpastas" se quiser varrer recursivamente uma pasta
3. Clique em "Varrer"
4. Revise os resultados, incluindo a observacao do motivo
5. Selecione/desmarque os arquivos desejados
6. Clique em "Renomear Selecionados"

### Linha de comando
```bash
# Analisar um arquivo especifico
python descobrir_conteudo.py "D:\Backup\Dropbox\_AnosAnteriores\CASA EFETIVADA"

# Varrer uma pasta
python descobrir_conteudo.py "C:\minha\pasta"

# Varrer incluindo subpastas
python descobrir_conteudo.py "C:\minha\pasta" -r

# Renomear automaticamente sem confirmacao
python descobrir_conteudo.py "C:\minha\pasta" -r -y

# Modo CLI na pasta atual
python descobrir_conteudo.py --cli
```

### Executavel Windows
```powershell
# Arquivo especifico
.\dist\DescobrirConteudo.exe "D:\Backup\Dropbox\_AnosAnteriores\CASA EFETIVADA"

# Pasta
.\dist\DescobrirConteudo.exe "C:\minha\pasta"

# Pasta com subpastas e renomeacao automatica
.\dist\DescobrirConteudo.exe "C:\minha\pasta" -r -y
```

Se quiser uso global no terminal, adicione a pasta que contem `DescobrirConteudo.exe` ao `PATH` e depois rode, por exemplo:

```powershell
DescobrirConteudo.exe "D:\Backup\Dropbox\_AnosAnteriores\CASA EFETIVADA" -y
```

## Tipos suportados (60+)

| Categoria    | Formatos                                              |
|--------------|-------------------------------------------------------|
| Documentos   | PDF, DOCX, DOC, XLSX, XLS, PPTX, PPT, RTF, ODT, ODS, EPUB |
| Imagens      | JPG, PNG, GIF, BMP, WEBP, TIFF, SVG, ICO, PSD        |
| Audio        | MP3, WAV, OGG, FLAC, AAC, M4A                         |
| Video        | MP4, AVI, MKV, MOV, WEBM, FLV, MPEG                   |
| Compactados  | ZIP, RAR, 7Z, GZ, TAR, BZ2                            |
| Executaveis  | EXE, DLL, MSI, JAR                                    |
| Texto/Codigo | TXT, HTML, CSS, CSV, XML, JSON, JS, PY, C, CPP, JAVA, SH |
| Outros       | SQLite, ISO, TTF, OTF, WOFF, WOFF2                    |

## Como funciona

1. **Varredura**: lista os arquivos do caminho informado
2. **Filtro de extensao inteligente**: identifica arquivos sem extensao real e aceita analise de arquivo individual
3. **Deteccao por conteudo**: le os primeiros 8KB de cada arquivo e usa libmagic para identificar o MIME type
4. **Mapeamento**: converte o MIME type para a extensao de arquivo correspondente
5. **Diagnostico**: informa por que um arquivo nao pode ser renomeado quando o MIME e desconhecido ou nao possui mapeamento
6. **Renomeacao segura**: adiciona a extensao ao nome original, com sufixo numerico se ja existir arquivo com o mesmo nome

## Gerar executavel

```bash
pip install pyinstaller
pyinstaller --onefile --name "DescobrirConteudo" --clean descobrir_conteudo.py
```

O executavel sera gerado em `dist/DescobrirConteudo.exe`.

## Licenca

MIT
