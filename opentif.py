from PIL import Image
import numpy as np

def read_tiff(path, n_images):
    """
    path - Path to the multipage-tiff file
    n_images - Number of pages in the tiff file
    """
    img = Image.open(path)
    images = []
    for i in range(n_images):
        try:
            img.seek(i)
            slice_ = np.zeros((img.height, img.width))
            for j in range(slice_.shape[0]):
                for k in range(slice_.shape[1]):
                    slice_[j,k] = img.getpixel((j, k))

            images.append(slice_)

        except EOFError:
            # Not enough frames in img
            break

    return np.array(images)

path = 'D:/PESQUISA/Outros/Maiara/2021_Sensibilidade_teste1/Sensibilidde Glicose 19-10/0_H20_15h10.tif'
n_images= 10

X = read_tiff(path, n_images)

np.save('0_H20_15h10',X)