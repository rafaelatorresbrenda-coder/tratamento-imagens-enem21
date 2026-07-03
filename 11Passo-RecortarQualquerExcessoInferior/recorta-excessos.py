"""
Propósito: várias questões tem um rascunhozinho abaixo da questão. O objetivo deste código é encontrar esses rascunhos e recortá-los.
Autor: Alexandre Nassar de Peder
Criação: 02/10/2025
Atualização: 03/06/2026

OBS1: puxe a pasta "questoes" do passo 10 para este passo 11

OBS2: este código vai criar uma pasta de saída chamada "finalizadas"
OBS3: execute o código
"""

from PIL import Image
import os
import shutil

def encontrar_ultimo_pixel_cor(imagem, cor_alvo=(39, 39, 39), tolerancia=10):
    """
    Encontra o último pixel (mais inferior) com a cor alvo (#272727)
    Retorna a posição Y do último pixel encontrado ou None se não encontrar
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    
    ultimo_y = None
    
    # Percorre a imagem de baixo para cima
    for y in range(altura - 1, -1, -1):
        for x in range(largura):
            pixel = pixels[x, y]
            
            if len(pixel) == 4:  # RGBA
                r, g, b, a = pixel
            else:  # RGB
                r, g, b = pixel[:3]
            
            # Verifica se é cinza escuro (dentro da tolerância)
            if (abs(r - cor_alvo[0]) <= tolerancia and 
                abs(g - cor_alvo[1]) <= tolerancia and 
                abs(b - cor_alvo[2]) <= tolerancia):
                ultimo_y = y
                print(f"Último pixel com cor #272727 encontrado em y={ultimo_y}")
                return ultimo_y
    
    return None

def encontrar_primeiro_pixel_esquerda(imagem, cor_alvo=(58, 58, 58), tolerancia=10):
    """
    Encontra o primeiro pixel (mais à esquerda) com a cor alvo (#3a3a3a)
    Verifica da esquerda para a direita
    Retorna a posição X do primeiro pixel encontrado ou None se não encontrar
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    
    # Percorre a imagem da esquerda para a direita
    for x in range(largura):
        for y in range(altura):
            pixel = pixels[x, y]
            
            if len(pixel) == 4:  # RGBA
                r, g, b, a = pixel
            else:  # RGB
                r, g, b = pixel[:3]
            
            # Verifica se é cinza médio (dentro da tolerância)
            if (abs(r - cor_alvo[0]) <= tolerancia and 
                abs(g - cor_alvo[1]) <= tolerancia and 
                abs(b - cor_alvo[2]) <= tolerancia):
                # Volta 5 pixels
                posicao_corte = max(0, x - 5)
                print(f"Primeiro pixel com cor #3a3a3a encontrado em x={x}, cortando em x={posicao_corte}")
                return posicao_corte
    
    return None

def encontrar_ultimo_pixel_direita(imagem, cor_alvo=(58, 58, 58), tolerancia=10):
    """
    Encontra o último pixel (mais à direita) com a cor alvo (#3a3a3a)
    Verifica da direita para a esquerda
    Retorna a posição X do último pixel encontrado ou None se não encontrar
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    
    # Percorre a imagem da direita para a esquerda
    for x in range(largura - 1, -1, -1):
        for y in range(altura):
            pixel = pixels[x, y]
            
            if len(pixel) == 4:  # RGBA
                r, g, b, a = pixel
            else:  # RGB
                r, g, b = pixel[:3]
            
            # Verifica se é cinza médio (dentro da tolerância)
            if (abs(r - cor_alvo[0]) <= tolerancia and 
                abs(g - cor_alvo[1]) <= tolerancia and 
                abs(b - cor_alvo[2]) <= tolerancia):
                # Volta 5 pixels (para a esquerda)
                posicao_corte = min(largura, x + 6)  # +6 porque queremos cortar após o pixel + 5
                print(f"Último pixel com cor #3a3a3a encontrado em x={x}, cortando em x={posicao_corte}")
                return posicao_corte
    
    return None

def processar_imagens(pasta_origem, pasta_destino, cor_inferior=(39, 39, 39), cor_lateral=(58, 58, 58)):
    """
    Processa todas as imagens da pasta origem, recortando as que têm bordas
    e copiando todas para a pasta destino
    """
    # Cria a pasta de destino se não existir
    os.makedirs(pasta_destino, exist_ok=True)
    
    # Lista todos os arquivos da pasta origem
    arquivos = [f for f in os.listdir(pasta_origem) 
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]
    
    print(f"Encontrados {len(arquivos)} arquivos para processar")
    
    for arquivo in arquivos:
        caminho_origem = os.path.join(pasta_origem, arquivo)
        caminho_destino = os.path.join(pasta_destino, arquivo)
        
        try:
            # Abre a imagem
            with Image.open(caminho_origem) as imagem:
                print(f"\nProcessando: {arquivo} ({imagem.width}x{imagem.height})")
                
                # Inicializa as coordenadas de corte
                left = 0
                top = 0
                right = imagem.width
                bottom = imagem.height
                
                # 1. PROCURA PELA BORDA INFERIOR (#272727)
                ultimo_pixel_y = encontrar_ultimo_pixel_cor(imagem, cor_inferior)
                if ultimo_pixel_y is not None:
                    # Corta 10 pixels abaixo do último pixel encontrado
                    bottom = min(imagem.height, ultimo_pixel_y + 10)
                    print(f"  → Cortar inferior em y={bottom} (último pixel em {ultimo_pixel_y} + 10)")
                
                # 2. PROCURA PELA BORDA ESQUERDA (#3a3a3a)
                primeiro_pixel_x = encontrar_primeiro_pixel_esquerda(imagem, cor_lateral)
                if primeiro_pixel_x is not None:
                    left = primeiro_pixel_x
                    print(f"  → Cortar esquerda em x={left}")
                
                # 3. PROCURA PELA BORDA DIREITA (#3a3a3a)
                ultimo_pixel_x = encontrar_ultimo_pixel_direita(imagem, cor_lateral)
                if ultimo_pixel_x is not None:
                    right = ultimo_pixel_x
                    print(f"  → Cortar direita em x={right}")
                
                # Se alguma borda foi encontrada, recorta a imagem
                if (bottom < imagem.height or left > 0 or right < imagem.width):
                    # Garante que as coordenadas são válidas
                    left = max(0, left)
                    top = max(0, top)
                    right = min(imagem.width, right)
                    bottom = min(imagem.height, bottom)
                    
                    # Verifica se a área de corte é válida
                    if right > left and bottom > top:
                        area_corte = (left, top, right, bottom)
                        imagem_recortada = imagem.crop(area_corte)
                        imagem_recortada.save(caminho_destino)
                        print(f"✓ Imagem recortada: {imagem_recortada.width}x{imagem_recortada.height}")
                        print(f"  → Área cortada: ({left}, {top}, {right}, {bottom})")
                    else:
                        shutil.copy2(caminho_origem, caminho_destino)
                        print(f"✓ Área de corte inválida, copiando original")
                else:
                    # Se não encontrou borda, copia a imagem original
                    shutil.copy2(caminho_origem, caminho_destino)
                    print(f"✓ Imagem mantida original (sem borda detectada)")
                    
        except Exception as e:
            print(f"✗ Erro ao processar {arquivo}: {e}")
            # Tenta copiar o arquivo mesmo com erro
            try:
                shutil.copy2(caminho_origem, caminho_destino)
                print(f"✓ Arquivo copiado mesmo com erro")
            except:
                print(f"✗ Não foi possível copiar o arquivo")

# Função principal
if __name__ == "__main__":
    # Configurações
    pasta_origem = "./questoes"
    pasta_destino = "finalizadas"
    cor_272727 = (39, 39, 39)  # RGB para #272727
    cor_3a3a3a = (58, 58, 58)  # RGB para #3a3a3a
    
    print("Iniciando processamento de imagens...")
    print(f"Pasta origem: {pasta_origem}")
    print(f"Pasta destino: {pasta_destino}")
    print(f"Cor inferior: RGB{cor_272727} (#272727)")
    print(f"Cor lateral: RGB{cor_3a3a3a} (#3a3a3a)")
    print(f"Regras:")
    print(f"  - Inferior: encontrar último pixel #272727 e cortar 10 pixels abaixo")
    print(f"  - Esquerda: encontrar primeiro pixel #3a3a3a e voltar 5 pixels")
    print(f"  - Direita: encontrar último pixel #3a3a3a e cortar após 5 pixels")
    
    # Verifica se a pasta origem existe
    if not os.path.exists(pasta_origem):
        print(f"Erro: A pasta '{pasta_origem}' não existe!")
        exit(1)
    
    # Executa o processamento
    processar_imagens(pasta_origem, pasta_destino, cor_272727, cor_3a3a3a)
    
    print("\n" + "="*50)
    print("Processamento concluído!")
    print(f"Todas as imagens foram salvas em: {pasta_destino}")