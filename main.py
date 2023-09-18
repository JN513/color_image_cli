#!/home/julio/Documents/maker/imager-binary/env/bin/python

import os
import sys
import cv2
import argparse
import clipboard
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

current_directory = os.getcwd()


parser = argparse.ArgumentParser(
    prog="color_image.py",
    description="Transforme imagens coloridas em escala de cinza e preto e branco",
    epilog="Text at the bottom of help",
)


parser.add_argument("filename", type=str, help="nome da imagem")
parser.add_argument(
    "-f",
    "--full_path",
    action="store_true",
    default=False,
    help="O nome da imagem passado e o path completo ou não",
)
parser.add_argument(
    "-c",
    "--clipboard_selection",
    type=int,
    default=0,
    help="Qual imagem você deseja copiar para o area de copia: 1 - gray, 2 - binary, 3 - binary inv. Caso sejá utilizado 0 nenhuma imagem e copiada",
)
parser.add_argument(
    "-d",
    "--directory_output",
    type=str,
    default="",
    help="Diretorio em que você deseja salvar a imagem",
)
parser.add_argument(
    "-s",
    "--show",
    action="store_true",
    default=False,
    help="Deseja plotar os resultados ?",
)

args = parser.parse_args()

image_path = ""

if not args.full_path:
    image_path = current_directory + "/" + args.filename
else:
    image_path = args.filename

image_name = image_path.split("/")[-1]
image_name = "".join(image_name.split(".")[:-1])

img = cv2.imread(image_path)

if not img.any():
    print("Erro ao abrir imagem :(")

    sys.exit()

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# default second parameter is 70
ret, thresh = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)

# default second parameter is 70
ret, thresh1 = cv2.threshold(img_gray, 120, 255, cv2.THRESH_BINARY)

if args.show:
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    plt.subplot(141), plt.imshow(img_rgb), plt.title(
        "Original Image"), plt.axis("off")

    plt.subplot(142), plt.imshow(img_gray, cmap="gray"), plt.title(
        "Gray Image"
    ), plt.axis("off")

    plt.subplot(143), plt.imshow(thresh, cmap="gray"), plt.title(
        "Bin Inv Image"
    ), plt.axis("off")

    plt.subplot(144), plt.imshow(thresh1, cmap="gray"), plt.title(
        "Bin Image"
    ), plt.axis("off")

    plt.show()

directory_to_save = ""

if args.clipboard_selection == 1:
    im_pil = Image.fromarray(img_gray)
    # clipboard.set_image(im_pil, format='png', jpeg_quality=1)
elif args.clipboard_selection == 2:
    im_pil = Image.fromarray(thresh1)
    # clipboard.set_image(im_pil, format='png', jpeg_quality=1)
elif args.clipboard_selection == 3:
    im_pil = Image.fromarray(thresh)
    # clipboard.set_image(im_pil, format='png', jpeg_quality=1)


if args.directory_output:
    directory_to_save = f"{args.directory_output}/"

cv2.imwrite(f"{directory_to_save}{image_name}_gray.png", img_gray)
cv2.imwrite(f"{directory_to_save}{image_name}_binary_inv.png", thresh)
cv2.imwrite(f"{directory_to_save}{image_name}_binary.png", thresh1)
