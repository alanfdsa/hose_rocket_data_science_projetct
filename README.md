# house_rocket_data_analysis

#  Introdução
House Rocket é uma empresa fictícia que trabalha com compra e venda. Quer encontrar as melhores oportunidades de negócio e a estratégia é comprar casas em ótimas condições a preços baixos e vender as propriedades com preços mais elevados. Os atributos das casas as tornam mais ou menos atrativas, influenciando na atratividade dos imóveis e consequentemente no seu preço.
Logo, as questões que guiam o estudo é que imóveis a empresa deve comprar e por qual preço e qual é o melhor momento para o vender pelo melhor preço.

#  Dataset

 * Baixado do site: https://www.kaggle.com/harlfoxem/housesalesprediction<br>
 
## As variáveis do dataset original são:

Variável | Definição
------------ | -------------
|id | Identificador de cada propriedade.|
|date | Data em que a propriedade ficou disponível.|
|price | O preço de cada imóvel, considerado como preço de compra.|
|bedrooms | Número de quartos.|
|bathrooms | O número de banheiros, o valor 0,5 indica um quarto com banheiro, mas sem chuveiro. O valor 0,75 ou 3/4 banheiro representa um banheiro que contém uma pia, um vaso sanitário e um chuveiro ou banheira.|
|sqft_living | Pés quadrados do interior das casas.|
|sqft_lot | Pés quadrados do terreno das casas.|
|floors | Número de andares.|
|waterfront | Uma variável fictícia para saber se a casa tinha vista para a orla ou não, '1' se a propriedade tem uma orla, '0' se não.|
|view | Vista, Um índice de 0 a 4 de quão boa era a visualização da propriedade.|
|condition | Um índice de 1 a 5 sobre o estado das moradias, 1 indica propriedade degradada e 5 excelente.|
|grade | Uma nota geral é dada à unidade habitacional com base no sistema de classificação de King County. O índice de 1 a 13, onde 1-3 fica aquém da construção e design do edifício, 7 tem um nível médio de construção e design e 11-13 tem um nível de construção e design de alta qualidade.|
|sqft_above | Os pés quadrados do espaço habitacional interior acima do nível do solo.|
|sqft_basement | Os pés quadrados do espaço habitacional interior abaixo do nível do solo.|
|yr_built | Ano de construção da propriedade.|
|yr_renovated | Representa o ano em que o imóvel foi reformado. Considera o número ‘0’ para descrever as propriedades nunca renovadas.|
|zipcode | Um código de cinco dígitos para indicar a área onde se encontra a propriedade.|
|lat | Latitude.|
|long | Longitude.|
|sqft_living15 | O tamanho médio em pés quadrados do espaço interno de habitação para as 15 casas mais próximas.|
|sqft_lot15 | Tamanho médio dos terrenos em metros quadrados para as 15 casas mais próximas.|

# Pastas e códigos

### AnotaçõesAulas.ipynb - anotações realizadas baseadas nas aulas

### CasasCompradas.ipynb - manipulação dos dados junto das hipóteses de negócio para decidir quais são as possíveis casas candidatas a se comprar.

### dados.csv - dados tratados e manipulados (com novas colunas)

### dados_port.csv - dados relevantes às possíveis casas candidatas para compra

### app/
Pasta que armazena os códigos para o aplicativo criado no streamlit e com os pré requisitos para fazer o deploy no Heroku
#### dashboard.py - visualização das informações das casas disponíveis para a compra
#### dashboard_port.py - visualização das informações das possíveis casas para comprar e seus respectivos preços de vendas e lucro

### aulas/
Pasta destinada a armazenar as aulas ministradas e conteúdos relevantes

### midia/
Pasta destinada a demonstrar os resultados do projeto. Nesse caso os prints são do arquivo dashboard.py que se localiza na pasta app/
O outro aplicativo dashboard_port.py se destina a mostrar a mesma interface que o dasboard.py só que com as possíveis casas candidata.

#  Ferramentas

   * Jupyter notebook
   * Python
   * Pandas
   * Geopandas
   * Streamlit
   * Folium
   * Numpy
   * Heroku

# Etapas

   * Coleta dos dados via kaggle ()
   * Entendimento do objetivo da empresa
   * Limpeza dos dados
   * Processamento dos dados
   * Exploração dos dados
   * Criação do app com dashboards
   * Deploy no Heroku
 
