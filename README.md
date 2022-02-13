# Go Game Winner Prediction

The meaning of this project follows from the name. The user sends us an endgame position image of the Go game, and we tell him who is the loser and winner.
## Presentation
You can get more information about the project and "production pipeline" from the ```demo/presentation/presentation.pdf```. 

## Flask app and API
You can check "production model" with the Flask app (```app/app.py```) or with the API (```api/api.py```). Weights of the production model are stored in the github release.
## Datasets

Endgame positions of the Go game (created with sgf2png utility [[1]](#1)):

https://www.kaggle.com/roykoandriy/endgame-positions-on-go-game

Go apps backgrounds:

https://www.kaggle.com/roykoandriy/go-apps-backgrounds

## References 
<a id="1">[1]</a>  Julian Andrews, SGF Render. Link:
https://github.com/julianandrews/sgf-render
