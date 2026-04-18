import os
import argparse
from pathlib import Path
from PIL import Image
import img2pdf
from ebooklib import epub

def create_pdf(image_paths, output_pdf_path):
    print(f"Creating High-Res Print PDF: {output_pdf_path}...")
    with open(output_pdf_path, "wb") as f:
        f.write(img2pdf.convert([str(p) for p in image_paths]))
    print("[OK] Print PDF Created successfully.")

def create_web_pdf(image_paths, output_pdf_path, max_height=1600, quality=75):
    print(f"Creating Compressed Web PDF: {output_pdf_path}...")
    processed_images = []
    for path in image_paths:
        img = Image.open(path).convert("RGBA")
        canvas = Image.new("RGB", img.size, (255, 255, 255))
        canvas.paste(img, mask=img.split()[3])
        if canvas.height > max_height:
            ratio = max_height / float(canvas.height)
            new_width = int(float(canvas.width) * ratio)
            canvas = canvas.resize((new_width, max_height), Image.Resampling.LANCZOS)
        processed_images.append(canvas)
    
    processed_images[0].save(
        output_pdf_path,
        save_all=True,
        append_images=processed_images[1:],
        quality=quality,
        optimize=True
    )
    print("[OK] Web PDF Created successfully.")

def create_epub(image_paths, output_epub_path, title="Comic Book"):
    print(f"Creating EPUB: {output_epub_path}...")
    book = epub.EpubBook()
    book.set_identifier(f"comic_{Path(output_epub_path).stem}")
    book.set_title(title)
    book.set_language('en')
    chapters = []
    for i, img_path in enumerate(image_paths):
        with open(img_path, 'rb') as f:
            img_content = f.read()
        img_name = f"page_{i:03d}{Path(img_path).suffix}"
        epub_img = epub.EpubImage()
        epub_img.file_name = f"images/{img_name}"
        epub_img.content = img_content
        book.add_item(epub_img)
        c = epub.EpubHtml(title=f'Page {i}', file_name=f'page_{i:03d}.xhtml', lang='en')
        c.content = f'<html><body style="margin:0;padding:0;text-align:center;"><img src="images/{img_name}" style="max-width:100%;height:auto;" /></body></html>'
        book.add_item(c)
        chapters.append(c)
    book.toc = tuple(chapters)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ['nav'] + chapters
    epub.write_epub(output_epub_path, book, {})
    print("[OK] EPUB Created successfully.")

def process_single_album(input_path, args):
    if not input_path.exists():
        print(f"Error: Folder {input_path} not found.")
        return

    extensions = {'.jpg', '.jpeg', '.png', '.webp', '.tiff'}
    image_paths = sorted(
        [p for p in input_path.iterdir() if p.suffix.lower() in extensions],
        key=lambda x: x.name
    )

    if not image_paths:
        print(f"No images found in {input_path.name}. Skipping.")
        return

    print(f"\n--- Bundling Album: {input_path.name} ---")
    base_name = input_path.name.split('_')[0] 
    title = args.title if args.title != "Spooky & Sara" else base_name
    
    do_all = not (args.web or args.print or args.epub)

    if args.web or do_all:
        create_web_pdf(image_paths, input_path.parent / f"{base_name}_web.pdf")
    
    if args.epub or do_all:
        create_epub(image_paths, input_path.parent / f"{base_name}.epub", title=title)
    
    if args.print or do_all:
        create_pdf(image_paths, input_path.parent / f"{base_name}_print.pdf")

def main():
    parser = argparse.ArgumentParser(description="Convert a folder of images to PDF and EPUB.")
    parser.add_argument("input_folder", nargs="?", default=None)
    parser.add_argument("-t", "--title", type=str, default="Spooky & Sara")
    parser.add_argument("--web", action="store_true", help="Generate only the web-optimized PDF")
    parser.add_argument("--print", action="store_true", help="Generate the heavy high-res print PDF")
    parser.add_argument("--epub", action="store_true", help="Generate the EPUB file")
    
    args = parser.parse_args()
    albums_root = Path(r"D:\GIT\Web\Hantekeningen.be\albums")
    
    if args.input_folder:
        process_single_album(Path(args.input_folder), args)
    else:
        print(f"No input folder specified. Scanning {albums_root} for processed albums...")
        for folder in sorted(albums_root.iterdir()):
            if folder.is_dir() and folder.name.endswith("_processed"):
                process_single_album(folder, args)

    print("\n[Done] All bundling tasks complete!")

if __name__ == "__main__":
    main()
