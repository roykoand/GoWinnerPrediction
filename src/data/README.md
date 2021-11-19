# Files info

## ```make_dataset.py```
This file contains class ```SGF2DS``` which transforms the directory with [SGF-format](https://www.red-bean.com/sgf/) files to the directory with images in PNG-format.

Dataset folder will have the following tree structure:
```
    path-to-save
    ├── B
    ├── Draw [Optional]
    └── W
```

This file also covered with tests (```tests/make_dataset.py```)

## Acknowledgment
In this module, I used perfect CLI utility ```sgf-render``` (https://github.com/julianandrews/sgf-render) written in Rust. 

