import json
import os

import model.DatasetModel


class DatasetDAO:
    def __init__(self):

        self._contador = 1
        self._dictBase = ""
        self._dictTitulo = ""
        self._dictContexto = ""
        self._dictPerguntaResposta = ""


    def printar(self):

        titulo = self._dictBase


        return titulo


    def CriarBase(self):

        self._dictBase = {
                "version": "v2.0",
                "data": []
            }

    def CriarTitulo(self, titulo):

        titulo = titulo.strip()

        # estrutura topico
        self._dictTitulo = {
            "title": titulo,
            "paragraphs": []
        }

    def CriarContexto(self, contexto):

        contexto = contexto.strip()
        
        self._dictContexto = {
            "context": contexto,
            "qas": []
        }

    def CriarPerguntaResposta(self, pergunta, resposta, impossivel, titulo, inicio_resposta):

        pergunta = pergunta.strip()
        resposta = resposta.strip()
        #respostaPlausivel = respostaPlausivel.strip()

        dictPR = {
            "id": f"id_{titulo}_{self._contador}",
            "question": pergunta,
            "is_impossible": impossivel,
            "answers": [],
            "plausible_answers": []
            }
        self._contador += 1

        if not impossivel:

            dictPR["answers"].append({
                "text": resposta,
                "answer_start": inicio_resposta
            })
        else:

            dictPR["plausible_answers"].append({
                "text": resposta,
                "answer_start": inicio_resposta
            })

        self._dictContexto["qas"].append(dictPR)


    def FecharContexto(self):

        self._dictTitulo["paragraphs"].append(self._dictContexto)

    def FecharDataset(self):

        self._dictBase["data"].append(self._dictTitulo)

    def SalvarDataset(self, nome_arquivo):

        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(self._dictBase, f, ensure_ascii=False, indent=2)




        