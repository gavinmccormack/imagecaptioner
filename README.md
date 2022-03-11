# "How can I caption and template a folder of images quickly in latex?"

Quick tool whipped up for someone's workflow

There is a runnable linux binary at

```
dist/captioner

```

If you're on Mac or Windows then alternatively you can run the python script by installing the prerequisites and running it with

```
python3 -m pip install pysimplegui
python3 captioner.py

```

Assuming python3 is installed. 

Might still run into issues on mac with assorted sub packages

# Build

Builds into a binary with pyinstaller

```
pyinstaller --onefile captioner.py

```

# Usage

Has a gui. Right hand pane is the template to use. It has three variables: caption, filepath, filename (without extension)

Left hand pane is the caption. 

![Editor](demo-image.jpg)

hit enter or click add to skip to the next image