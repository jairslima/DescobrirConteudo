# Descobrir a Extensao do Arquivo pelo Conteudo By Jair Lima

## Descricao
Ferramenta para identificar e restaurar extensoes de arquivos que foram perdidas, analisando o conteudo (magic bytes) de cada arquivo para determinar seu tipo real. Possui interface grafica (GUI) e modo linha de comando (CLI).

## Stack e Dependencias
- **Python 3.10+**
- **python-magic-bin** (libmagic para Windows): deteccao de MIME type pelo conteudo
- **tkinter** (built-in): interface grafica

### Instalacao de dependencias
```bash
pip install -r requirements.txt
```

## Estrutura
```text
DescobrirConteudo/
|-- descobrir_conteudo.py   # Ponto de entrada
|-- core.py                 # Nucleo de analise e renomeacao
|-- cli_app.py              # Interface de linha de comando
|-- gui_app.py              # Interface grafica
|-- PROJECT.md              # Documentacao de continuidade
|-- README.md               # Documentacao do repositorio
|-- requirements.txt        # Dependencias Python
|-- .gitignore              # Arquivos ignorados pelo Git
`-- dist/
    `-- DescobrirConteudo.exe  # Executavel Windows (gerado via PyInstaller)
```

## Comandos

### Escopo de execucao
- A execucao nao e global por padrao
- O script Python deve ser executado a partir da pasta do projeto, ou com caminho completo
- O executavel pode ser chamado por caminho completo ou a partir da pasta onde estiver
- Para uso global no terminal, a pasta do executavel precisa estar no `PATH`

### Alvos aceitos
- Arquivo individual sem extensao
- Pasta
- Pasta com subpastas quando `-r` for informado

### Interface grafica (padrao)
```bash
python descobrir_conteudo.py
```

### Modo CLI
```bash
python descobrir_conteudo.py "C:\caminho\do\arquivo"       # Analisa um arquivo
python descobrir_conteudo.py "C:\caminho\da\pasta"         # Varrer pasta
python descobrir_conteudo.py "C:\caminho\da\pasta" -r      # Incluir subpastas
python descobrir_conteudo.py "C:\caminho\da\pasta" -r -y   # Renomear sem perguntar
python descobrir_conteudo.py --cli                         # CLI na pasta atual
```

### Modo executavel
```powershell
.\dist\DescobrirConteudo.exe "C:\caminho\do\arquivo"
.\dist\DescobrirConteudo.exe "C:\caminho\da\pasta"
.\dist\DescobrirConteudo.exe "C:\caminho\da\pasta" -r -y
```

### Gerar executavel
```bash
pip install pyinstaller
pyinstaller --onefile --name "DescobrirConteudo" --clean descobrir_conteudo.py
```

## Tipos suportados (60+)
PDF, DOCX, DOC, XLSX, XLS, PPTX, PPT, RTF, ODT, ODS, EPUB,
JPG, PNG, GIF, BMP, WEBP, TIFF, SVG, ICO, PSD,
MP3, WAV, OGG, FLAC, AAC, M4A,
MP4, AVI, MKV, MOV, WEBM, FLV, MPEG,
ZIP, RAR, 7Z, GZ, TAR, BZ2,
EXE, DLL, MSI, JAR,
TXT, HTML, CSS, CSV, XML, JSON, JS, PY, C, CPP, JAVA, SH,
SQLite, ISO, TTF, OTF, WOFF, WOFF2

## Decisoes arquiteturais
- Deteccao inteligente de extensao: ignora extensoes falsas como `.09`, `. 02` (puramente numericas ou com espaco)
- Mapeamento MIME para extensao customizado cobrindo 60+ tipos
- Suporte a analise de arquivo individual na CLI e na GUI
- Diagnostico explicito quando um arquivo nao pode ser renomeado
- Se o nome destino ja existe, adiciona sufixo numerico (`_1`, `_2`)
- Thread separada para varredura na GUI (nao trava a interface)
- Encoding UTF-8 forcado no stdout para compatibilidade com console Windows (cp1252)

## Estado atual
- v1.1: CLI e GUI separadas do nucleo, com suporte a arquivo individual e mensagens de diagnostico
- Executavel Windows disponivel em `dist/`

## Problemas conhecidos
- Arquivos de texto podem ser classificados genericamente como `text/plain` quando o formato especifico nao e detectavel
- `application/octet-stream` (tipo generico binario) nao recebe extensao pois seria impreciso
