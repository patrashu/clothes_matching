#  딥러닝 및 실습 프로젝트 - 딥러닝 기반 의상 교체 시스템
![image (1)](https://github.com/patrashu/clothes_matching/assets/49676680/0d568c22-727d-4068-8014-40ad1825ffa1)

- 삼육대학교 교과목 딥러닝 및 실습 최종 프로젝트
- 개발 기간 : 2023/05/09 ~ 2023/06/20

## 프로젝트 소개

- 컴퓨터 비전과 딥러닝 기술을 활용하여 사용자의 의상을 GUI를 통해 실시간으로 변경
- 의상 선택과 스타일링을 제공하여 자신이 입고자 하는 옷을 가상으로 피팅
- 옷을 온라인으로 구매하고자 하는 사람들에게 편리한 서비스를 제공하고자 함

## 데이터셋 소개
[Dataset Link](https://github.com/xthan/VITON)


##  Requirements

[Checkpoints Link](https://drive.google.com/file/d/1SXmB8MJZ-8WERAe_Ipwe-0VXopo-463g/view?usp=sharing)

[segmentation_checkpoint](https://drive.google.com/file/d/1zz1n-4UjJFyN7doQZUjY9gOpQhBzhT_v/view?usp=drive_link)

Download and Unzip ./checkpoints/

```
conda create -n fashion python=3.8 -y
conda activate fashion
conda install pytorch==1.12.0 torchvision==0.13.0 cudatoolkit=11.3 -c pytorch
pip install -r requirements.txt
```

## 주요 기능
![image](https://github.com/patrashu/clothes_matching/assets/49676680/c9fbee5c-9ed2-485c-a4da-fe3da3ce3816)
- using local file with click btn
- using crawing image with selenium
- Pose Detection
- Semantic Segmentation
- Human Parsing
- mapping two images using ACGPN
- Image Super Resolution

## 기술 스택
- Python
- PyTorch
- PyTorch-Lightning
- PySide6
- OpenCV
- Selenium
- Ninja
- Wandb

