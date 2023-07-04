from components.U2Net import u2net_load, u2net_run
from PIL import Image
import os
import numpy as np

from .human_parse import simple_extractor
from .ACGPN.predict_pose import generate_pose_keypoints
from .ACGPN.test import main

u2net = u2net_load.model(model_name='u2netp')


def infer(img1, img2):
    cloth_name = 'cloth.jpg'
    cloth = Image.open(img2)
    cloth = cloth.resize((192, 256), Image.BICUBIC).convert('RGB')
    cloth.save(os.path.join('./Data_preprocessing/test_color', cloth_name))
    u2net_run.infer(u2net, './Data_preprocessing/test_color', './Data_preprocessing/test_edge')
    Image.open(f'./Data_preprocessing/test_edge/{cloth_name}')

    img_name = 'model.jpg'
    img = Image.open(img1)
    img = img.resize((192,256), Image.BICUBIC).convert('RGB')
    img_path = os.path.join('./Data_preprocessing/test_img', img_name)
    img.save(img_path)
    model_path = './checkpoints/human_parse/lip_final.pth'

    simple_extractor.main(dataset='lip', model_restore=model_path, input_dir='./Data_preprocessing/test_img', output_dir='./Data_preprocessing/test_label')

    pose_path = os.path.join('./Data_preprocessing/test_pose', img_name.replace('.jpg', '_keypoints.json'))
    generate_pose_keypoints(img_path, pose_path)

    if os.path.isfile('./Data_preprocessing/test_pairs.txt'):
        os.remove('./Data_preprocessing/test_pairs.txt')
    with open('./Data_preprocessing/test_pairs.txt', 'w') as f:
        f.write(f'{img_name} {cloth_name}')
    
    main()

    img_name = img_name.replace('jpg', 'png')
    img = Image.fromarray(np.array(Image.open(f'./results/test/try-on/{img_name}')))
    return img