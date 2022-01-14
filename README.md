# auto-annotation-web

## Please note that this repo will be frequently updated for bug fixing or system reworks 


https://user-images.githubusercontent.com/46059385/149577523-2c5e7cbd-d0cc-491b-bed0-250a0d9ee6f9.mp4


This is a developing repository for an web-based annotation platform, which should be finally integrated with https://github.com/alexliyihao/AAPI_code, this project is funded by Columbia Biomedical Informatics Department and supervised by Dr.Sumit Mohan, if you have interest or want to copy the complete version, please email Dr. Mohan at sm2206@cumc.columbia.edu and CC me at yl4326@columbia.edu 

Develop environment:

- Ubuntu 16.04.7 LTS (From Google cloud platform VM)

Current Testing browser(subject to updating, as of now Dec.11, 2021):

- Google Chrome 96.0.4664.55
- Microsoft Edge 96.0.1054.53 will be tested but not as primary concern
- Safari 15.1 (17612.2.9.1.20) will be tested but not as primary concern

Beside dependency described in requirement.txt, other dependency including:
 
- 2 python versions needed:
    - python 3.5(for openslide 1.1.2, which can't be run on higher version)
    - Python 3.6+ (for django 3.2.8, 3.9.2 used in the development)

- OpenSeadragon 2.4.2 https://openseadragon.github.io/ (included in the repo)

- Annotorious OpenSeadragon plugin 2.5.8 https://github.com/recogito/annotorious-openseadragon (included in the repo)

- Annotorious Toolbar https://github.com/recogito/recogito-client-plugins (included in the repo)

- Annotorious Better Polygon https://github.com/recogito/recogito-client-plugins/tree/main/plugins/annotorious-better-polygon (included in the repo)

- Annotorious Selector Pack https://github.com/recogito/annotorious-selector-pack (included in the repo)
