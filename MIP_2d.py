import SimpleITK as sitk
import numpy as np
from PIL import Image
import os
import tqdm


def get_listdir(path):
    tmp_list = []
    for file in os.listdir(path):
        if os.path.splitext(file)[1] == '.gz':
            file_path = os.path.join(path, file)
            tmp_list.append(file_path)
    return tmp_list


def calculate_map(img_path, save_path):
    _, fullflname = os.path.split(img_path)
    img_sitk_img = sitk.ReadImage(img_path)
    img_arr = sitk.GetArrayFromImage(img_sitk_img)
    MIN_BOUND = -1000.0
    MAX_BOUND = 400.0
    img_arr[img_arr > MAX_BOUND] = MAX_BOUND
    img_arr[img_arr < MIN_BOUND] = MIN_BOUND
    img_arr = (img_arr - MIN_BOUND) / (MAX_BOUND - MIN_BOUND) * 255
    shape = img_arr.shape[0]
    # three slices of axial plane
    new_img_arr_1 = img_arr[:int(shape / 3), :, :]
    new_img_arr_2 = img_arr[int(shape / 3):int(shape * 2 / 3), :, :]
    new_img_arr_3 = img_arr[int(shape * 2 / 3):int(shape), :, :]
    # get MIP
    max_pro_1 = np.max(new_img_arr_1, axis=0)
    max_pro_2 = np.max(new_img_arr_2, axis=0)
    max_pro_3 = np.max(new_img_arr_3, axis=0)
    #
    max_pro_1 = max_pro_1.astype('uint8')
    max_pro_2 = max_pro_2.astype('uint8')
    max_pro_3 = max_pro_3.astype('uint8')
    # save MIP as npy files
    # np.save(os.path.join(save_path, fullflname + '_1.npy'), max_pro_1)
    # np.save(os.path.join(save_path, fullflname + '_2.npy'), max_pro_2)
    # np.save(os.path.join(save_path, fullflname + '_3.npy'), max_pro_3)
    # transform Image from numpy array
    max_pro_img_1 = Image.fromarray(max_pro_1)
    max_pro_img_2 = Image.fromarray(max_pro_2)
    max_pro_img_3 = Image.fromarray(max_pro_3)
    # save png files

    max_pro_img_1.save(os.path.join(save_path, fullflname + '_1.png'))
    max_pro_img_2.save(os.path.join(save_path, fullflname + '_2.png'))
    max_pro_img_3.save(os.path.join(save_path, fullflname + '_3.png'))

    # one MIP of axial plane or coronal plane, you should select the axis=0 or 1
    # max_pro = np.max(img_arr, axis=2)
    # np.save(os.path.join(save_path, fullflname + '.npy'), max_pro)
    # one MIP of sagittal plane, the middle slice is selected as the watershed, the two MIPs are jointed as one image.
    # The axis=2
    # new_img_arr_1 = img_arr[:, :, :int(shape / 2)]
    # new_img_arr_2 = img_arr[:, :,int(shape / 2):int(shape)]
    #
    # max_pro_1 = np.max(new_img_arr_1, axis=2)
    # max_pro_2 = np.max(new_img_arr_2, axis=2)
    #
    # new_img = np.hstack((max_pro_1, max_pro_2))
    #
    # np.save(os.path.join(save_path, fullflname + '.npy'), max_pro_1)


if __name__ == '__main__':
    img_path_source = r'K:\paper\8-vessel_map\image\HC\dalian\img'
    save_map_path = r'K:\paper\8-vessel_map\2d_mip_png\HC\dalian'
    img_list = get_listdir(img_path_source)
    img_list.sort()
    for i in tqdm.trange(len(img_list)):
        calculate_map(img_list[i], save_map_path)
