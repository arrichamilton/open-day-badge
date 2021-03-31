def info_conv(place):
    information = {
        'Rankine': 'https://universitystory.gla.ac.uk/building/?id=18 ',
        'Library': 'https://universitystory.gla.ac.uk/building/?id=69 ',
        'James Watt School of Engineering': 'https://universitystory.gla.ac.uk/building/?id=112',
        'GUU': 'https://universitystory.gla.ac.uk/building/?id=50',
        'Frasers': 'https://universitystory.gla.ac.uk/building/?id=71',
        'Boyd Orr': 'https://universitystory.gla.ac.uk/building/?id=40',
        'QMU': 'https://universitystory.gla.ac.uk/building/?id=19',
        'EAST': 'https://en.wikipedia.org/wiki/University_of_Glasgow',
        'WEST': 'https://en.wikipedia.org/wiki/University_of_Glasgow',
    }
    return information.get(place, 'None')


def location_conv(name):
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
    return address.get(name, 'User Travelling')


start = input('enter start location>')
start_location = location_conv(start)
loc_int = []
loc_int.append(start_location)
loc = []
loc.append(start_location)


for i in range(1,10,1):
    name = input('>')
    loc_int.append(location_conv(name))
    if loc_int[i] != loc_int[i - 1]:
        loc.append(loc_int[i])
        if loc[-1] == 'User Travelling':
            z = 1
        else:
            print('Do you like this place?')
            x = input()
            if x == 'Yes':
                info_conv(loc[-1])
                print(info_conv(loc[-1]))
            else:
                print('Too Sad (❁´◡`❁)')

    else:
        print("same location")


print(loc)
