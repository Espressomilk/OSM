import xml.etree.ElementTree as ET
import pymysql.cursors
import utils as ut
tree = ET.parse('../data/shanghai_dump.osm')
root = tree.getroot()
db = pymysql.connect(host="localhost", user="root", db="OSM4", charset='utf8')
cur = db.cursor()


def disableIndex(tables):
    cur.execute('lock table %s' % ','.join(['`%s` write' % table for table in tables]))
    for table in tables:
        cur.execute('alter table `%s` disable keys' % table)
        print('Index for table %s disabled' % table)


def enableIndex(tables):
    for table in tables:
        cur.execute('alter table `%s` enable keys' % table)
        print('Index for table %s enabled' % table)
    cur.execute('unlock tables')


def insertNodesPOIsNonPOIs():
    cnt = 0
    nodesError = open('Nodes_error.txt', 'w')
    poisError = open('POIs_error.txt', 'w')
    nonpoisError = open('NonPOIs_error.txt', 'w')
    for node in root.findall('node'):
        ver = node.attrib['version']
        lon = node.attrib['lon']
        lat = node.attrib['lat']
        point = "POINT(%s %s)" % (lon, lat)
        (ply,plx) = ut.mapping(float(lat),float(lon))
        planaxy = "POINT(%f %f)" % (plx, ply)
        nodeID = node.attrib['id']
        cnt += 1
        if(cnt % 1000 == 0):
            print('%s nodes inserted...' % cnt)
        try:
            cur.execute("insert into nodes(nodeID, version) values(%s, %s)", (nodeID, ver))
        except:
            print('Nodes Insert Error:', nodeID)
            nodesError.write(nodeID)
            nodesError.write('\n')
        if(ver == '1'):
            name = ''
            poitype = ''
            otherInfo = []
            for tag in node.findall('tag'):
                if(tag.attrib['k'] == 'name'):
                    name = tag.attrib['v']
                elif(tag.attrib['k'] == 'poitype'):
                    poitype = tag.attrib['v']
                else:
                    otherInfo.append(tag.attrib)
            # print("insert into pois(nodeID, position, name, poitype, otherInfo) values(%s, GeomFromText('%s'), %s, %s, %s)"% (nodeID, point, name, poitype, str(otherInfo)))
            try:
                cur.execute("insert into pois(nodeID, position, planaxy, name, poitype, otherInfo) values(%s, GeomFromText(%s), GeomFromText(%s), %s, %s, %s)", (nodeID, point, planaxy, name, poitype, str(otherInfo)))
            except:
                print('POIs Insert Error:', nodeID)
                poisError.write(nodeID)
                poisError.write('\n')
        else:
            otherInfo = node.findall('tag')
            try:
                cur.execute("insert into nonpois(nodeID, position, planaxy, otherInfo) values(%s, GeomFromText(%s), GeomFromText(%s), %s)", (nodeID, point, planaxy, str(otherInfo)))
            except:
                print('NonPOIs Insert Error:', nodeID)
                nonpoisError.write(nodeID)
                nonpoisError.write('\n')
        db.commit()
    nodesError.close()
    poisError.close()
    nonpoisError.close()

# nodeID=26609107 version=-1 上海浦东国际机场
# nodeID=26609111 version=-1 上海虹桥国际机场


def insertWaysWayNode():
    cnt = 0
    waysError = open('Ways_error.txt', 'w')
    for way in root.findall('way'):
        wayID = way.attrib['id']
        name = "NULL"
        isRoad = 0
        otherInfo = []
        cnt += 1
        if(cnt % 1000 == 0):
            print('%s ways inserted...' % cnt)
        for tag in way.findall('tag'):
            if(tag.attrib['k'] == 'name'):
                name = tag.attrib['v']
            elif(tag.attrib['k'] == 'highway'):
                isRoad = 1
            else:
                otherInfo.append(tag.attrib)
        if(name == "NULL"):
            cur.execute("insert into ways(wayID, LineString, name, isRoad, otherInfo) values(%s, NULL, NULL, %s, %s)", (wayID, isRoad, str(otherInfo)))
        else:
            cur.execute("insert into ways(wayID, LineString, name, isRoad, otherInfo) values(%s, NULL, %s, %s, %s)", (wayID, name, isRoad, str(otherInfo)))
        node_order = 0
        for nd in way.findall('nd'):
            nodeID = nd.attrib['ref']
            node_order += 1
            cur.execute("insert into waynode(wayID, nodeID, node_order) values(%s, %s, %s)", (wayID, nodeID, node_order))
        db.commit()
    waysError.close()


def NodeInsert():
    disableIndex(['nodes', 'pois', 'nonpois'])
    insertNodesPOIsNonPOIs()
    enableIndex(['nodes', 'pois', 'nonpois'])


def WayInsert():
    disableIndex(['ways', 'waynode'])
    insertWaysWayNode()
    enableIndex(['ways', 'waynode'])


if __name__ == "__main__":
    NodeInsert()
    WayInsert()
