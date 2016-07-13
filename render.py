
import os

CONTENT_DIR = 'content'
OUTPUT_DIR = 'output'

def main():
    with open('base.html', 'r') as f:
        html = f.read()

    for md_file in os.listdir(CONTENT_DIR):
        path = os.path.join(CONTENT_DIR, md_file)
        with open(path, 'r') as f:
            md_html = html % f.read()
            output_path = os.path.join(OUTPUT_DIR, os.path.splitext(md_file)[0] + '.html')
            with open(output_path, 'w') as o:
                o.write(md_html)
    print('finished!')

if __name__ == '__main__':
    main()
