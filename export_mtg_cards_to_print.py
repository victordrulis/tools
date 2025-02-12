from PIL import Image
import os

# Tamanho de uma carta Magic em pixels (300 DPI)
CARD_WIDTH = 758
CARD_HEIGHT = 1020

# Tamanho de uma folha A4 em pixels (300 DPI)
A4_WIDTH = 2480
A4_HEIGHT = 3508

# Margens e espaçamento entre as cartas
MARGIN_X = 50
MARGIN_Y = 50
SPACE_X = 10
SPACE_Y = 10

# Função para redimensionar a carta
def resize_card(image_path):
    with Image.open(image_path) as img:
        # Redimensiona para o tamanho da carta Magic
        img = img.resize((CARD_WIDTH, CARD_HEIGHT), Image.LANCZOS)
        return img

# Função para colocar cartas na folha A4
def arrange_cards_on_a4(card_images, output_path):
    # Cria uma nova imagem em branco (branco é o fundo da folha A4)
    a4_image = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), (255, 255, 255))
    
    # Calcula quantas cartas cabem em cada linha e coluna
    cards_per_row = (A4_WIDTH - 2 * MARGIN_X) // (CARD_WIDTH + SPACE_X)
    cards_per_column = (A4_HEIGHT - 2 * MARGIN_Y) // (CARD_HEIGHT + SPACE_Y)
    
    # Coloca as cartas na folha A4
    x_offset = MARGIN_X
    y_offset = MARGIN_Y
    for i, card_image in enumerate(card_images):
        if i > 0 and i % cards_per_row == 0:
            # Nova linha
            x_offset = MARGIN_X
            y_offset += CARD_HEIGHT + SPACE_Y
        
        # Cola a imagem da carta na posição correta
        a4_image.paste(card_image, (x_offset, y_offset))
        x_offset += CARD_WIDTH + SPACE_X
    
    # Salva a imagem final como PNG
    a4_image.save(output_path)

# Função principal para gerar múltiplas páginas
def generate_magic_cards_on_a4(images_folder, output_folder):
    # Lista de arquivos de imagem na pasta
    card_images = []
    
    for file_name in os.listdir(images_folder):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            card_image_path = os.path.join(images_folder, file_name)
            resized_card = resize_card(card_image_path)
            card_images.append(resized_card)
    
    # Calcula quantas páginas serão necessárias
    total_cards = len(card_images)
    cards_per_page = ((A4_WIDTH - 2 * MARGIN_X) // (CARD_WIDTH + SPACE_X)) * ((A4_HEIGHT - 2 * MARGIN_Y) // (CARD_HEIGHT + SPACE_Y))
    num_pages = (total_cards + cards_per_page - 1) // cards_per_page  # arredonda para cima
    
    # Gera uma página A4 para cada conjunto de cartas
    for page_num in range(num_pages):
        start_idx = page_num * cards_per_page
        end_idx = min((page_num + 1) * cards_per_page, total_cards)
        
        # Cartas para essa página
        page_cards = card_images[start_idx:end_idx]
        
        # Caminho para salvar a página
        output_path = os.path.join(output_folder, f"magic_cards_page_{page_num + 1}.png")
        arrange_cards_on_a4(page_cards, output_path)
        print(f'Página {page_num + 1} gerada: {output_path}')

# Exemplo de uso
images_folder = 'imagens_cartas'  # Pasta com as imagens das cartas
output_folder = 'saida'  # Pasta para salvar os arquivos PNG gerados
os.makedirs(output_folder, exist_ok=True)

generate_magic_cards_on_a4(images_folder, output_folder)
