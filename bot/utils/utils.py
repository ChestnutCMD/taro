import random
from PIL import Image


def choice_cart():
    carts = [cart for cart in range(1, 79)]
    return random.choice(carts)


def choice_tree_carts():
    carts = [cart for cart in range(1, 79)]
    random.shuffle(carts)
    choices_carts = [carts[0], carts[1], carts[2]]
    return choices_carts


def image_join(image1: str, image2: str, image3: str, name: str):
    img1 = Image.open(image1)
    img2 = Image.open(image2)
    img3 = Image.open(image3)

    new_img = Image.new("RGB", (660, 400), "black")

    new_img.paste(img1, (0, 0))
    new_img.paste(img2, (220, 0))
    new_img.paste(img3, (440, 0))
    new_img.save(f'Images/Prediction/{name}.jpg', 'JPEG')
    return f'Images/Prediction/{name}.jpg'

# converted_img = img.transpose(Images.FLIP_TOP_BOTTOM)  # перевернуть изображение # rotated_img = img.rotate(180)
