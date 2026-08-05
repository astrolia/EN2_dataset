        


class data:

    def __init__(self):
        self._titulo = ""
        self._contexto = ""
        self._pergunta = ""
        self._resposta = ""
        self._respostaPlausivel = ""
        self._impossivel = False

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, titulo):
        self._titulo = titulo

    @property
    def contexto(self):
        return self._contexto

    @contexto.setter
    def contexto(self, contexto):
        self._contexto = contexto

    @property
    def pergunta(self):
        return self._pergunta

    @pergunta.setter
    def pergunta(self, pergunta):
        self._pergunta = pergunta

    @property
    def resposta(self):
        return self._resposta

    @resposta.setter
    def resposta(self, resposta):
        self._resposta = resposta

    @property
    def respostaPlausivel(self):
        return self._respostaPlausivel

    @respostaPlausivel.setter
    def respostaPlausivel(self, respostaPlausivel):
        self._respostaPlausivel = respostaPlausivel

    @property
    def impossivel(self):
        return self._impossivel

    @impossivel.setter
    def impossivel(self, valor):
        self._impossivel = valor