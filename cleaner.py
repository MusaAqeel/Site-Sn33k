# open vscode through anaconda
## pip install bs4
#  wget -r -np -nd -A.html,.txt,.tmp -P websites https://your-website # download the website
# install beautifulsoup4
# configure path to the directory where the files are stored
# run the script



import os
import urllib.request
from bs4 import BeautifulSoup
import chardet
import shutil
import ssl

# Define the URL to scrape
url = "https://www.reddit.com/r/personalfinance/wiki/index/"

# Create an SSL context that doesn't verify certificates
context = ssl._create_unverified_context()

# Use urllib to download the website
print("Downloading webpage...")
response = urllib.request.urlopen(url, context=context)
content = response.read()

# Detect the encoding
encoding = chardet.detect(content)['encoding']

# Decode the content
html_content = content.decode(encoding)

# Create the 'websites' directory if it doesn't exist
os.makedirs('websites', exist_ok=True)

# Save the content to a file
with open('websites/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Download complete. Proceeding with cleaning...")

def get_unique_filename(output_file_path):
    counter = 1
    original_output_file_path = output_file_path
    while os.path.exists(output_file_path):
        output_file_path = original_output_file_path.replace(".html", f"_{counter}.html")
        counter += 1
    return output_file_path

# Define the directory path
dir_path = "websites"
output_dir = "websites"

# Loop through all subdirectories and files in the directory
for root, dirs, files in os.walk(dir_path, topdown=False):
    for filename in files:
        # Construct the full file path
        file_path = os.path.join(root, filename)

        # Check if the path is a file
        if os.path.isfile(file_path):
            try:
                # Detect the file's encoding using chardet
                with open(file_path, 'rb') as file:
                    raw_data = file.read()
                    encoding = chardet.detect(raw_data)['encoding']

                # Read the file content with the detected encoding
                with open(file_path, 'r', encoding=encoding) as file:
                    file_content = file.read()

                # Create a Beautiful Soup object
                soup = BeautifulSoup(file_content, features="html.parser")

                # Extract only the main content
                main_content = soup.find('div', class_='md wiki')
                if main_content:
                    # Construct the output file path with .html extension
                    output_file_path = os.path.join(output_dir, os.path.basename(filename).split(".")[0] + ".html")

                    # Get a unique file name if the file already exists
                    output_file_path = get_unique_filename(output_file_path)

                    # Save the main content to a file in UTF-8
                    with open(output_file_path, 'w', encoding='utf-8') as file:
                        file.write(str(main_content))

                # Delete the original file
                os.remove(file_path)

            except UnicodeDecodeError:
                print(f"Error decoding file: {file_path}")

    # Delete the original directories
    for directory in dirs:
        shutil.rmtree(os.path.join(root, directory))

print("Scraping and cleaning completed.")