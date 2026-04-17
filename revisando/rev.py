import uuid
import json
import os

def criar_exemplo_squad(contexto, pergunta, resposta=None):

    if resposta:
        answer_start = contexto.find(resposta)

        if answer_start == -1:
            raise ValueError("Resposta não encontrada no contexto!")

        answers = [{
            "text": resposta,
            "answer_start": answer_start
        }]
        is_impossible = False
    else:
        answers = []
        is_impossible = True

    exemplo = {
        "data": [
            {
                "title": "exemplo",
                "paragraphs": [
                    {
                        "context": contexto,
                        "qas": [
                            {
                                "id": str(uuid.uuid4()),
                                "question": pergunta,
                                "answers": answers,
                                "is_impossible": is_impossible
                            }
                        ]
                    }
                ]
            }
        ]
    }

    return exemplo


dataset_total = {"data": []}

def adicionar_exemplo(dataset, exemplo):
    dataset["data"].extend(exemplo["data"])


if __name__ == "__main__":
    
    #para continuar a escrever sempre defina "continuar" como 0
    #para perguntas sem resposta basta dar enter quando for pedido a resposta
    #o trecho resposta deve estar exatamente como no texto, caso contrario o codigo retornara erro


    continuar = 0

    while(continuar == 0):

        print("Contexto:")
        contexto = input()
        print("Pergunta:")
        pergunta = input()
        print("Resposta:")
        resposta = input()

        dataset = criar_exemplo_squad(contexto, pergunta, resposta)


        adicionar_exemplo(dataset_total, dataset)

        print("Continuar?")
        continuar = int(input())

    with open("dataset_squad.json", "w", encoding="utf-8") as f:
        json.dump(dataset_total, f, indent=2, ensure_ascii=False)  

    print("Arquivo gerado com sucesso!")


