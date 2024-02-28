import random
import re
import cairosvg

#from CairoSVG import svg2png

generated_files = input('Number of files to generate: ')
target_path = './data/dataverses/dataverse-performance-demo/datasets/performance-test/files'

with open('dv_logo_hd.svg', 'r') as file:
    svg_code = file.read()

for iteration in range(int(generated_files)):
    random_color = '#' + ''.join(random.choices('0123456789ABCDEF', k=6))
    svg_code_tmp = re.sub(r'#c65b28', random_color, svg_code)
    destination_path = (
        f"{target_path}/dv_logo_{str(iteration).zfill(5)}.png"
    )
    cairosvg.svg2png(bytestring=svg_code_tmp, write_to=destination_path)