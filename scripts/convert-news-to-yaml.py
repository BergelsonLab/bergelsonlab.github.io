# This is the script that chatgpt wrote for the task. I didn't run this script. Instead, I copied the output from  the
# chatgpt web ui and then compared what Jekyll built to the original HTML. Use with caution.
from bs4 import BeautifulSoup
import markdownify as md
import yaml

def clean_html_to_markdown(html_content):
    # Convert HTML to Markdown and trim whitespace
    return md.markdownify(html_content).strip()

class CustomDumper(yaml.SafeDumper):
    def write_line_break(self, data=None):
        super().write_line_break(data)
        if len(self.indents) == 1:
            super().write_line_break()

def process_news_items(html_file_path, yaml_output_path):
    # Load and parse the HTML content
    with open(html_file_path, 'r') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract and process news items
    news_items = []
    for div in soup.find_all("div", class_="3u 12u(mobile)"):
        news_item = {}
        img_tag = div.find("img")
        news_item['image'] = img_tag['src'] if img_tag else None

        h3_tag = div.find("h3")
        if h3_tag:
            news_item['title'] = h3_tag.text.strip()

        date_tag = div.find("ul", class_="meta")
        if date_tag:
            news_item['date'] = date_tag.text.strip()

        description_html = ''.join(map(str, div.find_all('br')[-1].next_siblings))
        news_item['description'] = clean_html_to_markdown(description_html)

        news_items.append(news_item)

    # Write the news items to the YAML output file
    with open(yaml_output_path, 'w') as yaml_file:
        yaml.dump(news_items, yaml_file, Dumper=CustomDumper, allow_unicode=True)

# Path to the HTML input file and desired YAML output file
html_file_path = '/mnt/data/news.html'  # Adjust the path to your HTML file
yaml_output_path = '/mnt/data/streamlined_news_items.yaml'  # Desired output YAML file path

# Process the news items and write to YAML
process_news_items(html_file_path, yaml_output_path)

print(f"News items have been processed and saved to {yaml_output_path}")
