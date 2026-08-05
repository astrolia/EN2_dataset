import dao.DatasetDAO

class DatasetService:
    def __init__(self):
        self.datasetDAO = dao.DatasetDAO.DatasetDAO()


    def printar(self):

        return self.datasetDAO.printar()

    def Base(self):

        self.datasetDAO.CriarBase()

    def Titulo(self, titulo):

        if titulo == "":

            print("um titulo deve ser inserido")

        else:

            self.datasetDAO.CriarTitulo(titulo);

    def Contexto(self, contexto):

        if contexto == "":

            print("um contexto deve ser inserido")

        else:

            self.datasetDAO.CriarContexto(contexto);

    def PerguntaResposta(self, pergunta, resposta, contexto, impossivel, titulo):

        inicio_resposta = contexto.find(resposta)


        if inicio_resposta == -1:

            print("a resposta não está presente no contexto")

        else:

            self.datasetDAO.CriarPerguntaResposta(pergunta, resposta, impossivel, titulo, inicio_resposta)

    def ConcluirContexto(self):

        self.datasetDAO.FecharContexto()

    def ConcluirDataset(self):

        self.datasetDAO.FecharDataset()

    def Salvar(self, nome_arquivo):

        if not nome_arquivo.endswith('.json'):
                nome_arquivo += '.json'

        self.datasetDAO.SalvarDataset(nome_arquivo)





