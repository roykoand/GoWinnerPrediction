"""
Create dataset directory.
This file covered with tests in tests/make_dataset_test.py
"""
from typing import Union, List
import os
import re


class SGF2DS:
    """
    Class for transformation directory with sgf-files
    to a directory with images from endgame position.
    It generates directory:
        path-to-save
        ├── B
        ├── Draw [Optional]
        └── W
    """
    def __init__(
        self,
        path_to_convertor: str,
        path_to_dirs: Union[List[str], str],
        path_to_save: str,
    ) -> None:
        """
        Inits SGF2DS with the path to convertor sgf to png utility,
        path to the directory which contains sgf-files, 
        and path where images must be saved
        """
        self._path_to_convertor = path_to_convertor
        self._path_to_dirs = path_to_dirs if isinstance(path_to_dirs, list) else [path_to_dirs]
        self._path_to_save = path_to_save
            

    def save(self, pass_draw: bool=True) -> None:
        """
        If directory from path_to_save does not exist
        create it, and in this directory generate 3 folders
        path_to_save/{W, B, Draw} for images. Then parse dir/ with
        files in sgf-format and with utility convert sgf to png file 

        Args:
            pass draw [Optional]
                ignore games which ended with draw
        """
        if not os.path.isdir(self._path_to_save):
            os.mkdir(self._path_to_save)
            for dir_name in ["W", "B", "Draw"]:
                os.mkdir(os.path.join(self._path_to_save, dir_name))

        for dir_path in self._path_to_dirs:
            
            print(f"Collecting SGF-files from {dir_path}")

            for file in os.listdir(dir_path):
                if file.endswith(".sgf"):
                    # latin-1 encoding because SGF-file contain Chinese characters, UTF-8 crashed
                    with open(
                        os.path.join(dir_path, file), "r+", encoding="latin-1"
                    ) as sgf_file:

                        sgf_text = sgf_file.read()

                        winner_color = SGF2DS._find_winner(sgf_text)

                        # sometimes we have broken sgf-files
                        if winner_color == -1 or (winner_color == "Draw" and pass_draw):
                            continue
                        
                    file_name = file[:-4]
                    # ignore error messages from sgf2png utility
                    os.system(
                        f"{self._path_to_convertor} {dir_path}/{file} -n last -o {self._path_to_save}/{winner_color}/{file_name}.png 2>/dev/null"
                    )

    @staticmethod
    def _find_winner(sgf_text: str) -> str:
        """
        Find winner from the SGF file 
        SGF present it in the RE[COLOR+REASON] or RE[draw] format

        Args:
            sgf_text: 
                Text of file in SGF-format
                
        Returns:
            label of winner: B, W, draw
        """
        # dummy regex
        winner = re.findall(r"RE\[(W|B|draw)", sgf_text)

        if not len(winner) or len(winner) > 1:
            return -1 

        return winner[0].title()
    