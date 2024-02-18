# coding: utf-8

from volumentations_biomedicine.core.composition import *
from volumentations_biomedicine.augmentations import *

#from .devel import *
import time
import os

size_sample = [(1,64,64,64) , (1,128,128,128) , (1,256,256,256), (1, 512, 512 , 64)     ]

#None are placeholders
augmentations_to_check = [
     AffineTransform(angle_limit = [(22.5,22.5), (22.5,22.5), (22.5,22.5)], p=1),
     AffineTransform(angle_limit = [(22.5,22.5), (22.5,22.5), (22.5,22.5)], translantion_limit= [10,10,10],scaling_coef=[1,0.5,2] , p=1),
     Flip(axes= [1,2,3], p = 1),
     GaussianBlur(sigma = 0 , p = 1),
     GaussianNoise(var_limit= (0.001, 0.1), mean= 0 ,p = 1),
     HistogramEqualization(bins= 256 , p = 1),
     Normalize(mean = 0, std = 1, p = 1),
     NormalizeMeanStd(mean= 0.1, std= 1, p = 1),
     RandomBrightnessContrast(brightness_limit= 0.2, contrast_limit= 0.2, p= 0.1),
     RandomFlip( axes_to_choose= None, p = 1),
     RandomGamma(gamma_limit = (0.8, 1.2), p = 1),
     RandomGaussianBlur(max_sigma= 0.8, p = 1),
     RandomRotate90(axes=  [1,2,3] ,p = 1),
     RandomScale( scale_limit= (0.75, 1.5), p = 1),
     Scale( scale_factor= 1.5, p = 1),
     Scale( scale_factor= 0.75, p = 1),
     None,
     None,
     None,
     None,
     None,
     None

]


def get_augmentations(number, shape):
     bigger_shape = (shape[1] * 1.5, shape[2] * 1.5, shape[3] * 1.5  )
     smaller_shape = (shape[1] * 0.75, shape[2] * 0.75, shape[3] * 0.75  )
     augmentations = [
          CenterCrop(shape= bigger_shape, p = 1),
          CenterCrop(shape= smaller_shape, p = 1),
          RandomCrop(shape = bigger_shape, p = 1),
          RandomCrop(shape = smaller_shape, p = 1),
          Resize(bigger_shape, p = 1),
          Resize(smaller_shape, p = 1),
     ]
     return augmentations[number]




def single_transform(iterations, size, augumentation):
    cummulative = 0
    maximum = 0
    for i in range(iterations):
        test = np.random.uniform( low = 0, high= 1, size=size)
        aug = Compose( transforms=[augumentation], p = 1)
        data = {'image': test  } 
        second_time = time.time()
        aug_data = aug(**data)
        #img = aug_data['image']
        tmp =  time.time() - second_time
        cummulative += tmp
        if tmp > maximum :
             maximum = tmp
    return maximum, cummulative 


def augumentation_getter(augmentations_to_check, iteration, size):
     counter = 0
     for k in augmentations_to_check:
        if k is None:
            counter += 1 
     if augmentations_to_check[iteration] is not None:
        return augmentations_to_check[iteration]
     else:
        pixel_aug_index = (iteration - len(augmentations_to_check)) + counter  # Six is random contant
        return get_augmentations(pixel_aug_index, size)

def transformation_speed_benchmark(iterations):
    f = open("./100iterationCorrections.txt", "w")


    for i in range(len(augmentations_to_check)):  # random_scale_transform
         for size in size_sample:
            augumentation = augumentation_getter(augmentations_to_check, i, size)
            aug_name = augumentation.__class__.__name__
            test_sample = np.random.uniform( low = 0, high= 1, size=size)
            test = test_sample.copy()

            aug = Compose( transforms=[augumentation], p = 1)
            data = {'image': test  }
            first_time = time.time()
            aug_data = aug(**data)
            first_result = time.time() - first_time
            maximum, cummulative = single_transform(iterations, size, augumentation)
            result_time = cummulative / iterations
            f.write(f"Transform: {aug_name},  Size: {size}, FirstRun: {first_result:.3f}, Average: {result_time:.3f}, " + 
                  f"Iterations: {iterations}, maximum: {maximum:.3f} \n")

    f.close()





if __name__ == '__main__':
    transformation_speed_benchmark(100)
