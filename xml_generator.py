#!/usr/bin/env python

"""Generating file of xml for annotation."""

import os
import sys
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from element_tree_pretty import prettify

# set of image info
_FOLDER = 'VOC2007'

# set of item info
_DATABASE = 'The VOC2007 Database'
_ANNOTATION = 'PASCAL VOC2007'
_IMG_DEPTH = '3'
_SEGMENTED = '0'
_POSE = 'Frontal'
_TRUNCATED = '0'
_DIFFICULT = '0'

_pretty_root = None


def generate_xml(img_info, item_info):
    """Generating format of xml for annotation."""
    root = ET.Element('annotation')
    ET.SubElement(root, 'folder').text = _FOLDER
    ET.SubElement(root, 'filename').text = img_info['name']

    source_tag = ET.SubElement(root, 'source')
    ET.SubElement(source_tag, 'database').text = _DATABASE
    ET.SubElement(source_tag, 'annotation').text = _ANNOTATION
    ET.SubElement(source_tag, 'image').text = ''
    ET.SubElement(source_tag, 'flickrid').text = ''

    owner_tag = ET.SubElement(root, 'owner')
    ET.SubElement(owner_tag, 'flickrid').text = ''
    ET.SubElement(owner_tag, 'name').text = ''

    size_tag = ET.SubElement(root, 'size')
    ET.SubElement(size_tag, 'width').text = str(img_info['size']['h'])
    ET.SubElement(size_tag, 'height').text = str(img_info['size']['w'])
    ET.SubElement(size_tag, 'depth').text = _IMG_DEPTH

    ET.SubElement(root, 'segmented').text = _SEGMENTED

    object_tag = ET.SubElement(root, 'object')
    ET.SubElement(object_tag, 'name').text = item_info['name']
    ET.SubElement(object_tag, 'pose').text = _POSE
    ET.SubElement(object_tag, 'truncated').text = _TRUNCATED
    ET.SubElement(object_tag, 'difficult').text = _DIFFICULT
    bndbox_tag = ET.SubElement(object_tag, 'bndbox')

    bndbox = item_info['bndbox']
    ET.SubElement(bndbox_tag, 'xmin').text = str(bndbox['x']['min'])
    ET.SubElement(bndbox_tag, 'ymin').text = str(bndbox['y']['min'])
    ET.SubElement(bndbox_tag, 'xmax').text = str(bndbox['x']['max'])
    ET.SubElement(bndbox_tag, 'ymax').text = str(bndbox['y']['max'])
    global _pretty_root
    _pretty_root = prettify(root)


def _make_directory(directory):
    """Make a directory and create it which doesn't exist."""
    # convert relative path to absolute path
    _directory = os.path.expanduser(directory)
    if not os.path.exists(_directory):
        os.makedirs(_directory)
    return _directory


def save_file(filename, directory='./', display=False):
    """Saving file of generation."""
    path = os.path.join(_make_directory(directory), filename)
    with open(path, 'w') as f:
        if display:
            print _pretty_root
        if _pretty_root is not None:
            f.write(_pretty_root)


def _test():
    """Testing for xml generator."""
    generate_xml(
        img_info={'name': '01-00001.jpg', 'size': {'w': 640, 'h': 480}},
        item_info={
            'name': 'test',
            'bndbox': {
                'x': {'min': 88, 'max': 621},
                'y': {'min': 23, 'max': 991}
            }
        }
    )
    save_file(filename='test01-00001.xml', directory='./test01', display=True)


if __name__ == '__main__':
    _test()
