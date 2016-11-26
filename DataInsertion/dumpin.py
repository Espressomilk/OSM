import xml.etree.ElementTree as ET
import pymysql.cursors

tree = ET.parse('../data/shanghai_dump.osm')
root = tree.getroot()
db = pymysql.connect(host="localhost", user="root", db="OSM2", charset='utf8')
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
        point = "POINT(%s %s)"%(lon, lat)
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
                cur.execute("insert into pois(nodeID, position, name, poitype, otherInfo) values(%s, GeomFromText(%s), %s, %s, %s)", (nodeID, point, name, poitype, str(otherInfo)))
            except:
                print('POIs Insert Error:', nodeID)
                poisError.write(nodeID)
                poisError.write('\n')
        else:
            otherInfo = node.findall('tag')
            try:
                cur.execute("insert into nonpois(nodeID, position, otherInfo) values(%s, GeomFromText(%s), %s)", (nodeID, point, str(otherInfo)))
            except:
                print('NonPOIs Insert Error:', nodeID)
                nonpoisError.write(nodeID)
                nonpoisError.write('\n')
        db.commit()
    nodesError.close()
    poisError.close()
    nonpoisError.close()
    

def insertWays():
    waysError = open('Ways_error.txt', 'w')
    for way in root.findall('way'):
        pass


if __name__ == "__main__":
    disableIndex(['nodes', 'pois', 'nonpois'])
    insertNodesPOIsNonPOIs()
    enableIndex(['nodes', 'pois', 'nonpois'])