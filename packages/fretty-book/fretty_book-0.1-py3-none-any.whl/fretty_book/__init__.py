# -*- coding: utf-8 -*-
from .processor import HTMLDoumentProcessor, XHTMLDoumentProcessor

__version__ = '0.1'


_processors = {
    'html': lambda _f: HTMLDoumentProcessor,
    'xhtml': lambda _f: XHTMLDoumentProcessor,
    'auto': lambda input_file: XHTMLDoumentProcessor if input_file.lower().endswith('.xhtml') else HTMLDoumentProcessor
}


def main():
    import argparse

    parser = argparse.ArgumentParser(
                prog='fretty-book',
                description='fretty-book can replace inline fretty markup within documents with the generated images'
                )
    parser.add_argument('input_file')
    parser.add_argument('-o', '--output-file', help="output file name")
    parser.add_argument('--png', action='store_true', help="use png images files instead of svg")
    parser.add_argument('-e', '--embed-svg', action='store_true',
                        help="embed svg into the document")
    parser.add_argument('-p', '--processor', default="auto", choices=list(_processors.keys()),
                        help=f"type of input processing {list(_processors.keys())} (auto tryes to determine the processor by the file extension)")
    parser.add_argument('-V', '--verbose', action='store_true')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')
    args = parser.parse_args()

    processor_class = _processors[args.processor](args.input_file)
    
    if args.verbose:
        print(f"use processor: {processor_class.__name__}")
    
    processor = processor_class(embedded=args.embed_svg, png_images=args.png, output_file=args.output_file)
    output = processor.process_file(args.input_file)
    
    if args.output_file:
        if args.verbose:
            print(f"write file: {args.output_file}")
        with open(args.output_file, 'w') as o:
            o.write(output)
    else:
        print(output)