def location_conv(name):
    words = name.split(' ')
    address = {
        '00:2a:10:57:35:31': 'Rankine ',
        '00:2a:10:9b:8a:b1': 'Library ',
        'f8:4f:57:3a:21:11': 'James Watt School of Engineering',
        'd4:6d:50:f3:11:21': 'GUU',
        '84:78:ac:f0:22:a1': 'Frasers',
        'ec:e1:a9:6e:be:81': 'Boyd Orr',
        '00:2a:10:93:bf:f1': 'QMU',
        '70:79:b3:2d:6f:a1': 'EAST',
        'b8:62:1f:ac:60:81': 'WEST',
    }
    output = ' '
    for word in words:
        output += address.get(word, 'User Travelling') + ' '
    return output


name = input('>')
location_conv(name)
print(location_conv(name))


