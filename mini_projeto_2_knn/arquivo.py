class Client:
    """Essa classe é utilizada para guardar e manipular dados de clientes
    Recebe como entrada uma lista com CPF, perfil de investimento e uma
    carteira em formato de lista com qualquer numero de investimentos
    no formato: [str "CPF", str "perfil", list "carteira"].
    
    Adicionalmente inicializa uma lista de distancias e vizinhos a ser 
    usada no formato: [float "distancia", int "indice"] como vazia até 
    calcular a distancia até algum vizinho por um dos metodos de
    calculo de distancia.
    """

    def __init__(self, c):
        """Entrada: lista com CPF, perfil de investimento e uma carteira 
        em formato de lista com qualquer numero de investimentos no 
        formato: [str "CPF", str "perfil", list "carteira"].
        
        Adicionalmente inicializa uma lista de distancias e vizinhos a 
        ser usada no formato: [float "distancia", int "indice"] como 
        vazia até calcular a distancia até algum vizinho por um dos 
        metodos de calculo de distancia.
        """
        self.cpf = c[0]
        self.perfil = c[1]
        self.carteira = c[2]
        self.vizinhos = []

    def calc_dist_lst(self, indice, outro):
        """Calcula distancia euclidiana em relação a outro cliente em 
        formato de lista e atualiza distancia e indice do vizinho em
        "vizinhos".
        
        Entrada: indice do vizinho a calcular a distancia e lista com 
        dados de CPF, perfil e cartera do vizinho no formato: 
        int "indice", [str "CPF", str "perfil", list "carteira"]. 
        
        Saida: sem retorno, atualiza atributo lista "vizinhos" no formato:
        [float "distancia", int "indice"].
        """
        dist = 0
        temp_list = zip(self.carteira, outro[2])
        for i in temp_list:
            dist += (i[0] - i[1]) ** 2
        self.vizinhos.append([dist ** 0.5, indice])

    def calc_dist_cls(self, indice, outro_cliente):
        """Calcula distancia euclidiana em relação à outra instância de 
        classe cliente e atualiza distancia e indice do vizinho em "vizinhos".
        
        Entrada: indice do vizinho a calcular a distancia e outra instancia
        classe cliente no formato: int "indice", class "Cliente". 
        
        Saida: sem retorno, atualiza atributo lista "vizinhos" no formato:
        [float "distancia", int "indice"].
        """
        dist = 0
        temp_list = zip(self.carteira, outro_cliente.carteira)
        for i in temp_list:
            dist += (i[0] - i[1]) ** 2
        self.vizinhos.append([dist ** 0.5, indice])

    def avalia_perfil(self, k, lista_class):
        """Avalia perfil com base em lista "vizinhos", numero de vizinhos 
        definido como "k" e lista de dados de classificados "lista_class";
        Reduz a lista "vizinhos" ao tamanho "k", busca os perfis nos dados
        classificados, conta cada um e retorna o maior atualizando o perfil.
        
        Entrada: int "k", list "lista_class" contendo em cada elemento outra
        lista com [str "CPF", str "perfil", list "carteira"].
        
        Saida: sem retorno, atualiza atributo str "perfil" com o perfil calculado.
        """
        self.vizinhos = sorted(self.vizinhos)[:k]
        temp_perfil = []
        for i, j in self.vizinhos:
            temp_perfil.append(lista_class[j][1])
        self.perfil = max(set(temp_perfil), key=temp_perfil.count)

    def add_to_dict(self, dicionario):
        """Adiciona o cliente a um dicionario para o resultado.
        
        Entrada: dict "dicionario" contendo o dicionario a ser atualizado.
        
        Saida: sem retorno, "dicionario" atualizado com adição instancia atual
        da classe cliente.
        """
        dicionario[self.cpf] = dict(
            perfil=self.perfil, carteira=self.carteira
        )
