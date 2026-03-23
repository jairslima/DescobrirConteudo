# Descobrir a Extenção do Arquivo pelo Conteúdo By Jair Lima

## Descrição
Ferramenta para identificar e restaurar extensões de arquivos que foram perdidas, analisando o conteúdo (magic bytes) de cada arquivo para determinar seu tipo real. Possui interface gráfica (GUI) e modo linha de comando (CLI).

## Stack e Dependências
- **Python 3.10+**
- **python-magic-bin** (libmagic para Windows): detecção de MIME type pelo conteúdo
- **tkinter** (built-in): interface gráfica

### Instalação de dependências
```bash
pip install python-magic-bin
```

## Estrutura
```
DescobrirConteudo/
├── descobrir_conteudo.py   # Script principal (CLI + GUI)
├── PROJECT.md              # Documentação de continuidade
├── README.md               # Documentação do repositório
├── requirements.txt        # Dependências Python
├── .gitignore              # Arquivos ignorados pelo Git
└── dist/
    └── DescobrirConteudo.exe  # Executável Windows (gerado via PyInstaller)
```

## Comandos

### Interface gráfica (padrão)
```bash
python descobrir_conteudo.py
```

### Modo CLI
```bash
python descobrir_conteudo.py "C:\caminho\da\pasta"        # Varrer pasta
python descobrir_conteudo.py "C:\caminho\da\pasta" -r      # Incluir subpastas
python descobrir_conteudo.py "C:\caminho\da\pasta" -r -y   # Renomear sem perguntar
python descobrir_conteudo.py --cli                          # CLI na pasta atual
```

### Gerar executável
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "DescobrirConteudo" --clean descobrir_conteudo.py
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

## Decisões arquiteturais
- Usa `python-magic-bin` (inclui binários libmagic) para evitar dependências externas no Windows
- Usa `from_buffer()` ao invés de `from_file()` para compatibilidade com caminhos contendo caracteres especiais (acentos, cedilha)
- Detecção inteligente de extensão: ignora extensões falsas como `.09`, `. 02` (puramente numéricas ou com espaço)
- Mapeamento MIME para extensão customizado cobrindo 60+ tipos
- Se o nome destino já existe, adiciona sufixo numérico (_1, _2)
- Thread separada para varredura na GUI (não trava a interface)
- Encoding UTF-8 forçado no stdout para compatibilidade com console Windows (cp1252)

## Estado atual
- v1.0: funcional com CLI e GUI, testado com arquivos reais
- Executável Windows disponível em dist/

## Problemas conhecidos
- Arquivos de texto podem ser classificados genericamente como "text/plain" quando o formato específico não é detectável
- `application/octet-stream` (tipo genérico binário) não recebe extensão pois seria impreciso
