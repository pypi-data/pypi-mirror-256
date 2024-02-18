import click
import glob
import os
import pathlib
import img4md.img4 as img4

@click.group()
def cli():
    pass

@cli.command(name='download', help='Download images from Markdown file.')
@click.option('--file', default='myPythonProject', help='The markdown file to download images from.')
@click.option('--output', help='The output directory to save the images.')
@click.option('--rewrite', default=False, type=bool, help='Rewrite the markdown file with the new image urls.')
@click.option('--force', default=False, type=bool, help='Force to download all the images from the Markdown file.')
def download(file, output, rewrite, force):

    os.makedirs(output, exist_ok=True)

    exist_files_in_output = glob.glob(f"{output}/*")
    exist_files_in_output = [pathlib.Path(file).name for file in exist_files_in_output]

    with open(f"{file}", 'r') as f: md_file = f.read()
    img_paths = img4.find_img_path(md_file) # find img paths from the markdown file

    # check if the img path is a url
    img_paths = [img_path for img_path in img_paths if not img4.img_path_is_url(img_path)]
    
    for img_path in img_paths:
        if not force and img_path.split('/')[-1] in exist_files_in_output:
            print(f"🔥 Skipping {img_path} because it already exists in {output}")
        else:
            img4.download_img(img_path, output)
        
        md_file = md_file.replace(img_path, f"{output}/{img_path.split('/')[-1]}")
            

    if rewrite:
        print(f"📓 Rewriting {file} with the new image urls")
        with open(f"{file}", 'w') as f: f.write(md_file)
        
if __name__ == '__main__':
    cli()