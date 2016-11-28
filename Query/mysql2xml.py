#-*-coding:utf8-*-
import pymysql.cursors

db = pymysql.connect(host="localhost", user="root", db="OSM2", charset='utf8')
cur = db.cursor(pymysql.cursors.DictCursor)


def QueryNodesByRectangular(x1, y1, x2, y2):
    poly = 'Polygon((%s %s, %s %s, %s %s, %s %s, %s %s))' % (x1, y1, x1, y2, x2, y2, x2, y1, x1, y1)
    # print(poly)
    cur.execute("select nodeID, AsText(position) as position, name, poitype, otherInfo from pois where MBRContains(GeomFromText('%s'), position)" % poly)
    poiresult = cur.fetchall()
    cur.execute("select nodeID, AsText(position) as position, otherInfo from nonpois where MBRContains(GeomFromText('%s'), position)" % poly)
    nonpoiresult = cur.fetchall()
    # print(poiresult)
    return poiresult, nonpoiresult


def QueryWaysByRectangular(x1, y1, x2, y2):
    poly = 'Polygon((%s %s, %s %s, %s %s, %s %s, %s %s))' % (x1, y1, x1, y2, x2, y2, x2, y1, x1, y1)
    cur.execute("select wayID, name, isRoad, otherInfo from ways where wayID in (select distinct wayID from nonpois natural join waynode where MBRContains(GeomFromText('%s'), position))" % poly)
    part1 = cur.fetchall()
    cur.execute("select wayID, name, isRoad, otherInfo from ways where wayID in (select distinct wayID from pois natural join waynode where MBRContains(GeomFromText('%s'), position))" % poly)
    part2 = cur.fetchall()
    if(len(part1) > 0 and len(part2) > 0):
        return part1 + part2
    if(len(part1) > 0): 
        return part1
    return part2




def xmlConstruction(xmlname, pois, nonpois, ways, minlat, maxlat, minlon, maxlon):
    newXML = open("../XML/%s" % xmlname, 'w')
    newXML.write("""<?xml version="1.0" encoding="UTF-8"?>\n<osm version="0.6" generator="SZZ_IMAP 0.0.1">\n""")
    newXML.write(""" <bounds minlat="%s" minlon="%s" maxlat="%s" maxlon="%s"/>\n""" % (minlat, minlon, maxlat, maxlon))
    for row in pois:
        lon = row['position'].split('POINT(')[1].split(' ')[0]
        lat = row['position'].split('POINT(')[1].split(' ')[1][:-1]
        # print(lon, lat)
        newXML.write("""  <node id="%s" lat="%s" lon="%s" visible="true" version="1">\n""" % (row['nodeID'], lat, lon))
        newXML.write("""   <tag k="name" v="%s"/>\n""" % row['name'])
        otherInfo = eval(row['otherInfo'])
        for dic in otherInfo:
            newXML.write("""   <tag k="%s" v="%s"/>\n""" % (dic['k'], dic['v']))
        newXML.write("""  </node>\n""")
    for row in nonpois:
        lon = row['position'].split('POINT(')[1].split(' ')[0]
        lat = row['position'].split('POINT(')[1].split(' ')[1][:-1]
        otherInfo = eval(row['otherInfo'])
        if(len(otherInfo) == 0):
            newXML.write("""  <node id="%s" lat="%s" lon="%s" visible="true" version="-1"/>\n""" % (row['nodeID'], lat, lon))
        else:
            newXML.write("""  <node id="%s" lat="%s" lon="%s" visible="true" version="-1">\n""" % (row['nodeID'], lat, lon))
            for dic in otherInfo:
                newXML.write("""   <tag k="%s" v="%s"/>\n""" % (dic['k'], dic['v']))
            newXML.write("""  </node>\n""")
    for row in ways:
        newXML.write("""  <way id="%s" visible="true">\n""" % row['wayID'])
        cur.execute("select nodeID, node_order from waynode where wayID=%s order by node_order" % row['wayID'])
        nodeIDs = cur.fetchall()
        for second_row in nodeIDs:
            newXML.write("""   <nd ref="%s"/>\n""" % second_row['nodeID'])
        if(row['isRoad'] != "0"):
            newXML.write("""   <tag k="highway" v="%s"/>\n""" % row['isRoad'])
        if(row['name'] != None):
            newXML.write("""   <tag k="name" v="%s"/>\n""" % row['name'])
        otherInfo = eval(row['otherInfo'])
        for dic in otherInfo:
            newXML.write("""   <tag k="%s" v="%s"/>\n""" % (dic['k'], dic['v']))
        newXML.write("""  </way>\n""")
    newXML.write("""</osm>""")


if __name__ == "__main__":
    poiresult, nonpoiresult = QueryNodesByRectangular(120.6, 30.9, 120.7, 31)
    waysresult = QueryWaysByRectangular(120.6, 30.9, 120.7, 31)
    xmlConstruction('text.xml', poiresult, nonpoiresult, waysresult, 31.2, 121.3, 31.21, 121.31)