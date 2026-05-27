import json
import os

def criar_dataset_squad():
    print("--- Gerador de Dataset SQuAD 2.0 ---")
    
    # Estrutura principal do SQuAD
    dataset = {
        "version": "v2.0",
        "data": []
    }
    
    # Solicita o título geral do tema/dataset
    titulo_tema = input("Digite o título geral do tema (ex: Historia_do_Brasil): ").strip()
    
    # Estrutura do tópico
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
            
            is_impossible_input = input("Esta pergunta é IMPOSSÍVEL de responder com base no texto? (s/n): ").strip().lower()
            is_impossible = True if is_impossible_input == 's' else False
            
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
                
                # Encontra o índice automaticamente no contexto
                answer_start = contexto.find(resposta_texto)
                
                if answer_start == -1:
                    print("⚠️ Alerta: A resposta digitada não foi encontrada exatamente igual no texto!")
                    print("Por favor, tente novamente para este campo.")
                    resposta_texto = input("Digite a resposta exata (letras maiúsculas/minúsculas importam): ").strip()
                    answer_start = contexto.find(resposta_texto)
                
                qa_dict["answers"].append({
                    "text": resposta_texto,
                    "answer_start": answer_start
                })
            else:
                # Pergunta Impossível (SQuAD 2.0 pede uma resposta plausível opcional)
                print("\n[Opcional] Para perguntas impossíveis, você pode sugerir uma resposta 'plausível' (que parece certa, mas está errada).")
                quer_plausivel = input("Deseja adicionar uma resposta plausível? (s/n): ").strip().lower()
                
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
        
    print(f"\n» Sucesso! Dataset salvo com sucesso em: {os.path.abspath(nome_arquivo)}")


def normalizar_texto(texto):
    """
    Remove espaços extras e padroniza o texto para evitar que 
    pequenas diferenças de digitação (como um espaço no fim) criem duplicatas.
    """
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

    # Dicionário auxiliar para mapear: contexto_normalizado -> dict_do_paragrafo_original
    # Isso acelera a busca e evita loops complexos repetitivos
    mapa_contextos = {}
    
    # Como o SQuAD tem uma lista 'data' com vários tópicos/títulos, 
    # vamos assumir o primeiro tópico para mapeamento (ou unificar se os títulos forem iguais)
    # Para este algoritmo, vamos indexar todos os contextos existentes na base
    for topico in base_data.get("data", []):
        for paragrafo in topico.get("paragraphs", []):
            ctx_normalizado = normalizar_texto(paragrafo["context"])
            mapa_contextos[ctx_normalizado] = paragrafo

    # Se a base estiver vazia, pegamos a estrutura do novo arquivo
    if not base_data.get("data"):
        base_data["data"] = [{"title": "Dataset_Merged", "paragraphs": []}]
    
    # Garantimos que temos pelo menos um tópico alvo para adicionar novos contextos
    alvo_topico = base_data["data"][0]

    # 3. Processa o novo arquivo e faz a fusão
    contador_novas_perguntas = 0
    contador_novos_contextos = 0

    for topico_novo in novo_data.get("data", []):
        for paragrafo_novo in topico_novo.get("paragraphs", []):
            ctx_novo_norm = normalizar_texto(paragrafo_novo["context"])
            
            # CASO 1: O contexto já existe na base! (Fusão de perguntas)
            if ctx_novo_norm in mapa_contextos:
                paragrafo_existente = mapa_contextos[ctx_novo_norm]
                
                # Lista de IDs já existentes para evitar duplicar a MESMA pergunta
                ids_existentes = {qa["id"] for qa in paragrafo_existente["qas"]}
                
                for qa_nova in paragrafo_novo["qas"]:
                    if qa_nova["id"] not in ids_existentes:
                        paragrafo_existente["qas"].append(qa_nova)
                        contador_novas_perguntas += 1
                    else:
                        # Se o ID já existir, mas você quiser garantir que mude caso seja diferente, 
                        # podemos gerar um sufixo, mas por padrão o SQuAD exige IDs únicos.
                        qa_nova["id"] = f"{qa_nova['id']}_dup"
                        paragrafo_existente["qas"].append(qa_nova)
                        contador_novas_perguntas += 1
            
            # CASO 2: O contexto é inédito! (Concatenado no final)
            else:
                alvo_topico["paragraphs"].append(paragrafo_novo)
                # Atualiza o mapa caso o próprio novo arquivo tenha contextos repetidos dele mesmo
                mapa_contextos[ctx_novo_norm] = paragrafo_novo
                contador_novos_contextos += 1
                contador_novas_perguntas += len(paragrafo_novo["qas"])

    # 4. Salva o resultado final
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        json.dump(base_data, f, ensure_ascii=False, indent=2)
        
    print("\n--- Merge Concluído ---")
    print(f"Contextos inéditos adicionados: {contador_novos_contextos}")
    print(f"Total de perguntas inseridas/fundidas: {contador_novas_perguntas}")
    print(f"Arquivo salvo com sucesso em: {arquivo_saida}")

# --- EXEMPLO DE USO ---
if __name__ == "__main__":
    # Criando dois arquivos JSON fictícios para demonstrar o funcionamento
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
                    # Mesmo contexto (com uma pequena variação de espaço/maíuscula para testar a robustez)
                    "context": "  A inteligência artificial é o futuro da tecnologia. ",
                    "qas": [{"id": "q2", "question": "Do que a IA é o futuro?", "is_impossible": False, "answers": [{"text": "da tecnologia", "answer_start": 37}]}]
                },
                {
                    # Contexto completamente novo
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
    # Executando a função de Merge
    fazer_merge_squad(
        arquivo_principal="merge2_dataset.json", 
        arquivo_novo="quarto_dataset.json", 
        arquivo_saida="merge3_dataset.json"
    )