import os
from PIL import Image
import argparse

# Função para calcular as dimensões com base no DPI
def calculate_dimensions(dpi):
    # Tamanho de uma carta Magic em pixels (com base no DPI)
    card_width = 758 * dpi / 300  # Aumenta a largura proporcionalmente ao DPI
    card_height = 1020 * dpi / 300  # Aumenta a altura proporcionalmente ao DPI
    
    # Tamanho de uma folha A4 em pixels (com base no DPI)
    a4_width = 2480 * dpi / 300  # Aumenta a largura da folha proporcionalmente ao DPI
    a4_height = 3508 * dpi / 300  # Aumenta a altura da folha proporcionalmente ao DPI
    
    return card_width, card_height, a4_width, a4_height

# Função para redimensionar a carta
def resize_card(image_path, card_width, card_height):
    with Image.open(image_path) as img:
        # Redimensiona a imagem para o tamanho da carta com base no DPI
        img = img.resize((int(card_width), int(card_height)), Image.LANCZOS)
        return img

# Função para colocar cartas na folha A4
def arrange_cards_on_a4(card_images, output_path, card_width, card_height, a4_width, a4_height, margin_x, margin_y, space_x, space_y):
    # Cria uma nova imagem em branco (branco é o fundo da folha A4)
    a4_image = Image.new("RGB", (int(a4_width), int(a4_height)), (255, 255, 255))
    
    # Calcula quantas cartas cabem em cada linha e coluna
    cards_per_row = (a4_width - 2 * margin_x) // (card_width + space_x)
    cards_per_column = (a4_height - 2 * margin_y) // (card_height + space_y)
    
    # Coloca as cartas na folha A4
    x_offset = margin_x
    y_offset = margin_y
    for i, card_image in enumerate(card_images):
        if i > 0 and i % cards_per_row == 0:
            # Nova linha
            x_offset = margin_x
            y_offset += card_height + space_y
        
        # Cola a imagem da carta na posição correta
        a4_image.paste(card_image, (int(x_offset), int(y_offset)))
        x_offset += card_width + space_x
    
    # Salva a imagem final como PNG
    a4_image.save(output_path)

# Função principal para gerar múltiplas páginas
def generate_magic_cards_on_a4(images_folder, output_folder, dpi):
    # Calcula as dimensões com base no DPI fornecido
    card_width, card_height, a4_width, a4_height = calculate_dimensions(dpi)
    
    # Definindo as margens e espaçamento
    margin_x = 50 * dpi / 300
    margin_y = 50 * dpi / 300
    space_x = 10 * dpi / 300
    space_y = 10 * dpi / 300
    
    # Lista de arquivos de imagem na pasta
    card_images = []
    
    for file_name in os.listdir(images_folder):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            card_image_path = os.path.join(images_folder, file_name)
            resized_card = resize_card(card_image_path, card_width, card_height)
            card_images.append(resized_card)
    
    # Calcula quantas páginas serão necessárias
    total_cards = len(card_images)
    cards_per_page = ((a4_width - 2 * margin_x) // (card_width + space_x)) * ((a4_height - 2 * margin_y) // (card_height + space_y))
    num_pages = (total_cards + cards_per_page - 1) // cards_per_page  # arredonda para cima
    
    # Gera uma página A4 para cada conjunto de cartas
    for page_num in range(num_pages):
        start_idx = page_num * cards_per_page
        end_idx = min((page_num + 1) * cards_per_page, total_cards)
        
        # Cartas para essa página
        page_cards = card_images[start_idx:end_idx]
        
        # Caminho para salvar a página
        output_path = os.path.join(output_folder, f"magic_cards_page_{page_num + 1}.png")
        arrange_cards_on_a4(page_cards, output_path, card_width, card_height, a4_width, a4_height, margin_x, margin_y, space_x, space_y)
        print(f'Página {page_num + 1} gerada: {output_path}')

# Função para processar os argumentos de linha de comando
def parse_arguments():
    parser = argparse.ArgumentParser(description="Gerar páginas de cartas Magic em PNG com base no DPI.")
    parser.add_argument('dpi', type=int, help="Defina o DPI para o redimensionamento das cartas e da folha A4 (ex: 300, 600)")
    parser.add_argument('images_folder', type=str, help="Caminho da pasta com as imagens das cartas.")
    parser.add_argument('output_folder', type=str, help="Caminho da pasta para salvar os arquivos PNG gerados.")
    return parser.parse_args()

# Exemplo de uso:
if __name__ == "__main__":
    args = parse_arguments()
    
    # Cria a pasta de saída se não existir
    os.makedirs(args.output_folder, exist_ok=True)
    
    generate_magic_cards_on_a4(args.images_folder, args.output_folder, args.dpi)
