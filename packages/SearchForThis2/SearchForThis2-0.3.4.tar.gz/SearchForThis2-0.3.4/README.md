# Descrição
A `SearchForThis2` é uma biblioteca que efetua pesquisas em motores de busca na web.

# Funcionalidades
* Realizar buscas por conteúdos desejados
* Acessar links retornados

# Biblioteca
### Instalação
```python
pip install SearchForThis2
```
### Importação
```python
import SearchForThis2
```
### Formas de utilização
```python
search = SearchForThis2.Searchft
```
`Ou`
```python
from SearchForThis2 import SearchForThis2 
```

### Acessando métodos
Uma das formas de acessar os métodos da classe, é a seguinte:
```python
Searchft2.method()
```
Onde `method`, é o nome método que você deseja utilizar.

### Realizando buscas:
Use o método `pesquisar` da classe, da seguinte forma:
```python
resultado = SearchForThis2.Searchft2.pesquisar(conteúdo_da_busca, size)
```
A variável size, armazena a quantidade de links que você deseja buscar. O conteúdo da busca deve ser uma string.

### Visitando links
Use o método `visitarLink`, da seguinte forma:
```python
SearchForThis2.Searchft2.visitarLink(link)
```
O link deve ser uma string.

### Realizando buscas por produtos:
Use o método `pesquisarProduto` da classe, da seguinte forma:
```python
resultado = SearchForThis2.Searchft2.pesquisarProduto(conteúdo_da_busca, plataforma_de_venda)
```
A variável conteúdo_da_busca, armazena o produto que você deseja buscar. E a variável plataforma_de_venda a plataforma em que será feita a busca pelo produto.

# Exemplos de uso

### Pesquisar
SearchForThis2.Searchft2.pesquisar("Ano do dragão")
SearchForThis2.Searchft2.pesquisar("Ano do dragão",10)

### VisitarLink
SearchForThis2.Searchft2.visitarLink("google.com")

### PesquisarProduto
SearchForThis2.Searchft2.pesquisarProduto("Tenis")
SearchForThis2.Searchft2.pesquisarProduto("Tenis", "aliexpress")
