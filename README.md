# tools
Tools to make everyday work easier


# Geração de Múltiplas Páginas para Impressão de Cartas de TCG
### (export_mtg_card_to_print.py)

Este script Python permite redimensionar imagens das cartas de TCG, ajustá-las ao tamanho oficial das cartas e distribuí-las em páginas A4, com marcações e espaçamento adequados para impressão e corte.

## O que o código faz

1. **Redimensionamento das Cartas**: A função `resize_card()` redimensiona cada imagem de carta para o tamanho padrão de uma carta de TCG (758x1020 pixels), mantendo a qualidade de imagem.
   
2. **Distribuição das Cartas na Página A4**: A função `arrange_cards_on_a4()` organiza as cartas dentro de uma folha A4 (2480x3508 pixels). As cartas são posicionadas com base nas margens e espaçamentos configuráveis.

3. **Geração de Múltiplas Páginas**: A função principal `generate_magic_cards_on_a4()` divide o total de cartas em várias páginas A4, gerando um arquivo PNG para cada página. Cada página é numerada automaticamente (ex: `magic_cards_page_1.png`, `magic_cards_page_2.png`, etc.).

## Detalhes Importantes

- **Tamanho das Cartas**: O tamanho de cada carta de Magic foi definido como 758x1020 pixels, que corresponde ao tamanho oficial de uma carta a 300 DPI.
- **Tamanho da Folha A4**: A folha A4 tem o tamanho de 2480x3508 pixels a 300 DPI. Esse é o tamanho que será usado para a impressão.
- **Margens e Espaçamento**: As margens e o espaçamento entre as cartas podem ser ajustados. As margens padrão são de 50 pixels para a posição X (horizontal) e 50 pixels para a posição Y (vertical), com um espaçamento de 10 pixels entre as cartas.
  
- **Cálculo de Múltiplas Páginas**: O código calcula automaticamente quantas páginas A4 serão necessárias para acomodar todas as cartas. As cartas serão organizadas nas páginas de acordo com a quantidade máxima de cartas que podem caber em uma única página, com base no tamanho das cartas e nas margens configuradas.

## Ajustes

- **MARGENS**: Você pode ajustar as margens horizontais (`MARGIN_X`) e verticais (`MARGIN_Y`) para alterar o espaço ao redor das cartas na página.
- **ESPAÇAMENTO ENTRE AS CARTAS**: O espaçamento entre as cartas na direção horizontal (`SPACE_X`) e vertical (`SPACE_Y`) pode ser ajustado de acordo com sua preferência.
- **Resolução das Imagens**: O código assume que as imagens das cartas têm uma boa resolução. Caso as imagens originais sejam menores ou de resolução inferior, o redimensionamento pode resultar em perda de qualidade, mas o código mantém a qualidade ao redimensionar com o método `LANCZOS`, que preserva os detalhes ao reduzir o tamanho da imagem.

## Como usar

1. Coloque as imagens das cartas de TCG na pasta `imagens_cartas`.
2. Rode o script. Ele gerará as imagens das páginas A4 com as cartas organizadas para impressão na pasta `saida`.
3. O arquivo PNG gerado para cada página será nomeado como `magic_cards_page_1.png`, `magic_cards_page_2.png`, etc.

### Exemplo de uso:
```python
images_folder = 'imagens_cartas'  # Pasta com as imagens das cartas
output_folder = 'saida'  # Pasta para salvar os arquivos PNG gerados
os.makedirs(output_folder, exist_ok=True)

generate_magic_cards_on_a4(images_folder, output_folder)
```


# Explicação das modificações:
## Função calculate_dimensions(dpi):

Calcula automaticamente o tamanho das cartas e da folha A4 com base no valor do DPI fornecido.
Para cada DPI, as dimensões das cartas e da folha A4 são escaladas proporcionalmente.
## Função resize_card(image_path, card_width, card_height):

Agora, recebe as dimensões calculadas com base no DPI para redimensionar as cartas para o tamanho correto.
## Função arrange_cards_on_a4():

Foi modificada para usar as novas dimensões da carta e da folha A4 calculadas com base no DPI.
Ajusta a organização das cartas na folha A4 de acordo com o novo tamanho.
## Uso de argparse:

A função parse_arguments() usa o módulo argparse para permitir que o usuário forneça os argumentos de DPI, caminho da pasta com as imagens das cartas e caminho da pasta de saída diretamente pela linha de comando.

Ao executar o script, o usuário poderá passar o valor do DPI, e o código irá gerar as páginas com base no DPI fornecido.
## Como rodar:
Agora, você pode executar o script da seguinte forma:

```bash
python gerar_cartas.py 600 imagens_cartas saida
```
### Onde:
- 600 é o DPI desejado.
- imagens_cartas é o diretório com as imagens das cartas.
- saida é o diretório onde os arquivos PNG gerados serão salvos.
### Resultado:
O script gerará páginas A4 com cartas redimensionadas para o DPI especificado, e a quantidade de cartas por página será calculada automaticamente, de acordo com o DPI e as dimensões da folha A4.