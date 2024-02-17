from googlesearch import search
import webbrowser

class Searchft2:
    '''
    Classe onde estão contido os metodos dessa biblioteca
    '''
    def pesquisar(pesquisar: str, size = 10):
        '''
        Metodo de pesquisa onde tem como entrada
        uma string de pesquisa e opcionalmente a quantidade
        de links para ser retornada
        retorna os links mais relevantes do item pesquisado 
        direto pelo terminal.
        '''
        resultado = []
        
        for url in search(pesquisar, stop=size, lang="pt"):
            resultado.append(url)
       
        return resultado

    def visitarLink(link: str):
        '''
        Metodo para acessar um link de forma direta.
        Ao inserir um link ira abrir uma janela no seu navegador
        com o link que foi insedo.
        '''
        webbrowser.open(link)
    
    def pesquisarProduto(produto: str, site = "mercadolivre"):
        '''
        Metodo que ira pesquisar por um produto 
        A entrada é uma string que é o produto e a segunda entrada, opcional,
        é o site onde quer realizar a busca, que por padrão é o mercado livre.
        '''
        pesquisa = site+"/" + produto
        resultado = []
        for url in search(pesquisa, stop=10, lang="pt"):
            resultado.append(url)
        
        return resultado
    
