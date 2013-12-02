def playerIcons(poi):
    if poi['id'] == 'Player':
        poi['icon'] = "http://overviewer.org/avatar/%s" % poi['EntityId']
        return "Last known location for %s" % poi['EntityId']

worlds['Sigma'] = "/home/sigma/minecraft-rakefile/world-temp/world"
outputdir = "/srv/http/sigma"

renders["day"] = {
        'world': 'Sigma',
        'title': 'Day',
        'rendermode': 'smooth_lighting',
        'markers': [dict(name="Players", filterFunction=playerIcons)]
        }

renders["night"] = {
        'world': 'Sigma',
        'title': 'Night',
        'rendermode': 'smooth_night',
        'markers': [dict(name="Players", filterFunction=playerIcons)]
        }

