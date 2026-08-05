import tkinter as tk

def acao_botao():
    print("Botao clicado")

janela = tk.Tk()
janela.title("minha janela")
janela.geometry("300x200")

rotulo = tk.Label(janela, text = "bem vindo")
rotulo.pack(pady=20)

botao = tk.Button(janela, text="clica", command=acao_botao)
botao.pack()

janela.mainloop()

#camada dde interface

#camada controle de interface(para as funções)

#camada service regras de negocio

#camada model