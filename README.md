# 🐟😁 고려대학교 지능정보 4조 프로젝트😁🐟

# Multimodal Based OTT English Education Platform -- DailSH 



<a href="https://pytorch.org/"><img src="https://img.shields.io/badge/PyTorch-v2.00+-red.svg?logo=PyTorch&style=for-the-badge" /></a>
<a href="#"><img src="https://img.shields.io/badge/python-v3.9+-blue.svg?logo=python&style=for-the-badge" /></a>

# 전체 모델 구조

![image](https://github.com/2023inisw04/inisw04project/assets/35323806/bfce895c-4230-4146-bdf2-e748a6a452ab)

# 모델 실행 순서

## 1. Shot Detection
아래 링크에서 ilsd shot detector를 다운받아 주세요.
https://drive.google.com/drive/folders/1AAje4IdjccW6PXJwzewj6GEZYJhpGJKQ?usp=sharing
이후 분석하고 싶은 video를 shot detector의 debug폴더 안에 videos folder에 넣고 shot detection을 수행합니다.

## 2. 이후 나온 video와 shot_txt 파일을 가지고 Scene detection을 수행합니다.

앞서 나온 detected shot과 video를 바탕으로 Inception V3 모델을 수행하여 scene image feature를 가져오고, 이를 바탕으로 H5 file을 만듭니다.

![image](https://github.com/2023inisw04/inisw04project/assets/35323806/b94f580a-4088-47f3-8522-d40177323676)


Scene detection 이후 나온 후 해당 앞서 가져온 H5 file에서 Sceen boundary를 추가합니다. 그리고 비디오를 다음과 같은 디렉토리 형식으로 잘라서 다시 저장합니다.

<pre><code>
  BaseFolder
    |
    -- videoName
        |
        -- video_scene1.mp4
        -- video_scene2.mp4
    -- videoName2
        |
        -- video_scene1.mp4
        -- video_scene2.mp4
</code></pre>

## 3. MMV 모델

![image](https://github.com/2023inisw04/inisw04project/assets/35323806/a3201231-558d-4f51-94ce-51848bd5f1e2)


Scene detection으로 추출된 영상을 각 backbone을 통해 feature vector를 추출한 후 MMV 모델을 거쳐 랭크를 비교합니다.

## 4. 소비자에게 가장 랭크가 높은 비디오 장면 제공

- 시연 영상 1

  ![시연1](https://github.com/2023inisw04/inisw04project/assets/104895119/1e0e80ed-69c3-4027-a9b9-00b107bff57d)


- 시연 영상 2

  우리의 down stream task인 moment-detr 모델에 넣는다면 output은 video[id] 와 영상에서 연관이 있는 장면의 초 수가 나옵니     다. 따라서 moment-detr의 결과를 추후에 포함할 수 있도록 시간을 조정해서 영상을 보여주는 시연 영상입니다.

  ![시연2](https://github.com/2023inisw04/inisw04project/assets/104895119/941d44bc-30ec-4cad-9f45-6c4a709c8940)


  


