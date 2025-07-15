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
    
    instructions = """The following is the raw textual data from an HTML Website. Please take the data and create a clear and organized structure for the data in a textual format.
    
    Ensure that you put your answer between ``` and ```, so that it can be parsed by the code, and please separate each sub-section/section with '<---->'.
    """

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
            with open(raw_data_path, "r", encoding="utf-8") as f:
                raw_data = f.read()
            
            response = client.models.generate_content(
                model=model,
                contents=instructions + "\n\n" + raw_data,
            )
            
            refined_data_path = os.path.join(refined_data_dir, filename)
            with open(refined_data_path, "w", encoding="utf-8") as f:
                f.write(response.text)

