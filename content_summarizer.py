import os
from utils import parse_summary
from model import GPT
import json

class ContentSummarizer:
    def __init__(self) -> None:
        self.gpt = GPT('gpt-4o')

    def summarize(self, paper, folder):
        self.repo_path = folder
        
        # read the smmarization from cache if it exists
        cache_file = os.path.join('Cache', f'{folder}_summarization.json')
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                summarize = json.load(f)
            slide_number, title, contents = summarize['slide_number'], summarize['title'], summarize['contents']
        else:
            prompt = f"""Please help summarize a scientific paper consisting of LaTeX or plain text files.
Follow these instructions:
- Automatically detect the number of sections in the paper.
- Indicate the number of sections in the format: ```number [number]```
- Write a summary for each section.
- Format each summary of section as follows: ```[section name]\n [content of summary]```
- Consider using bullet points to structure each section's summary.

The paper details are provided as follows:
{paper}

Example format: (Add or remove sections based on the content of the paper)
```
Title: [title of this paper]

```Introduction
[content of introduction]
```

```Background
[content of Background]
```

```Approach
[content of Approach]
```

```Evaluation
[content of Evaluation]
```

```Discussion
[content of Discussion]
```

```Threats
[content of Threats]
```

```Conclusion
[content of Conclusion]
```
"""
            res = self.gpt.infer(user_prompt = prompt)
            slide_number, title, contents = parse_summary(res)
            # save the summary to cache to avoid re-summarizing, reducing time and token usage
            with open(cache_file, 'w') as f:
                json.dump({'slide_number': slide_number, 'title': title, 'contents': contents}, f)
        return slide_number, title, contents