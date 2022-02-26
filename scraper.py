import os
import re
import toml

from requests_html import HTMLSession

data_path = "data"

class Parser():

    def __init__(self):
        session = HTMLSession()
        self.r = session.get(self.url)
        self.r.html.render()
        self.data = []

    def write(self):
        for d in self.data:
            # Normalise and sanitize the title into a filename
            filename = d['title'].lower()
            filename = re.sub(r'[^a-z0-9]', '-', filename)
            filename = re.sub(r'-+', '-', filename)
            filename = f"{filename}.toml"
            
            path = os.path.join(data_path, filename)

            # Write the data out to the file
            with open(path, "w") as f:
                print(f"writing: {path}")
                toml.dump(d, f)

        
class XRPLGranteeParser(Parser):

    url = "https://xrplgrants.org/grantees"
    
    def parse(self):
        for block in self.r.html.find(".grantee-block"):
            try:
                url = block.find('h4')[0].find('a')[0].attrs['href']
            except IndexError:
                url = ""
            title = block.find('h4')[0].text
            
            data = {'title': title,
                    'url': url
                    }

            self.data.append(data)


if __name__ == '__main__':
    parser = XRPLGranteeParser()
    parser.parse()
    parser.write()