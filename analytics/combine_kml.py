from copy import deepcopy
from lxml import etree
from pykml import parser
from pykml.factory import KML_ElementMaker as KML
import sys

kml_out = None
for filename in sys.argv[1:]:
  with open(filename) as f:
    kml_in = parser.parse(f)
    root = kml_in.getroot()
    if kml_out is None:
      kml_out = deepcopy(kml_in)
      folder = kml_out.getroot().Document.Folder
      folder.name = 'all'
      for elem in folder.Placemark:
        folder.remove(elem)
    folder_in = kml_in.getroot().Document.Folder
    placemark = folder_in.Placemark
    placemark.name = folder_in.name
    kml_out.getroot().Document.Folder.append(deepcopy(placemark))
print etree.tostring(kml_out)
