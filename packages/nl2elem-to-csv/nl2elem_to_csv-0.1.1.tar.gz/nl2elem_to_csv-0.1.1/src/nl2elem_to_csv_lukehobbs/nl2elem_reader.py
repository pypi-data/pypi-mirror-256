import xml.etree.ElementTree


def read(filename) -> list[dict]:
    tree = xml.etree.ElementTree.parse(filename)
    root = tree.getroot().find('element')

    vertices = [vertex for vertex in root.iter('vertex')]
    rolls = [roll for roll in root.iter('roll')]

    if len(vertices) != len(rolls):
        raise ValueError('Number of vertices and rolls do not match')

    return [
        {
            'x': float(vertex.find('x').text),
            'y': float(vertex.find('y').text),
            'z': float(vertex.find('z').text),
            'strict': bool(vertex.find('strict') or 'false'),
            'roll': {
                'ux': float(roll.find('ux').text),
                'uy': float(roll.find('uy').text),
                'uz': float(roll.find('uz').text),
                'rx': float(roll.find('rx').text),
                'ry': float(roll.find('ry').text),
                'rz': float(roll.find('rz').text),
                'coord': float(roll.find('coord').text),
                'strict': bool(roll.find('strict').text),
            }
        } for vertex, roll in zip(vertices, rolls)
    ]
