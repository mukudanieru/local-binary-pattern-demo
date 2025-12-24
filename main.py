from helpers.image import (
    read_image,
    rgb_to_grayscale,
    save_grayscale_image,
    extract_3msb_image,
    save_texture_map,
)
from helpers.texture import compute_lbp_texture_map


def output_gray_image(gray_list):
    gray_file = "img/lenna_gray.png"

    gray = rgb_to_grayscale(gray_list)
    save_grayscale_image(gray, gray_file)


def lenna():
    file = "img/lenna.png"
    rgb = read_image(file)

    gray_file = "img/lenna_gray.png"
    gray = rgb_to_grayscale(rgb)

    save_grayscale_image(gray, gray_file)

    three_msb = extract_3msb_image(gray)
    texture = compute_lbp_texture_map(three_msb)

    texture_file = "img/lenna_texture.png"
    save_texture_map(texture, texture_file)


def main():
    file = "img/joker.png"
    rgb = read_image(file)
    print(rgb[0][0])

    gray_file = "img/joker_gray.png"
    gray = rgb_to_grayscale(rgb)
    print(gray[0][0])

    save_grayscale_image(gray, gray_file)

    three_msb = extract_3msb_image(gray)
    texture = compute_lbp_texture_map(three_msb)
    print(texture[0][0])

    texture_file = "img/joker_texture.png"
    save_texture_map(texture, texture_file)


if __name__ == "__main__":
    main()
