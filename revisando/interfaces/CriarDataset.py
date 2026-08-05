import tkinter as tk

import controller.CriarDatasetController
import model.DatasetModel

if __name__ == "__main__":

    def func_botao_titulo():

        item.titulo = entrada_titulo.get()
        ctrl.FazerTItulo(item.titulo)

    def func_botao_contexto():

        item.contexto = entrada_contexto.get()
        ctrl.FazerContexto(item.contexto)
        

    def func_botao_pr():

        item.pergunta = entrada_pergunta.get()
        item.resposta = entrada_resposta.get()
        item.impossivel = check_var.get()

        ctrl.FazerPerguntaResposta(item.pergunta, item.resposta, item.contexto, item.impossivel, item.titulo)

        entrada_pergunta.delete(0, tk.END)
        entrada_resposta.delete(0, tk.END)
        

    def func_fechar_contexto():

        entrada_contexto.delete(0, tk.END)
        # Reseta a checkbox para False (desmarcada)
        check_var.set(False)

        ctrl.FecharContexto()

    def func_fechar_dataset():

        entrada_titulo.delete(0, tk.END)

        ctrl.FecharDataset()
        print(ctrl.printar())

    def func_salvar():

        ctrl.Salvar(entrada_salvar.get())
        

    ctrl = controller.CriarDatasetController.CriarDatasetController()
    item = model.DatasetModel.Dataset()

    janela = tk.Tk()
    janela.title("Selecionar Tarefa")
    janela.geometry("800x800")

    ctrl.FazerBase()

    #titulo

    label_titulo = tk.Label(janela, text = "Digite um titulo:")
    label_titulo.pack(pady=5)

    entrada_titulo = tk.Entry(janela, width=30)
    entrada_titulo.pack(pady=5)

    botao_titulo = tk.Button(janela, text="Definir Titulo", command=func_botao_titulo)
    botao_titulo.pack(pady=10)

    #contexto

    label_contexto = tk.Label(janela, text = "Digite um Contexto:")
    label_contexto.pack(pady=5)

    entrada_contexto = tk.Entry(janela, width=60)
    entrada_contexto.pack(pady=5)

    botao_contexto = tk.Button(janela, text="Definir Contexto", command=func_botao_contexto)
    botao_contexto.pack(pady=10)

    #perguntas e respostas

    label_pergunta = tk.Label(janela, text = "Digite uma pergunta:")
    label_pergunta.pack(pady=5)
    
    entrada_pergunta = tk.Entry(janela, width=60)
    entrada_pergunta.pack(pady=5)

    check_var = tk.BooleanVar(value=False) # Inicia desmarcada (False)
    checkbox = tk.Checkbutton(janela, text="pergunta impossível", variable=check_var)
    checkbox.pack(pady=5)

    label_resposta = tk.Label(janela, text = "Digite uma resposta:")
    label_resposta.pack(pady=5)
    
    entrada_resposta = tk.Entry(janela, width=60)
    entrada_resposta.pack(pady=5)

    botao_pr = tk.Button(janela, text="Definir Pergunta e Resposta", command=func_botao_pr)
    botao_pr.pack(pady=10)

    #fechar contexto

    botao_fechar_contexto = tk.Button(janela, text="Concluir contexto", command=func_fechar_contexto)
    botao_fechar_contexto.pack(pady=10)

    #fechar dataset

    botao_fechar_dataset = tk.Button(janela, text="Concluir Dataset", command=func_fechar_dataset)
    botao_fechar_dataset.pack(pady=10)
    
    #salvar

    label_salvar = tk.Label(janela, text = "Informe o caminho e nome do arquivo:")
    label_salvar.pack(pady=5)

    entrada_salvar = tk.Entry(janela, width=60)
    entrada_salvar.pack(pady=5)

    botao_salvar = tk.Button(janela, text="Salvar Dataset", command=func_salvar)
    botao_salvar.pack(pady=10)

    janela.mainloop()