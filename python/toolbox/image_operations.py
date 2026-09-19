#!/usr/bin/env python3

from pathlib import Path
from PIL import Image
import sys


# ============================================================
# Configuration
# ============================================================

SUPPORTED_IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp",
    ".tiff",
    ".tif",
}


# ============================================================
# Utility functions
# ============================================================

def get_image_files(folder: Path):
    """Return supported image files from a folder, sorted by name."""
    return sorted(
        [
            file
            for file in folder.iterdir()
            if file.is_file()
            and file.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS
        ],
        key=lambda x: x.name.lower(),
    )


def prepare_image_for_pdf(image: Image.Image):
    """
    Convert an image into RGB format suitable for PDF.
    Handles images with transparency.
    """

    if image.mode in ("RGBA", "LA"):
        background = Image.new("RGB", image.size, "white")

        if image.mode == "RGBA":
            background.paste(image, mask=image.getchannel("A"))
        else:
            background.paste(image, mask=image.getchannel("A"))

        return background

    if image.mode == "P":
        image = image.convert("RGBA")

        background = Image.new("RGB", image.size, "white")
        background.paste(image, mask=image.getchannel("A"))

        return background

    return image.convert("RGB")


def images_to_pdf(image_paths, output_path):
    """Convert a list of images into a single PDF."""

    if not image_paths:
        raise ValueError("No images were provided.")

    converted_images = []

    try:
        for image_path in image_paths:
            print(f"  Processing: {image_path.name}")

            with Image.open(image_path) as image:
                # Copy image before closing the file
                image_copy = image.copy()

            converted = prepare_image_for_pdf(image_copy)
            converted_images.append(converted)

        first_image = converted_images[0]
        remaining_images = converted_images[1:]

        first_image.save(
            output_path,
            "PDF",
            resolution=100.0,
            save_all=True,
            append_images=remaining_images,
        )

    finally:
        for image in converted_images:
            image.close()


# ============================================================
# Command: Images to PDF
# ============================================================

def images_to_pdf_command():
    print("\n" + "=" * 50)
    print(" IMAGES → PDF")
    print("=" * 50)

    raw_input = input(
        "\nEnter image paths separated by commas:\n> "
    ).strip()

    if not raw_input:
        print("No images provided.")
        return

    image_paths = []

    for item in raw_input.split(","):
        path = Path(item.strip()).expanduser()

        if not path.exists():
            print(f"File not found: {path}")
            return

        if not path.is_file():
            print(f"Not a file: {path}")
            return

        if path.suffix.lower() not in SUPPORTED_IMAGE_EXTENSIONS:
            print(f"Unsupported image format: {path}")
            return

        image_paths.append(path)

    print("\nImages selected:")
    for index, path in enumerate(image_paths, start=1):
        print(f"  {index}. {path}")

    output = input(
        "\nEnter output PDF path [output.pdf]:\n> "
    ).strip()

    if not output:
        output = "output.pdf"

    output_path = Path(output).expanduser()

    if output_path.suffix.lower() != ".pdf":
        output_path = output_path.with_suffix(".pdf")

    # Create parent folder if necessary
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        print("\nConverting...")

        images_to_pdf(image_paths, output_path)

        print("\n✓ PDF created successfully!")
        print(f"  {output_path.resolve()}")

    except Exception as error:
        print(f"\n✗ Failed to create PDF:")
        print(f"  {error}")


# ============================================================
# Command: Folder to PDF
# ============================================================

def folder_to_pdf_command():
    print("\n" + "=" * 50)
    print(" FOLDER → PDF")
    print("=" * 50)

    folder_input = input(
        "\nEnter folder path:\n> "
    ).strip()

    if not folder_input:
        print("No folder provided.")
        return

    folder = Path(folder_input).expanduser()

    if not folder.exists():
        print(f"Folder not found: {folder}")
        return

    if not folder.is_dir():
        print(f"Not a folder: {folder}")
        return

    image_paths = get_image_files(folder)

    if not image_paths:
        print("\nNo supported images found in this folder.")
        print(
            "Supported formats: "
            + ", ".join(sorted(SUPPORTED_IMAGE_EXTENSIONS))
        )
        return

    print(f"\nFound {len(image_paths)} image(s):\n")

    for index, image_path in enumerate(image_paths, start=1):
        print(f"  {index:>3}. {image_path.name}")

    default_name = f"{folder.name}.pdf"

    output = input(
        f"\nEnter output PDF path [{default_name}]:\n> "
    ).strip()

    if not output:
        output = default_name

    output_path = Path(output).expanduser()

    if output_path.suffix.lower() != ".pdf":
        output_path = output_path.with_suffix(".pdf")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        print("\nConverting...")

        images_to_pdf(image_paths, output_path)

        print("\n✓ PDF created successfully!")
        print(f"  {output_path.resolve()}")

    except Exception as error:
        print(f"\n✗ Failed to create PDF:")
        print(f"  {error}")


# ============================================================
# Future commands
# ============================================================

def pdf_to_images_command():
    """
    Placeholder for future implementation.
    """
    print("\nPDF → Images is not implemented yet.")


def compress_pdf_command():
    """
    Placeholder for future implementation.
    """
    print("\nCompress PDF is not implemented yet.")


# ============================================================
# Command registry
# ============================================================

COMMANDS = {
    "1": {
        "name": "Images to PDF",
        "function": images_to_pdf_command,
    },
    "2": {
        "name": "Folder to PDF",
        "function": folder_to_pdf_command,
    },

    # Easy to enable later:
    #
    # "3": {
    #     "name": "PDF to Images",
    #     "function": pdf_to_images_command,
    # },
    #
    # "4": {
    #     "name": "Compress PDF",
    #     "function": compress_pdf_command,
    # },
}


# ============================================================
# Menu
# ============================================================

def show_menu():
    print("\n")
    print("=" * 50)
    print("                 PDF TOOLKIT")
    print("=" * 50)

    for key, command in COMMANDS.items():
        print(f"  {key}. {command['name']}")

    print("  q. Quit")

    print("=" * 50)


# ============================================================
# Main application
# ============================================================

def main():
    print("\nWelcome to PDF Toolkit!")

    while True:
        show_menu()

        try:
            choice = input("\nSelect a command: ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\n\nGoodbye!")
            break

        if choice == "q":
            print("\nGoodbye!")
            break

        command = COMMANDS.get(choice)

        if command is None:
            print("\n✗ Invalid choice.")
            continue

        try:
            command["function"]()

        except KeyboardInterrupt:
            print("\n\nOperation cancelled.")

        except Exception as error:
            print(f"\n✗ Unexpected error:")
            print(f"  {error}")

        input("\nPress Enter to return to the main menu...")


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    main()