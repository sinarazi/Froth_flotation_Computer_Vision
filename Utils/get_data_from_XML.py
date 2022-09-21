import numpy as np
import os
#from xml.etree import ElementTree
import lxml.etree as ElementTree

class XML_preprocessor(object):

    def __init__(self, data_path):
        self.path_prefix = data_path
        self.num_classes = 1
        self.data = dict()
        self._preprocess_XML()

    def _preprocess_XML(self): # processing each feature of a datum, such as height and so on.
        filenames = os.listdir(self.path_prefix)
        for filename in filenames:
            tree = ElementTree.parse("anno\\" + filename)
            root = tree.getroot()
            bounding_boxes = []
            one_hot_classes = []
            size_tree = root.find('size')
            width = float(size_tree.find('width').text)
            height = float(size_tree.find('height').text)
            for object_tree in root.findall('object'):
                for bounding_box in object_tree.iter('bndbox'):
                    xmin = float(bounding_box.find('xmin').text)/width
                    ymin = float(bounding_box.find('ymin').text)/height
                    xmax = float(bounding_box.find('xmax').text)/width
                    ymax = float(bounding_box.find('ymax').text)/height
                bounding_box = [xmin,ymin,xmax,ymax]
                bounding_boxes.append(bounding_box)
                class_name = object_tree.find('name').text
                one_hot_class = self._to_one_hot(class_name)
                one_hot_classes.append(one_hot_class)
            image_name = root.find('filename').text
            bounding_boxes = np.asarray(bounding_boxes)
            one_hot_classes = np.asarray(one_hot_classes)
            image_data = np.hstack((bounding_boxes, one_hot_classes))
            self.data[image_name] = image_data

    def _to_one_hot(self,name): # labeling each dataset 
        one_hot_vector = [0] * self.num_classes
        if name == 'nucleus':
            one_hot_vector[0] = 1
        else:
            print('unknown label: %s' %name)

        return one_hot_vector

## example on how to use it
import pickle
data = XML_preprocessor("C:\\Users\\Sina\\Desktop\\annotation_500").data  # convet xml to .p file
pickle.dump(data,open('Froth_500.p','wb'))
