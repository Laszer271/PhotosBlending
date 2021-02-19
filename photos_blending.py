import numpy as np
from PIL import Image

def gradient_from_point(image, point, max_val=1.0, min_val=0.0):
    width, height = image.size
    x_coord = point[0]
    y_coord = point[1]
    val_diff = max_val - min_val
    
    gradient = np.full((height, width), 0, float)
    width_grad = np.full((width), 0, float)
    height_grad = np.full((height), 0, float)
    temp_val = min_val
    step = val_diff / x_coord
    for i in range(x_coord):
        width_grad[i] = temp_val
        temp_val += step
    
    temp = width - x_coord - 1
    temp_val = max_val
    step = val_diff / temp
    for i in range(temp):
        width_grad[i+x_coord] = temp_val
        temp_val -= step
        
    temp_val = min_val
    step = val_diff / y_coord
    for i in range(y_coord):
        height_grad[i] = temp_val
        temp_val += step
    
    temp = height - y_coord - 1
    temp_val = max_val
    step = val_diff / temp
    for i in range(temp):
        height_grad[i + y_coord] = temp_val
        temp_val -= step
        
    for row in range(height):
        for col in range(width):
            new_val = (height_grad[row] + width_grad[col]) / 2.0
            gradient[row, col] = new_val
        
    return gradient
    

if __name__ == '__main__':
    base = Image.open('winny_the_pooh.jpg')
    base_size = base.size
    addition = Image.open('universe.jpg')
    addition = addition.resize(base_size)
    addition = np.array(addition)
    
    #addition = np.full((base_size[1], base_size[0], 3), 0, np.uint8)
    
    mask_array = np.full((base_size[1], base_size[0], 3), 0, float)
    min_val = -2.0
    mask1 = gradient_from_point(base, (364, 223), min_val=min_val) # left eye
    mask1 = mask1.clip(0, 1)
    mask2 = gradient_from_point(base, (446, 268), min_val=min_val) # right eye
    mask2 = mask2.clip(0, 1)
    mask = (mask1 + mask2) / 2.0
    for i in range(3):
        mask_array[:, :, i] = mask
    
    new_image = np.array(base) * mask_array
    new_image += addition * (-mask_array + 1)
    new_image = Image.fromarray(new_image.astype(np.uint8))
    new_image.show()
    
    base.close()
    new_image.close()
    
    '''
    addition = addition.resize(base_size)
    
    base_array = np.array(base)
    addition_array = np.array(addition)
    mask = base_array.mean(axis=2) < 190
    
    new_image = np.full((base_size[1], base_size[0], 3), 0, np.uint8)
    new_image[mask] += base_array[mask]
    new_image[~mask] += addition_array[~mask]
    
    new_image = Image.fromarray(new_image)
    new_image.show()
    '''