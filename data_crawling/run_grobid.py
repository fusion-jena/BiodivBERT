from os.path import realpath, join, exists
from os import makedirs
from grobid_client_python.grobid_client.grobid_client import GrobidClient

if __name__ == '__main__':
    client = GrobidClient(config_path=join(realpath('.'), 'grobid_client_python', "config.json"))
    pdfs_path = join(realpath('.'), 'Data', 'Springer_PDFs')
    output_path = join(realpath('.'), 'Data', 'Grobid_output')
    if not exists(output_path):
        makedirs(output_path)
    client.process("processFulltextDocument", pdfs_path, output=output_path,  n=10)
