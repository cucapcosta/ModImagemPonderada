# Modificador de Imagens - Ponderada Lucas Periquito

## Features

- Filtro Grey-Scale
- Blur
- Sharpen
- Detecção de Borda
- Inversão de Cores
- Aumento de contraste
- Modo psicodélico!
- Redimencionamento de imagem
- Rotações

## Sobre o Projeto

&emsp;Este projeto tem como objetivo o aprendizado sobre o uso do OpenCV2 para manipulação de imagens e do Streamlit para criação de web apps. Creio que a principal lição veio de como os modificadores afetam as imagens e as possíveis incompatibilidades e efeitos inesperados que podem causar; Filtros de tons de cinza como em:
```python
cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```
E
```
cv2.Canny(img, 100, 200)
```
&emsp;... Mudam o formato da matriz de cores, que podem causar erros ao usar filtros como psicodélico ou tentar aplicar grey scale novamente.
&emsp;Também houveram questões a serem resolvidas, como efeitos resultantes de resizing, problemas na rotação (que, fora em rotações de múltiplos de 90 graus, não foram completamente resolvidos) e a questão do openCV utilizar BGR ao invés de RGB por padrão, que causou resultados interessantes na hora de baixar o arquivo.

## Vídeo

https://drive.google.com/file/d/1zFtzdINKVZx99ntuO4X3jJC38E_r_qOY/view?usp=sharing

## Como rodar

```bash
git clone {repo}
cd {repo}
pip install -r requirements.txt
streamlit run main.py
```