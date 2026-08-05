import json
import os

def criar_dataset_squad():
    print("--- Gerador de Dataset SQuAD 2.0 ---")
    
    # Estrutura principal do SQuAD
    dataset = {
        "version": "v2.0",
        "data": []
    }
    
    # titulo arquivo
    titulo_tema = input("Digite o título geral do tema (ex: Historia_do_Brasil): ").strip()
    
    # estrutura topico
    topico = {
        "title": titulo_tema,
        "paragraphs": []
    }
    
    id_contador = 1  # Gerador simples de ID único
    
    while True:
        print("\n--- Novo Parágrafo de Contexto ---")
        contexto = input("Digite o texto do contexto (parágrafo): ").strip()
        
        paragrafo_dict = {
            "context": contexto,
            "qas": []
        }
        
        while True:
            print("\n-- Adicionando uma Pergunta --")
            pergunta = input("Digite a pergunta: ").strip()
            
            #define se é impossivwl
            is_impossible_input = input("Esta pergunta é IMPOSSÍVEL de responder com base no texto? (s/n): ").strip().lower()
            is_impossible = True if is_impossible_input == 's' else False
            
            #ddefine estrutura 
            qa_dict = {
                "id": f"id_{titulo_tema}_{id_contador}",
                "question": pergunta,
                "is_impossible": is_impossible,
                "answers": [],
                "plausible_answers": []
            }
            id_contador += 1
            
            if not is_impossible:
                # Pergunta Respondível
                print("\nPara perguntas respondíveis, informe a resposta exata como aparece no texto.")
                resposta_texto = input("Digite a resposta exata: ").strip()
                
                # Encontra o índice no contexto
                answer_start = contexto.find(resposta_texto)
                
                if answer_start == -1:
                    print("⚠️ Alerta: A resposta digitada não foi encontrada exatamente igual no texto!")
                    print("Por favor, tente novamente para este campo.")
                    resposta_texto = input("Digite a resposta exata (letras maiúsculas/minúsculas importam): ").strip()
                    answer_start = contexto.find(resposta_texto)
                
                #add resposta em answers
                qa_dict["answers"].append({
                    "text": resposta_texto,
                    "answer_start": answer_start
                })
            else:
                # se impossivel é opcional colocar resposta plausivel
                print("\n[Opcional] Para perguntas impossíveis, você pode sugerir uma resposta 'plausível' (que parece certa, mas está errada).")
                quer_plausivel = input("Deseja adicionar uma resposta plausível? (s/n): ").strip().lower()
                
                # define resposta plausivel e confere se esta no contexto
                if quer_plausivel == 's':
                    resposta_plausivel = input("Digite a resposta plausível: ").strip()
                    answer_start_plausivel = contexto.find(resposta_plausivel)
                    
                    qa_dict["plausible_answers"].append({
                        "text": resposta_plausivel,
                        "answer_start": answer_start_plausivel
                    })
            
            paragrafo_dict["qas"].append(qa_dict)
            
            mais_pergunta = input("\nDeseja adicionar OUTRA pergunta para ESTE mesmo contexto? (s/n): ").strip().lower()
            if mais_pergunta != 's':
                break
                
        topico["paragraphs"].append(paragrafo_dict)
        
        mais_contexto = input("\nDeseja adicionar OUTRO parágrafo/contexto? (s/n): ").strip().lower()
        if mais_contexto != 's':
            break

    dataset["data"].append(topico)
    
    # Salvar em arquivo JSON
    nome_arquivo = input("\nDigite o nome do arquivo para salvar (ex: meu_dataset.json): ").strip()
    if not nome_arquivo.endswith('.json'):
        nome_arquivo += '.json'
        
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
        
    print(f"\nDataset salvo com sucesso em: {os.path.abspath(nome_arquivo)}")

#normaliza espaços e letras
def normalizar_texto(texto):
    return " ".join(texto.strip().lower().split())

def fazer_merge_squad(arquivo_principal, arquivo_novo, arquivo_saida):
    print(f"Iniciando o merge de '{arquivo_principal}' com '{arquivo_novo}'...")
    
    # 1. Carrega o arquivo principal (base)
    if not os.path.exists(arquivo_principal):
        print(f"Erro: O arquivo principal '{arquivo_principal}' não existe.")
        return
    with open(arquivo_principal, 'r', encoding='utf-8') as f:
        base_data = json.load(f)
        
    # 2. Carrega o novo arquivo que será fundido
    if not os.path.exists(arquivo_novo):
        print(f"Erro: O arquivo novo '{arquivo_novo}' não existe.")
        return
    with open(arquivo_novo, 'r', encoding='utf-8') as f:
        novo_data = json.load(f)

    # dicionário auxiliar para mapear contexto_normalizado do arquivo base
    mapa_contextos = {}
    
    #percorre o arquivo mapeando os contextos normalizados em mapa_contextos
    for topico in base_data.get("data", []):
        for paragrafo in topico.get("paragraphs", []):
            ctx_normalizado = normalizar_texto(paragrafo["context"])
            mapa_contextos[ctx_normalizado] = paragrafo

    # se a base estiver vazia cria a estrutura do novo arquivo
    if not base_data.get("data"):
        base_data["data"] = [{"title": "Dataset_Merged", "paragraphs": []}]
    
    # pelo menos um tópico alvo para adicionar novos contextos, inicio do arquivo
    alvo_topico = base_data["data"][0]

    # contadores
    contador_novas_perguntas = 0
    contador_novos_contextos = 0

    # loop para fazer o merge
    #primeiro pega um contexto do novo arquivo e normaliza
    for topico_novo in novo_data.get("data", []):
        for paragrafo_novo in topico_novo.get("paragraphs", []):
            ctx_novo_norm = normalizar_texto(paragrafo_novo["context"])
            
            # caso o contexto seja repetido ele pega do mapa
            if ctx_novo_norm in mapa_contextos:
                paragrafo_existente = mapa_contextos[ctx_novo_norm]
                
                # lista os ids para evitar duplicatas
                ids_existentes = {qa["id"] for qa in paragrafo_existente["qas"]}
                
                # caso o id n seja igual as pergundas e respostas são anexada ao final do contexto base normalmente
                for qa_nova in paragrafo_novo["qas"]:
                    if qa_nova["id"] not in ids_existentes:
                        paragrafo_existente["qas"].append(qa_nova)
                        contador_novas_perguntas += 1
                    else:
                        #se o id for parecido com o existente é adicionado _dup como sufixo de diferenciação
                        qa_nova["id"] = f"{qa_nova['id']}_dup"
                        paragrafo_existente["qas"].append(qa_nova)
                        contador_novas_perguntas += 1
            
            # se o contexto for inedito ele é adicionado ao final do arquivo normalmente
            else:
                alvo_topico["paragraphs"].append(paragrafo_novo)
                # Atualiza o mapa caso o próprio novo arquivo tenha contextos repetidos dele mesmo
                mapa_contextos[ctx_novo_norm] = paragrafo_novo
                contador_novos_contextos += 1
                contador_novas_perguntas += len(paragrafo_novo["qas"])

    #Salva o resultado final
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        json.dump(base_data, f, ensure_ascii=False, indent=2)
        
    print("\n--- Merge Concluído ---")
    print(f"Contextos inéditos adicionados: {contador_novos_contextos}")
    print(f"Total de perguntas inseridas/fundidas: {contador_novas_perguntas}")
    print(f"Arquivo salvo com sucesso em: {arquivo_saida}")


if __name__ == "__main__":
    # exemplos
    """arquivo1 = {
        "version": "v2.0",
        "data": [{
            "title": "Exemplo",
            "paragraphs": [{
                "context": "A inteligência artificial é o futuro da tecnologia.",
                "qas": [{"id": "q1", "question": "O que é o futuro?", "is_impossible": False, "answers": [{"text": "inteligência artificial", "answer_start": 2}]}]
            }]
        }]
    }
    
    arquivo2 = {
        "version": "v2.0",
        "data": [{
            "title": "Exemplo",
            "paragraphs": [
                {
                    # contexto similar com variação de identação
                    "context": "  A inteligência artificial é o futuro da tecnologia. ",
                    "qas": [{"id": "q2", "question": "Do que a IA é o futuro?", "is_impossible": False, "answers": [{"text": "da tecnologia", "answer_start": 37}]}]
                },
                {
                    # contexto novo
                    "context": "O Python é uma linguagem de programação muito popular.",
                    "qas": [{"id": "q3", "question": "O Python é o quê?", "is_impossible": False, "answers": [{"text": "linguagem de programação", "answer_start": 15}]}]
                }
            ]
        }]
    }

    # Salvando os arquivos de teste
    with open("dataset_a.json", "w", encoding="utf-8") as f: json.dump(arquivo1, f)
    with open("dataset_b.json", "w", encoding="utf-8") as f: json.dump(arquivo2, f)
"""

    fazer_merge_squad(
        arquivo_principal="merge2_dataset.json", 
        arquivo_novo="quarto_dataset.json", 
        arquivo_saida="merge3_dataset.json"
    )