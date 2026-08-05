import tkinter as tk

import controller.SelecionarTarefaController

if __name__ == "__main__":

    botao_apertado = controller.SelecionarTarefaController.selecionarTarefa()

    janela = tk.Tk()
    janela.title("Selecionar Tarefa")
    janela.geometry("300x200")

    rotulo = tk.Label(janela, text="Escolha uma tarefa")
    rotulo.pack(pady=20)

    botao = tk.Button(janela, text="Criar Novo Dataset", command=botao_apertado.clicar)
    botao.pack()
    janela.mainloop()