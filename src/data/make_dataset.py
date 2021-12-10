"""
Create balanced/imbalanced dataset directory.
This file covered with tests in tests/make_dataset_test.py
"""
from typing import Union, List, Optional
from PIL import Image
import os
import re
import random
import hashlib

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
        path_to_board_styles_dir: Optional[Union[str, None]] = None,
        balanced_dataset: Optional[Union[int, None]] = None
    ) -> None:
        """
        Inits SGF2DS with the path to convertor sgf to png utility,
        path to the directory which contains sgf-files, 
        and path where images must be saved and also you 
        can specify path to directory with styles in .toml format

        Args:
            path_to_converter:
                path to utility which convert sgf to png
            path_to_dirs:
                dirs which contain sgf files
            path_to_save:
                directory where to save files
            path_to_board_styles_dir [Optional]:
                directory which contain different styles of Go boards
            balanced_dataset [Optional]:
                number of images per one class
        """
        self._path_to_convertor = path_to_convertor
        self._path_to_dirs = path_to_dirs if isinstance(path_to_dirs, list) else [path_to_dirs]
        self._path_to_save = path_to_save
        self.balanced_dataset = balanced_dataset
        self.path_to_board_styles_dir = path_to_board_styles_dir

        if self.path_to_board_styles_dir is not None:
            self.paths_to_board_styles = os.listdir(self.path_to_board_styles_dir)


    def save(self, pass_draw: bool=True) -> None:
        """
        If directory from path_to_save does not exist
        create it, and in this directory generate 3 folders
        path_to_save/{W, B, Draw} for images. Then parse dir/ with
        files in sgf-format and with utility convert sgf to png file 
        with some custom styles (if prescribed)

        Args:
            pass draw [Optional]
                ignore games which ended with draw
        """
        if not os.path.isdir(self._path_to_save):
            os.mkdir(self._path_to_save)
            dataset_dirs = ["W", "B"]

            if not pass_draw:
                dataset_dirs.append("Draw")

            for dir_name in dataset_dirs:
                os.mkdir(os.path.join(self._path_to_save, dir_name))

        number_of_w = 0 
        number_of_b = 0 
        break_flag = False

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

                    if (number_of_w == number_of_b == self.balanced_dataset) and self.balanced_dataset:
                        break_flag = True
                        break

                    if winner_color == "B" and (number_of_b == self.balanced_dataset) and self.balanced_dataset:
                        continue

                    elif winner_color == "W" and (number_of_w == self.balanced_dataset) and self.balanced_dataset:
                        continue                     

                    file_name = file[:-4]
                    
                    # ignore error messages from sgf2png utility
                    terminal_script = f"{self._path_to_convertor} {dir_path}/{file} -n last -o {self._path_to_save}/{winner_color}/{file_name}.png"
                    
                    # if we want not only default board style
                    if self.path_to_board_styles_dir is not None:       
                        style_path = os.path.join(self.path_to_board_styles_dir, 
                                        random.choice(self.paths_to_board_styles))
                        terminal_script += f" --custom-style {style_path}"

                    os.system(terminal_script + " 2> /dev/null")

                    img_filename = os.path.join(self._path_to_save, winner_color, file_name + ".png")

                    if os.path.isfile(img_filename):
                        hashcode = SGF2DS._hash_image(img_filename)
                        os.rename(img_filename, os.path.join(self._path_to_save, winner_color, hashcode + ".png"))

                        if winner_color == "B":
                            number_of_b += 1
                        else:
                            number_of_w += 1
            
            if break_flag:
                print(f"Dataset from {2 * self.balanced_dataset} images is collected")
                break

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

    @staticmethod
    def _hash_image(image_path: str) -> None:
        """
        Bytes of the image to hashcode hex
        """
        img = Image.open(image_path)
        return hashlib.md5(img.tobytes()).hexdigest()
