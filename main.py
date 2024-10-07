import os
import time
from content_summarizer import ContentSummarizer
from file_loader import FileLoader
from figure_processor import FigureProcessor
from slides_generator import SlidesGenerator

def generate(file_type, folder, theme):
    loader = FileLoader()
    summarizer = ContentSummarizer()
    figure_processor = FigureProcessor()
    generator = SlidesGenerator()

    print("\nLoading the contents...")
    paper = loader.load(folder, file_type)

    print("Summarizing the contents and extracting figures...")
    slide_number, title, contents = summarizer.summarize(paper, folder)
    figure_processor.extract_figures(paper, folder)

    print("Generating the powerpoint...")
    slide_text = generator.generate_raw_text(title, contents, slide_number, folder)
    # TODO: move append_figures after generate_slide
    slide_text_with_figure = figure_processor.append_figures(slide_text)
    slide_path = generator.generate_slide(slide_text_with_figure, theme, title, folder)

    print ("The powerpoint has been generated at:", slide_path)

def main():
    print("Welcome to the powerpoint generator!\n")

    doc_type = int(input("Please select the type of document you want to generate (1: tex, 2: pdf, 3: word): "))
    if not doc_type or doc_type > 3 or doc_type < 1:
        print("Invalid document type, please try again and select a valid document type.")
        return

    file_path = input("Please enter the path of the file folder: ")
    if not file_path or not os.path.exists(file_path):
        print("Invalid file path, please try again and enter a valid file path.")
        return

    print("The following themes are available for the powerpoint:")
    print("Design 1 = Envelope, beige")
    print("Design 2 = Blue Bubble")
    print("Design 3 = Light Blue Black")
    print("Design 4 = Black, dark")
    print("Design 5 = wood")
    print("Design 6 = Multicolored, Simple")
    print("Design 7 = Black, white")
    theme = int(input("Please select theme of the powerpoint (1-7): "))
    if not theme or theme > 7 or theme < 1:
        theme = 7
        print("Invalid theme number, default theme will be applied.")
    
    start_time = time.time()
    generate(doc_type, file_path, theme)
    end_time = time.time()
    print ("Time used for generating:", round((end_time - start_time), 2))
    
if __name__ == '__main__':
    main()
