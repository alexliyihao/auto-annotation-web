# auto-annotation-web

This is a developing repository for an web-based annotation platform, which should be finally integrated with https://github.com/alexliyihao/AAPI_code

Develop environment:

- Ubuntu 16.04.7 LTS (From Google cloud platform VM)

Beside django version dependency described in requirement.txt, other dependency including:
 
- 2 python versions needed:
    - python 3.5(for openslide 1.1.2, which can't be run on higher version)
    - Python 3.6+ (for django 3.2.8, 3.9.2 used in the development)

- OpenSeadragon 2.4.2 https://openseadragon.github.io/ (included in the repo)

- Annotorious OpenSeadragon plugin 2.5.8 https://github.com/recogito/annotorious-openseadragon (included in the repo)

- Annotorious Toolbar https://github.com/recogito/recogito-client-plugins (included in the repo)

- Annotorious Better Polygon https://github.com/recogito/recogito-client-plugins/tree/main/plugins/annotorious-better-polygon (included in the repo)

- Annotorious Selector Pack https://github.com/recogito/annotorious-selector-pack (included in the repo)
