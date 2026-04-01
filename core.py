"""Nucleo de analise e renomeacao de arquivos por conteudo."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import magic

MIME_TO_EXT = {
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
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif",
    "image/bmp": ".bmp",
    "image/webp": ".webp",
    "image/tiff": ".tiff",
    "image/svg+xml": ".svg",
    "image/x-icon": ".ico",
    "image/vnd.adobe.photoshop": ".psd",
    "audio/mpeg": ".mp3",
    "audio/wav": ".wav",
    "audio/x-wav": ".wav",
    "audio/ogg": ".ogg",
    "audio/flac": ".flac",
    "audio/x-flac": ".flac",
    "audio/aac": ".aac",
    "audio/mp4": ".m4a",
    "audio/x-m4a": ".m4a",
    "video/mp4": ".mp4",
    "video/x-msvideo": ".avi",
    "video/x-matroska": ".mkv",
    "video/quicktime": ".mov",
    "video/webm": ".webm",
    "video/x-flv": ".flv",
    "video/mpeg": ".mpeg",
    "application/zip": ".zip",
    "application/x-rar-compressed": ".rar",
    "application/x-rar": ".rar",
    "application/x-7z-compressed": ".7z",
    "application/gzip": ".gz",
    "application/x-tar": ".tar",
    "application/x-bzip2": ".bz2",
    "application/x-executable": ".exe",
    "application/x-dosexec": ".exe",
    "application/x-msi": ".msi",
    "application/java-archive": ".jar",
    "application/x-sharedlib": ".dll",
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


@dataclass(slots=True)
class ResultadoAnalise:
    caminho: Path
    nome: str
    mime: str
    extensao: Optional[str]
    elegivel: bool
    motivo: str
    erro: Optional[str] = None


def tem_extensao(nome_arquivo: str) -> bool:
    """Verifica se o arquivo possui uma extensao real e conhecida."""
    ext = Path(nome_arquivo).suffix
    if not ext or len(ext) < 2:
        return False
    ext_lower = ext.lower()
    if " " in ext:
        return False
    if ext[1:].isdigit():
        return False
    if ext_lower in EXTENSOES_CONHECIDAS:
        return True
    if len(ext) > 10:
        return False
    if 2 <= len(ext) <= 6 and ext[1:].isalpha():
        return True
    return False


def detectar_tipo(caminho_arquivo: Path) -> tuple[Optional[str], Optional[str]]:
    """Detecta o MIME type do arquivo pelo conteudo."""
    try:
        with caminho_arquivo.open("rb") as arquivo:
            header = arquivo.read(8192)
        mime = magic.Magic(mime=True)
        return mime.from_buffer(header), None
    except Exception as exc:  # pragma: no cover - depende do filesystem real
        return None, str(exc)


def obter_extensao(mime_type: Optional[str]) -> Optional[str]:
    """Retorna a extensao correspondente ao MIME type."""
    if not mime_type:
        return None
    if mime_type in MIME_TO_EXT:
        return MIME_TO_EXT[mime_type]
    if mime_type == "application/octet-stream":
        return None
    return None


def analisar_arquivo(caminho: Path) -> ResultadoAnalise:
    """Analisa um arquivo individual e descreve por que ele pode ou nao ser renomeado."""
    possui_extensao = tem_extensao(caminho.name)
    mime, erro = detectar_tipo(caminho)
    extensao = obter_extensao(mime)

    if erro:
        return ResultadoAnalise(
            caminho=caminho,
            nome=caminho.name,
            mime=mime or "desconhecido",
            extensao=extensao,
            elegivel=False,
            motivo="falha ao ler ou identificar o arquivo",
            erro=erro,
        )

    if possui_extensao:
        return ResultadoAnalise(
            caminho=caminho,
            nome=caminho.name,
            mime=mime or "desconhecido",
            extensao=None,
            elegivel=False,
            motivo="arquivo ja possui extensao valida",
        )

    if extensao:
        return ResultadoAnalise(
            caminho=caminho,
            nome=caminho.name,
            mime=mime or "desconhecido",
            extensao=extensao,
            elegivel=True,
            motivo=f"extensao sugerida: {extensao}",
        )

    if mime == "application/octet-stream":
        motivo = "tipo binario generico; extensao seria imprecisa"
    elif mime:
        motivo = f"MIME sem mapeamento para extensao: {mime}"
    else:
        motivo = "tipo MIME nao identificado"

    return ResultadoAnalise(
        caminho=caminho,
        nome=caminho.name,
        mime=mime or "desconhecido",
        extensao=None,
        elegivel=False,
        motivo=motivo,
    )


def varrer_alvo(alvo: Path, recursivo: bool = False) -> list[ResultadoAnalise]:
    """Analisa um arquivo especifico ou uma pasta."""
    if alvo.is_file():
        return [analisar_arquivo(alvo)]

    resultados: list[ResultadoAnalise] = []
    if recursivo:
        arquivos = (item for item in alvo.rglob("*") if item.is_file())
    else:
        arquivos = (item for item in alvo.iterdir() if item.is_file())

    for arquivo in arquivos:
        if not tem_extensao(arquivo.name):
            resultados.append(analisar_arquivo(arquivo))
    return resultados


def renomear_arquivo(caminho: Path, nova_extensao: str) -> Path:
    """Renomeia o arquivo adicionando a extensao, evitando colisoes."""
    novo_caminho = caminho.with_name(caminho.name + nova_extensao)
    contador = 1
    while novo_caminho.exists():
        novo_caminho = caminho.with_name(f"{caminho.name}_{contador}{nova_extensao}")
        contador += 1
    caminho.rename(novo_caminho)
    return novo_caminho
