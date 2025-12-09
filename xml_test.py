import xml.etree.ElementTree as et
tree=et.ElementTree(file="xml_test.xml")
root=tree.getroot()
root.tag
for child in root:
    print('tag:',child.tag,'attributes:',child.attrib)
    for grandchild in child:
        print('\ttag:',grandchild.tag,\
              'attributes:',grandchild.attrib)
