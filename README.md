# Descobrir a Extenção do Arquivo pelo Conteúdo By Jair Lima

Ferramenta para identificar e restaurar extensões de arquivos perdidas, analisando o conteúdo binário (magic bytes) de cada arquivo para determinar seu tipo real.

## O problema

Arquivos podem perder suas extensões por diversos motivos: transferências interrompidas, renomeações acidentais, downloads corrompidos, backups mal formatados. Sem a extensão, o sistema operacional não sabe qual programa usar para abrir o arquivo.

## A solução

Este programa varre uma pasta, encontra arquivos sem extensão (ou com extensão falsa/numérica), analisa os primeiros bytes do conteúdo para identificar o tipo real e renomeia adicionando a extensão correta.

## Instalação

### Opção 1: Executável Windows (sem Python)
Baixe o `DescobrirConteudo.exe` da seção [Releases](../../releases) e execute diretamente.

### Opção 2: Rodar com Python
```bash
pip install python-magic-bin
python descobrir_conteudo.py
```

## Uso

### Interface gráfica
```bash
python descobrir_conteudo.py
```
1. Selecione a pasta com os arquivos
2. Marque "Subpastas" se quiser varrer recursivamente
3. Clique em "Varrer"
4. Revise os resultados na tabela
5. Selecione/desmarque os arquivos desejados
6. Clique em "Renomear Selecionados"

### Linha de comando
```bash
# Varrer uma pasta
python descobrir_conteudo.py "C:\minha\pasta"

# Varrer incluindo subpastas
python descobrir_conteudo.py "C:\minha\pasta" -r

# Renomear automaticamente sem confirmação
python descobrir_conteudo.py "C:\minha\pasta" -r -y

# Modo CLI na pasta atual
python descobrir_conteudo.py --cli
```

## Tipos suportados (60+)

| Categoria    | Formatos                                              |
|--------------|-------------------------------------------------------|
| Documentos   | PDF, DOCX, DOC, XLSX, XLS, PPTX, PPT, RTF, ODT, ODS, EPUB |
| Imagens      | JPG, PNG, GIF, BMP, WEBP, TIFF, SVG, ICO, PSD        |
| Áudio        | MP3, WAV, OGG, FLAC, AAC, M4A                         |
| Vídeo        | MP4, AVI, MKV, MOV, WEBM, FLV, MPEG                   |
| Compactados  | ZIP, RAR, 7Z, GZ, TAR, BZ2                            |
| Executáveis  | EXE, DLL, MSI, JAR                                    |
| Texto/Código | TXT, HTML, CSS, CSV, XML, JSON, JS, PY, C, CPP, JAVA, SH |
| Outros       | SQLite, ISO, TTF, OTF, WOFF, WOFF2                    |

## Como funciona

1. **Varredura**: lista todos os arquivos da pasta
2. **Filtro de extensão inteligente**: identifica arquivos sem extensão real (ignora extensões falsas como `.09`, `. 02`)
3. **Detecção por conteúdo**: lê os primeiros 8KB de cada arquivo e usa libmagic para identificar o MIME type
4. **Mapeamento**: converte o MIME type para a extensão de arquivo correspondente
5. **Renomeação segura**: adiciona a extensão ao nome original (com sufixo numérico se já existir arquivo com o mesmo nome)

## Gerar executável

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "DescobrirConteudo" --clean descobrir_conteudo.py
```

O executável será gerado em `dist/DescobrirConteudo.exe`.

## Licença

MIT
