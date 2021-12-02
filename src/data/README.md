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
In this module, I used perfect CLI utility ```sgf-render``` (https://github.com/julianandrews/sgf-render) written in Rust. Also, for generating different styles of Go board, I used these [.toml configurations](https://github.com/julianandrews/sgf-render/tree/master/resources/styles) from the same author of utility. 

## ```parsers.py```

Parsers for scraping images from Google Images and Reddit subreddits.

For using this, you need to have config with credentials in ```.yaml``` format:
```
Reddit:
  client_id: client_id
  client_secret: client_secret
  user_agent: user_agent
  username: username
  password: password

Google: 
  dev_api_key: dev_api_key
  project_cx:  project_cx
```
