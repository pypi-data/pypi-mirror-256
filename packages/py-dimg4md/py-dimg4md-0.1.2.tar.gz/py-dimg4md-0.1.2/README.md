<center>
    <img width="300px" src="image/cover.png">
</center>

# DIMG4MD

Many companies offer services that allow easy creation of Markdown on the web. However, when pasting images into their services, the images are not stored locally. Instead, they are stored in the cloud. If you need to automatically download the image and update the link in the Markdown, you can use this tool.

## Installation

You can install the package via pip:
```bash
pip install dimg4md
```

Or you can install the package from source:

```bash
git clone https://github.com/hsiangjenli/pyimg4md.git
cd pyimg4md
pip install .
```

## Usage

```javascript
Usage: dimg download [OPTIONS]

  Download images from Markdown file.

Options:
  --file TEXT        The markdown file to download images from.
  --output TEXT      The output directory to save the images.
  --rewrite BOOLEAN  Rewrite the markdown file with the new image urls.
  --force BOOLEAN    Force to download all the images from the Markdown file.
  --help             Show this message and exit.
```
