from sys import stdin
import argparse

if __name__ == "__main__":
    from txt2img import Txt2img, FONT_FACE_MESLO
else:
    from .txt2img import Txt2img, FONT_FACE_MESLO


def main():
    parser = argparse.ArgumentParser(
        description="Turns a text input into an image.",
        epilog='example: echo "Example echo" | command2img',
    )

    parser.add_argument(
        "--output",
        "-o",
        dest="output",
        action="store",
        default="output.png",
        nargs="?",
        help="Output file.",
        type=str,
    )

    parser.add_argument(
        "--font_face",
        "-ff",
        dest="fontFace",
        action="store",
        default=FONT_FACE_MESLO,
        nargs="?",
        help="Font face file.",
        type=str,
    )
    parser.add_argument(
        "--font_size",
        "-fs",
        dest="fontSize",
        action="store",
        default=26,
        nargs="?",
        help="Font size.",
        type=int,
    )
    parser.add_argument(
        "--font_encod",
        "-fe",
        dest="fontEncod",
        action="store",
        default="unic",
        nargs="?",
        help="font format.",
        type=str,
    )

    parser.add_argument(
        "--backgroud-color",
        "-bc",
        dest="backgroud_color",
        action="store",
        default="white",
        nargs="?",
        help="Backgroud color.",
        type=str,
    )
    parser.add_argument(
        "--backgroud-transparency",
        "-bt",
        dest="backgroud_transparency",
        action="store",
        default=255,
        nargs="?",
        help="Backgroud transparency [0-255].",
        type=int,
    )
    
    parser.add_argument(
        "--text_fill",
        "-tf",
        dest="text_fill",
        action="store",
        default="black",
        nargs="?",
        help="Text color.",
        type=str,
    )
    parser.add_argument(
        "--margin",
        "-m",
        dest="margin",
        action="store",
        default=10,
        nargs="?",
        help="Image margin.",
        type=int,
    )

    parser.add_argument(
        "-v",
        "--verbose",
        help="increase output verbosity",
        dest="verbose",
        action="store_true",
    )

    args = parser.parse_args()

    if args.verbose:
        print("version: 0.1.0")
        exit(0)
    if not stdin.isatty():

        text = stdin.read()
        img = Txt2img(
            text=text,
            font_face=args.fontFace,
            font_size=args.fontSize,
            font_encoding=args.fontEncod,
            backgroud_color=args.backgroud_color,
            backgroud_transparency=args.backgroud_transparency,
            text_fill=args.text_fill,
            margin=args.margin,
        )

        img.save(args.output)
        img.show()
    else:
        parser.error(
            "It is necessary to receive an input through the pipe. example: tree | command2img."
        )

if __name__ == "__main__":
    main()