import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

# This app treats images, removing noise, adjust saturation, white balance, etc.
# Just enter the source folder and destination folder as arguments.
# Prerequisites: 
#   - python 3
#   - pip
# Istall: 
#   - pyhton3-pillow
#   - python3-opencv
#   - numpy

# Função para aumentar a resolução
def aumentar_resolucao(imagem, escala=2):
    largura, altura = imagem.size
    imagem_ampliada = imagem.resize((largura * escala, altura * escala), Image.Resampling.LANCZOS)
    return imagem_ampliada

# Função para reduzir o ruído da imagem
def reduzir_ruido(imagem):
    imagem_cv = np.array(imagem)
    imagem_denoised = cv2.fastNlMeansDenoisingColored(imagem_cv, None, 10, 10, 7, 21)
    return Image.fromarray(imagem_denoised)

# Função para ajustar o brilho e o contraste
def ajustar_brilho_contraste(imagem, brilho=1.1, contraste=0.85):
    enhancer = ImageEnhance.Brightness(imagem)
    imagem_brilhante = enhancer.enhance(brilho)
    
    enhancer = ImageEnhance.Contrast(imagem_brilhante)
    imagem_final = enhancer.enhance(contraste)
    
    return imagem_final

# Ajustar saturacao
def ajustar_saturacao(imagem, fator=1.2):
    enhancer = ImageEnhance.Color(imagem)
    imagem_saturada = enhancer.enhance(fator)
    return imagem_saturada

# Balanceamento de cor
def ajustar_balanceamento_cor(imagem, r_factor=1.0, g_factor=1.0, b_factor=1.0):
    # Converter a imagem para um array numpy
    imagem_np = np.array(imagem)
    
    # Ajustar os canais RGB
    imagem_np[:, :, 0] = np.clip(imagem_np[:, :, 0] * r_factor, 0, 255)  # Red
    imagem_np[:, :, 1] = np.clip(imagem_np[:, :, 1] * g_factor, 0, 255)  # Green
    imagem_np[:, :, 2] = np.clip(imagem_np[:, :, 2] * b_factor, 0, 255)  # Blue
    
    return Image.fromarray(imagem_np)

# Aplicar blur
def aplicar_blur(imagem, raio=2):
    imagem_blur = imagem.filter(ImageFilter.GaussianBlur(radius=raio))
    return imagem_blur

# Função para processar as imagens de uma pasta
def processar_imagens(input_dir, output_dir):
    # Criar a pasta de saída, se não existir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Percorrer todos os arquivos na pasta de entrada
    for nome_arquivo in os.listdir(input_dir):
        if nome_arquivo.endswith(".jpg"):
            caminho_entrada = os.path.join(input_dir, nome_arquivo)
            caminho_saida = os.path.join(output_dir, nome_arquivo)
            
            # Carregar a imagem
            imagem = Image.open(caminho_entrada)
            
            # Aumentar resolução
            imagem_resolucao = aumentar_resolucao(imagem, escala=2)
            
            # Reduzir o ruído
            imagem_sem_ruido = reduzir_ruido(imagem_resolucao)
            
            # Ajustar saturacao
            imagem_saturacao = ajustar_saturacao(imagem_sem_ruido)
            
            # Balanceamento de cor
            imagem_cor_balanceada = ajustar_balanceamento_cor(imagem_saturacao)

            # Ajustar brilho e contraste
            # imagem_final = ajustar_brilho_contraste(imagem_sem_ruido)

            # Aplicar blur
            # imagem_com_blur = aplicar_blur(imagem_cor_corrigida)

            # Salvar a imagem processada na pasta de saída
            imagem_cor_balanceada.save(caminho_saida)

            print(f"Imagem processada e salva em: {caminho_saida}")

# Definir os diretórios de entrada e saída
input_dir = '/path/to/source/images'
output_dir = '/path/to/output/folder'

# Processar as imagens
processar_imagens(input_dir, output_dir)
