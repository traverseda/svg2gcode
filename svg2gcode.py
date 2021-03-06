#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET
import shapes as shapes_pkg
from shapes import point_generator
from config import *

def generate_gcode():
    svg_shapes = set(['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path'])
    
    tree = ET.parse(sys.stdin)
    root = tree.getroot()
    
    width = float(root.get('width'))
    height = float(root.get('height'))
    scale_x = bed_max_x / max(width, height)
    scale_y = bed_max_y / max(width, height)

    print preamble 
    
    for elem in root.iter():
        
        try:
            _, tag_suffix = elem.tag.split('}')
        except ValueError:
            continue

        if tag_suffix in svg_shapes:
            shape_class = getattr(shapes_pkg, tag_suffix)
            shape_obj = shape_class(elem)
            d = shape_obj.d_path()
            if d:
                print shape_preamble 
                p = point_generator(d, smoothness)
                for x,y in p:
                    print "G1 X%0.1f Y%0.1f" % (scale_x*x, scale_y*y) 
                print shape_postamble

    print postamble 

if __name__ == "__main__":
    generate_gcode()



