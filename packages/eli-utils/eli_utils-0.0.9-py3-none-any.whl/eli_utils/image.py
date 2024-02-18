from PIL import Image

def resize_image(image: Image.Image, desired_size: int):
    width, height = image.size
    aspect_ratio = width / height

    if width > height:
        new_width = desired_size
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = desired_size
        new_width = int(new_height * aspect_ratio)

    resized_image = image.resize((new_width, new_height))
    return resized_image

def change_dpi(image: Image.Image, output_path: str, dpi: int = 300):
    dpi = (dpi, dpi)
    image.info['dpi'] = dpi
    image.save(output_path, dpi=dpi)


def change_dpi_from_file(input_path, output_path: str, dpi: int = 300):
    image = Image.open(input_path)
    dpi = (dpi, dpi)
    image.info['dpi'] = dpi
    image.save(output_path, dpi=dpi)
