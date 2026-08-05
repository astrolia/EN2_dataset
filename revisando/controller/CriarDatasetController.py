import tkinter as tk

import service.DatasetService


class CriarDatasetController:

    def __init__(self):

        self.datasetService = service.DatasetService.DatasetService()

    #são as funções q serão chamadas na interface quando alguma ação acontecer

    def printar(self):

        return self.datasetService.printar()

    def FazerBase(self):

        self.datasetService.Base()

    def FazerTItulo(self, titulo):

        self.datasetService.Titulo(titulo)

    def FazerContexto(self, contexto):

        self.datasetService.Contexto(contexto)

    def FazerPerguntaResposta(self, pergunta, resposta, contexto, impossivel, titulo):

        self.datasetService.PerguntaResposta(pergunta, resposta, contexto, impossivel, titulo)

    def FecharContexto(self):
        self.datasetService.ConcluirContexto()

    def FecharDataset(self):
        self.datasetService.ConcluirDataset()

    def Salvar(self, nome_arquivo):
        self.datasetService.Salvar(nome_arquivo)
        