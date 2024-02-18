import argparse
import os

import PyPDF2
from gtts import gTTS
from langdetect import detect as detect_language
from rich import print


def bold(text: str) -> str:
    return f"[bold]{text}[/bold]"


# TODO: add a progress status bar
def convert_pdf_to_mp3(
    input_path: str,
    output_path: str,
    language: str = "en",
):
    language_detected = False
    try:
        with open(input_path, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            pdf_text = ""

            print(bold("Converting PDF to text..."))
            for page in range(len(pdf_reader.pages)):
                text = pdf_reader.pages[page].extract_text()
                if not language_detected:
                    language = detect_language(text)
                    language_detected = True
                pdf_text += text

        tts = gTTS(text=pdf_text, lang=language, lang_check=True, slow=False)
        print(bold("Saving text to MP3..."))
        tts.save(output_path)
        print(f"Audio file saved as {bold(output_path)}")
    except FileNotFoundError:
        print(bold(f"Error: Input file '{input_path}' not found."))
    except Exception as e:
        print(bold(f"[red]An error occurred: {e}[/red]"))


def main():
    parser = argparse.ArgumentParser(
        description="Convert a PDF file to an MP3 audio file."
    )
    parser.add_argument("input_path", type=str, help="Input PDF file path")
    parser.add_argument("-o", "--output_path", type=str, help="Output MP3 file path")
    args = parser.parse_args()

    input_path = args.input_path
    output_path = args.output_path

    if not os.path.isfile(args.input_path):
        print(bold(f"Input file {args.input_path} does not exist."))
        exit(1)
    if not output_path:
        filename = os.path.basename(input_path).split(".")[0]
        output_path = f"{filename}.mp3"

    convert_pdf_to_mp3(input_path, output_path)


if __name__ == "__main__":
    main()
