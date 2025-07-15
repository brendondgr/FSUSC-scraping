import os
from google import genai

def refine_all_raw_data(api_key):
    """
    Refines all raw text files in the raw_data directory using the Gemini API
    and saves them to the refined_data directory.
    """
    refined_data_dir = "./refined_data"
    raw_data_dir = "./raw_data"

    if not os.path.exists(refined_data_dir):
        os.makedirs(refined_data_dir)

    client = genai.Client(api_key=open("api_key.txt", "r").read())    
    model = "gemini-2.5-pro"
    
    instructions = (
        "The following is the raw textual data from an HTML Website. Please take the data and create "
        "a clear and organized structure for the data in a LaTeX format.\n\n"
        "Do not include any other text in your response, just the LaTeX code. The code should assume "
        "that the user already has a title page and table of contents. You should add in 'section' and "
        "'subsection' commands as needed. The current code is as follows:\n"
        "\\\\documentclass[12pt,a4paper]{article}\n\n"
        "% Packages %\n"
        "\\\\usepackage{titling} % Gives Page Title\n" 
        "\\\\usepackage{setspace} % Gives Ability to use \\\\onehalfspacing and \\\\doublespacing\n"
        "\\\\usepackage{times} % Time New Roman Font\n"
        "\\\\usepackage{indentfirst} % Makes the indentation after section\n"
        "\\\\usepackage{graphicx} % Graphics (Images)\n"
        "\\\\graphicspath{../images/}\n\n"
        "% Bibliography %\n"
        "\\\\usepackage{natbib}\n"
        "\\\\usepackage{hyperref}\n"
        "\\\\bibliographystyle{plain} % Style Here\n\n"
        "% Following Are From TablesGenerator.com %\n"
        "\\\\usepackage[table,xcdraw]{xcolor}\n"
        "\\\\usepackage{colortbl}\n\n"
        "% Title, author, and date %\n"
        "\\\\title{Title}\n"
        "\\\\author{Brendon Gutierrez \\\\\\\\ \\\\textit{Class Code: Class name}}\n"
        "\\\\date{\\\\today}\n\n\n"
        "\\\\begin{document}\n\n"
        "There is also no need to provide \\\\end{document} at the end of your response, as I will do "
        "this myself. As stated, do not include the above text in your response, as I will be adding it in myself. "
        "Finally, after each section is started, add the URL for reference to the webpage is came from.\n\n"
        "Please convert the following into LaTeX Code, as outlined above:"
    )

    if not os.path.exists(raw_data_dir):
        print("No raw data directory found.")
        return

    raw_data_files = os.listdir(raw_data_dir)
    if not raw_data_files:
        print("No raw data files found to refine.")
        return

    for filename in raw_data_files:
        if filename.endswith(".txt"):
            raw_data_path = os.path.join(raw_data_dir, filename)
            refined_data_path = os.path.join(refined_data_dir, filename)
            
            # Skip if refined file already exists
            if os.path.exists(refined_data_path):
                continue
                
            with open(raw_data_path, "r", encoding="utf-8") as f:
                raw_data = f.read()
            
            response = client.models.generate_content(
                model=model,
                contents=instructions + "\n\n" + raw_data,
            )
            
            with open(refined_data_path, "w", encoding="utf-8") as f:
                f.write(response.text)

