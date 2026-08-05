import tkinter as tk

import util.FazerMergeUtil

if __name__ == "__main__":

    def func_merge():

        util.FazerMergeUtil.fazer_merge_squad(entrada_arq1.get(), entrada_arq2.get(), entrada_saida.get())

    janela = tk.Tk()
    janela.title("Selecionar Tarefa")
    janela.geometry("800x800")

    label_arq1 = tk.Label(janela, text = "Caminho do Arquivo 1:")
    label_arq1.pack(pady=5)

    entrada_arq1 = tk.Entry(janela, width=60)
    entrada_arq1.pack(pady=5)

    label_arq2 = tk.Label(janela, text = "Caminho do Arquivo 2:")
    label_arq2.pack(pady=5)

    entrada_arq2 = tk.Entry(janela, width=60)
    entrada_arq2.pack(pady=5)

    label_saida = tk.Label(janela, text = "Caminho da saida:")
    label_saida.pack(pady=5)

    entrada_saida = tk.Entry(janela, width=60)
    entrada_saida.pack(pady=5)

    botao_arq = tk.Button(janela, text="Fazer Merge", command=func_merge)
    botao_arq.pack(pady=10)


    janela.mainloop()