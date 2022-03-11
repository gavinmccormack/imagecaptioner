# image_viewer.py
import io
import os, os.path
import PySimpleGUI as sg
from PIL import Image

file_types = [("JPEG (*.jpg)", "*.jpg", "*.png"),
              ("All files (*.*)", "*.*")]

def main():
    # Get list of images
    imgs = []
    path = os.getcwd() # NB: Probably needs amending to be target dir.
    target_path = os.path.join(path, "put-images-here")

    latex_template = """
\\begin{figure}
\\caption{%(caption)s}
\\begin{center}
\\includegraphics{%(filepath)s}
\\label{fig:%(filename)s}
\\end{center}
\\end{figure}
            """

    sg.theme('DarkTeal9')
    if not os.path.exists(target_path):
        os.mkdir(target_path)
    valid_images = [".jpg",".gif",".png",".tga"]
    for f in os.listdir(target_path):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_images:
            continue
        imgs.append(os.path.join(target_path,f))

    number_of_images = len(imgs)
    count = 0
    if number_of_images == 0:
        print("You din't put any images in")
        exit()

    image_section = sg.Image(key="-IMAGE-")
    layout = [
        [sg.Text("%s of %s" % (count,number_of_images), font="Helvetica", key="Image-Count")],
        [sg.Column([[image_section]], justification='center')],
        [sg.Text("Input a caption"), 
         sg.Multiline(size=(60, 10),  key='-MLINE-',font="Helvetica",enter_submits=True,do_not_clear=False, pad=(20, (15, 20)) ),
         sg.Multiline(size=(60, 10),  key='-MLINE2-', font="Helvetica", enter_submits=True,do_not_clear=True, pad=(20, (15, 20)) ),
         sg.Button("Add",pad=(0, (15, 0)))],
    ]
    window = sg.Window("Captions! CAPTIONS! CAPTIONSSSSS!", layout, margins=(20,20), finalize=True)
    window['-MLINE-'].bind("<Return>", "_Enter")
    window['-MLINE2-'].update(latex_template)

    while True:
        filename = imgs.pop() # This crashes the program when finished. But like, a cool crash.
        if os.path.exists(filename):
            image = Image.open(filename)
            image.thumbnail((700, 700)) # If image is too big other sections may not display
            bio = io.BytesIO()
            image.save(bio, format="PNG")
            window["-IMAGE-"].update(data=bio.getvalue())

            # Update counter text
            count += 1
            window['Image-Count'].update("%s of %s" % (count, number_of_images))

        event, values = window.read()

        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event == "-MLINE-_Enter" or event == "Add":
            caption = values['-MLINE-']

            filename_without_ext = os.path.basename(filename).split('.')[0]
            latex_template = values['-MLINE2-'] % { 'caption': caption, 'filepath': filename, 'filename' :filename_without_ext}
            try:
                with open("outputs.tex", "a") as file:
                    print("Adding to file: \n", latex_template)
                    file.write(latex_template)
            except:
                print("Something went wrong with the file. Check permissions, or create a 'outputs.tex' file in this directory")

    window.close()
if __name__ == "__main__":
    main()