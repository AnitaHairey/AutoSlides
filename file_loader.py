import os
from pypdf import PdfReader
from utils import read_file, remove_comment, add_content

class FileLoader:
    def __init__(self) -> None:
        return

    def load_tex_file(self, folder):
        # load all tex files in the folder recursively to self.tex_names
        files = os.listdir(folder)
        files = [os.path.join(folder, file) for file in files]
        self.tex_names = self.tex_names + [file for file in files if file.endswith('.tex')]
        sub_folders = [file for file in files if os.path.isdir(file)]
        for sub_folder in sub_folders:
            self.load_tex_file(sub_folder)

    def load(self, folder, file_type=1):
        if file_type == 1: # tex
            self.tex_names = []
            self.load_tex_file(folder)
            self.tex_contents = [read_file(tex) for tex in self.tex_names]
            self.tex_contents = [remove_comment(file) for file in self.tex_contents]
            # The paper format is:
            # The conent of file `file_name.tex` is ~~~ tex code ~~~.
            paper = [add_content(os.path.basename(tex_name), tex_content) for tex_name, tex_content in zip
            (self.tex_names, self.tex_contents)]
            return paper
        elif file_type == 2:
            # TODO: Implement pdf loader and figure extraction
            files = os.listdir(folder)
            self.pdf_name = [file for file in files if file.endswith('.pdf')][0]
            reader = PdfReader(os.path.join(folder, self.pdf_name))
            self.pdf_content = ""
            for page in reader.pages:
                self.pdf_content += page.extract_text()
            return self.pdf_content
        elif file_type == 3:
            # TODO: Implement word loader
            return
