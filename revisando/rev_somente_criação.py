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


if __name__ == "__main__":
    criar_dataset_squad()