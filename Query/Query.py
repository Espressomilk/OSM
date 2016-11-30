import pymysql.cursors
import operator
import utils as ut
import time
import mysql2xml

db = pymysql.connect(host="localhost", user="root", db="OSM4", charset='utf8')
cur = db.cursor(pymysql.cursors.DictCursor)


def Query1ByNodeID(nodeID):
    cur.execute('select * from ways where wayID in (select wayID from waynode where nodeID=%s)' % nodeID)
    queryResult = cur.fetchall()
    isIntersection = 0
    if(len(queryResult) > 1):
        isIntersection = 1
    return isIntersection, queryResult


def Query2ByWayID(wayID):
    cur.execute('select * from nodes where nodeID in (select nodeID from waynode where wayID=%s)' % wayID)
    result = cur.fetchall()
    ans = []
    for row in result:
        # print(row['version'], row['nodeID'])
        if(row['version'] == 1):
            cur.execute('select nodeID, AsText(position) as position, name, poitype, otherInfo from pois where nodeID=%s' % row['nodeID'])
            tmpRes = cur.fetchall()
            ans.append(tmpRes)
        else:
            cur.execute('select nodeID, AsText(position) as position, otherInfo from nonpois where nodeID=%s' % row['nodeID'])
            tmpRes = cur.fetchall()
            ans.append(tmpRes)
    return ans


def Query3ByNameOfRoad(name):
    cur.execute("select * from ways where name like('%%%s%%')" % name)
    result = cur.fetchall()
    print(result)
    return result


def Query4ByLLR(lat, lon, rad):
    rad_ori = rad
    rad = rad*1.33
    (y, x) = ut.mapping(lat, lon)
    cur.execute("set @poly='Polygon((%f %f,%f %f,%f %f,%f %f,%f %f))'" % (x - rad, y + rad, x + rad, y + rad, x + rad, y - rad, x - rad, y - rad, x - rad, y + rad))
    cur.execute('select nodeID,ST_AsText(position),name,poitype from POIs where MBRContains(ST_GeomFromText(@poly),planaxy)')
    queryResult = cur.fetchall()
    ans = []
    for row in queryResult:
        coordinate = row['ST_AsText(position)'].strip().split(' ')
        lons = float(coordinate[0][6:])
        lats = float(coordinate[1][:-1])
        d = ut.vin_dist(lat, lon, lats, lons)
        if d <= rad_ori:
            ans.append((row['nodeID'], (lons, lats), row['name'], row['poitype'], d))
    return(sorted(ans, key=operator.itemgetter(4)))


def Query5ByLL(lat, lon):
    (y, x) = ut.mapping(lat, lon)
    rad_ori = 10
    rad = rad_ori*1.33
    queryResult = []
    flag = 1
    ans = []
    while True:
        cur.execute("set @poly='Polygon((%f %f,%f %f,%f %f,%f %f,%f %f))'" % (x - rad, y + rad, x + rad, y + rad, x + rad, y - rad, x - rad, y - rad, x - rad, y + rad))
        cur.execute('select nodeID,ST_AsText(position) from nonPOIs where MBRContains(ST_GeomFromText(@poly),planaxy)')
        queryResult = cur.fetchall()
        ans = []
        for row in queryResult:
            coordinate = row['ST_AsText(position)'].strip().split(' ')
            lons = float(coordinate[0][6:])
            lats = float(coordinate[1][:-1])
            d = ut.vin_dist(lat, lon, lats, lons)
            if d <= rad_ori:
                ans.append((row['nodeID'], (lons, lats), d))
        ls = (sorted(ans, key=operator.itemgetter(2)))
        for each in ls:
            cur.execute("select ways.wayid, ways.name, ways.isRoad, ways.otherinfo from waynode, ways where waynode.nodeid=%s and waynode.wayid=ways.wayid and ways.isroad <> '0'" % (each[0]))
            queryRes = cur.fetchall()
            if len(queryRes) > 0:
                ans = queryRes
                flag = 0
                break
        if flag == 0:
            break
        else:
            rad_ori = rad_ori * 2.7
            rad = rad_ori * 1.33
    return ans


def Query6By2LL(filename, lat1, lon1, lat2, lon2):
    mysql2xml.work(filename, lon1, lat1, lon2, lat2)


if __name__ == "__main__":
    (lat1, lon1) = (31.2629820000, 121.5345790000)
    (lat2, lon2) = (31.2626770000, 121.5353520000)
    rad = 50
    print('Q1:')
    print(Query1ByNodeID(28111460))
    print('Q2:')
    print(Query2ByWayID(4531289))
    print('Q3:')
    print(Query3ByNameOfRoad('p'))
    print('Q4:')
    print(Query4ByLLR(lat1, lon1, rad))
    print('Q5:')
    print(Query5ByLL(lat1, lon1))
    print('Q6:')
    Query6By2LL('../XML/text2.xml', lat1, lon1, lat2, lon2)
