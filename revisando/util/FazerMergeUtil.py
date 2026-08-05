import json
import os

def normalizar_texto(texto):
    return " ".join(texto.strip().lower().split())

def fazer_merge_squad(arquivo_principal, arquivo_novo, arquivo_saida):

    
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
        