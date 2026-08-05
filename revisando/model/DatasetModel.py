import json
import os

from dataclasses import dataclass

@dataclass
class Dataset():

    titulo: str = ""
    contexto: str = ""
    pergunta: str = ""
    resposta: str = ""
    respostaPlausivel: str = ""
    impossivel: bool = False