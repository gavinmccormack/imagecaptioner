#!/usr/bin/env python3
"""
Desktop utility for speeding through image captioning and template generation.

Aim is for user friendly.
"""
import io
import os
import os.path
import PySimpleGUI as sg
from PIL import Image


VALID_IMAGES = [".jpg", ".gif", ".png", ".tga"]

LATEX_TEMPLATE = """
\\begin{figure}
\\caption{%(caption)s}
\\begin{center}
\\includegraphics{%(filepath)s}
\\label{fig:%(filename)s}
\\end{center}
\\end{figure}
"""


PATH = os.getcwd() 
TARGET_PATH = os.path.join(PATH, "put-images-here")


sg.theme("DarkTeal9")


def get_list_of_image_paths() -> list:
    """Gets.... a list of image paths! in the TARGET_PATH directory"""
    if not os.path.exists(TARGET_PATH):
        os.mkdir(TARGET_PATH)
    imgs = []
    for file in os.listdir(TARGET_PATH):
        ext = os.path.splitext(file)[1]
        if ext.lower() not in VALID_IMAGES:
            continue
        imgs.append(os.path.join(TARGET_PATH, file))

    if len(imgs) == 0:
        print("You didn't put any images in")
        exit()
    return imgs


def main():
    """Get list of images"""
    imgs = get_list_of_image_paths()
    number_of_images = len(imgs)
    index = 0  # Index of current image

    layout = [
        [
            sg.Text(
                f"{index} of {number_of_images}",
                font="Helvetica",
                key="Image-index",
                justification="left",
            )
        ],
        [sg.Column([[sg.Image(key="-IMAGE-")]], justification="center")],
        [
            sg.Text("Input a caption"),
            sg.Multiline(
                size=(60, 10),
                key="-MLINE-",
                font="Helvetica",
                enter_submits=True,
                do_not_clear=False,
                pad=(20, (15, 20)),
            ),
            sg.Multiline(
                size=(60, 10),
                key="-MLINE2-",
                font="Helvetica",
                enter_submits=True,
                do_not_clear=True,
                pad=(20, (15, 20)),
            ),
            sg.Button("Add", font="Helvetica", pad=(0, (15, 0))),
        ],
    ]
    window = sg.Window(
        "Captions! CAPTIONS! CAPTIONSSSSS!", layout, margins=(20, 20), finalize=True
    )
    window["-MLINE-"].bind("<Return>", "_Enter")
    window["-MLINE2-"].update(LATEX_TEMPLATE)

    while True:
        try:
            filename = imgs.pop()
        except:
            print("Done.")
            break

        if os.path.exists(filename):
            image = Image.open(filename)
            image.thumbnail(
                (700, 700)
            )  # If image is too big other sections may not display
            bio = io.BytesIO()
            image.save(bio, format="PNG")
            window["-IMAGE-"].update(data=bio.getvalue())

            # Update indexer text
            index += 1
            window["Image-index"].update("{index} of {number_of_images}")

        event, values = window.read()

        if event in ["Exit", sg.WIN_CLOSED]:
            break

        if event in ["Add", "-MLINE-_Enter"]:
            caption = values["-MLINE-"]

            filename_without_ext = os.path.basename(filename).split(".")[0]
            output_latex = values["-MLINE2-"] % {
                "caption": caption,
                "filepath": filename,
                "filename": filename_without_ext,
            }

            try:
                with open("outputs.tex", "a", encoding="UTF-8") as file:
                    print("Added to output file")
                    file.write(output_latex)
            except:
                print("Something went wrong with the file access")
                print(
                    "Check permissions, or create the 'outputs.tex' file in this directory"
                )

    window.close()


if __name__ == "__main__":
    main()
