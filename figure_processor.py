import os
from utils import parse_figures
from model import GPT
import fitz

class FigureProcessor:
    def __init__(self) -> None:
        self.gpt = GPT('gpt-4o')

    def extract_figures(self, paper, folder):
        self.repo_path = folder

        # read the figures from cache if it exists
        cache_file = os.path.join('Cache', f'{folder}_figs.txt')
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                res = f.read()
        else:
            prompt = f"""Please help extract all figures included in a scientific paper consisting of LaTeX files.

Please note that:
- A Latex figures is enclosed within blocks like \begin{{figure}}...\end{{figure}} or \begin{{figure*}}...\end{{figure*}}..
- The relative path of each figure must include a valid suffix, such as e.g., png, jpg, jpeg, or pdf.

The paper details are provided as follows:
{paper}

Example output format:

```Figure
Path: [the relative path of the figure]
Description: [briefly explain the content and purpose of this figure]
```
"""
            res = self.gpt.infer(user_prompt = prompt)
            # save the figures to cache to avoid re-processing, reducing time and token usage
            with open(cache_file, 'w') as f:
                f.write(res)
        self.figures = parse_figures(res, self.repo_path)


    def append_figures(self, content):
        cache_file = f'Cache/{self.repo_path}_raw_with_figs.txt'
        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                slide_text_with_figure = f.read()
        else:
            figure_descriptions = '\n'.join([f"This Figure's relative path is: {path}, its description is: {desc}\n" \
                                              for path, desc in self.figures])
            prompt = f"""Please help add appropriate figures to a series of slides.
The content of all candidate figures are: {figure_descriptions}.

The content of your input slides are: {content}.

The original content of an example slide is:
Slide: INDEX
Header: HEADER
Content: - CONTENT 1
- CONTENT 2
- CONTENT 3

The target output of this slide is:
Slide: INDEX
Header: HEADER
Content: - CONTENT 1
- CONTENT 2
- CONTENT 3
Figure: A FIGURE's RELATIVE PATH

You should either add the last line or not, keeping the other lines unchanged.

Please note:
- Keep the number of slides and their original content.
- Each figure should be used at most once (or not at all).
- Each slide should contain at most one figure.
- If a slide has no figure, don't change its content and keep the original slide.
- Output the target output directly, without further explanation.
- Ensure you retain the title.
"""
            res = self.gpt.infer(user_prompt = prompt)
            slide_text_with_figure = res
            with open(cache_file, 'w', encoding='utf-8') as f:
                f.write(slide_text_with_figure)
        return slide_text_with_figure


    def select_figures(self, content):
        figure_descriptions = '\n'.join([f'The usage of Figure "{path}" is: {desc}\n' \
                                          for path, desc in self.figures])

        prompt = f"""Please help choose a figure for a specific slide.
The content of the silde is: {content}

The candidate figures are: {figure_descriptions}

Please note:
- Only output "NO" if no figure is appropriate, or provide the relative path of the chosen figure.
"""
        res = self.gpt.infer(user_prompt = prompt)
        res = os.path.join(self.repo_path, res)
        if res.endswith('.pdf'):
            try:
                pix = fitz.open(res).load_page(0).get_pixmap()
                res = f'{res}.png'
                pix.save(res)
            except:
                res = 'NO'
        return res
