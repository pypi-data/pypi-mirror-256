# -*- coding: utf-8 -*-

from fretty import generate_svg, write_image
import os


class DoumentProcessor:
    def __init__(self, embedded=True, png_images=False, output_file=None):
        self.embedded = embedded
        self.png_images = png_images
        self.output_file = output_file

    @property
    def document_dir(self):
        return os.path.dirname(self.output_file)

    @property
    def image_extension(self):
        return 'png' if self.png_images else 'svg'

    def process_file(self, input_file):
        with open(input_file) as f:
            return self.process_text(f.read())

    def process_text(self, input):
        return self._process(input)

    def _process(self, input):
        return input
    

class HTMLDoumentProcessor(DoumentProcessor):

    def _process(self, html_input):
        import lxml.html

        doc = lxml.html.document_fromstring(html_input)
        count = 0
        for node in doc.findall(".//fretty"):
            lines = node.text.strip().split("\n")
            svg = generate_svg(
                lines,
                width=node.get('width'),
                height=node.get('height'),
                embedded=self.embedded
            )
            if self.embedded:
                replace_node = lxml.html.fromstring(svg)
            else:
                image_file = write_image(f"fretty-{count}.{self.image_extension}", svg, target_path=self.document_dir)
                replace_node = lxml.html.fromstring(f'<img src="{image_file}" />')
            node.getparent().replace(node, replace_node)
            count += 1
        return lxml.html.tostring(doc, encoding='unicode')
    

class XHTMLDoumentProcessor(DoumentProcessor):
    def _process(self, xhtml_input):
        from xml.dom.minidom import parseString

        dom = parseString(xhtml_input)
        count = 0
        for node in dom.getElementsByTagName("fretty"):
            lines = [l for child in node.childNodes for l in child.data.strip().split("\n")]
            svg = generate_svg(
                lines,
                width=node.getAttribute('width'),
                height=node.getAttribute('height'),
                embedded=self.embedded
            )
            if self.embedded:
                replace_node = parseString(svg)
            else:
                image_file = write_image(f"fretty-{count}.{self.image_extension}", svg, target_path=self.document_dir)
                replace_node = parseString(f'<img src="{image_file}" />')
            node.parentNode.replaceChild(replace_node.documentElement, node)
            count += 1
        return dom.toxml()