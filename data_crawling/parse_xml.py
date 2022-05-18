from lxml import etree
import lxml
from os.path import join, realpath, exists
from os import makedirs, listdir

if __name__ == '__main__':
    data_root = join(realpath('.'), 'Data', 'grobid_output')
    output_root = join(realpath('.'), 'Data', 'Springer_full_txt')
    if not exists(output_root):
        makedirs(output_root)

    filenames = listdir(data_root)
    for filename in filenames:
        try:
            root = etree.parse(join(data_root, filename))
            content = ""
            for element in root.iter("*"):
                if element.text is not None:
                    # exclude very short sentences and xml nodes that are related to GROBID
                    # if len(element.text) > 50 and 'GROBID' not in element.text:
                    content += element.text
                    if element.text[-1] != '.':
                        content += '. '
            with open(join(output_root, filename+'txt'), 'w', encoding='utf-8') as file:
                file.write(content)
        except lxml.etree.XMLSyntaxError:
            print(filename)
            continue

