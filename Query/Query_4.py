import pymysql.cursors
import operator
import utils as ut
import time
db = pymysql.connect(host="localhost", user="root", db="OSM4", charset='utf8')
cur = db.cursor()


def FindAllIntersection():
    cur.execute()


def Query1ByNodeID(nodeID):
    cur.execute('select wayID, name, isRoad from ways where wayID in (select wayID from waynode where nodeID=%s)' % nodeID)
    queryResult = cur.fetchall()
    isIntersection = 0
    if(len(queryResult) > 1):
        isIntersection = 1
    return isIntersection, queryResult


def Query2ByWayID(wayID):
    cur.execute('select * from nodes where nodeID in (select nodeID from waynode where wayID=%s)' % wayID)
    queryResult = cur.fetchall()
    return queryResult


def Query4ByLLR(lat, lon, rad):
    (y, x) = ut.mapping(lat, lon)
    cur.execute("set @poly='Polygon((%f %f,%f %f,%f %f,%f %f,%f %f))'" % (x - rad, y + rad, x + rad, y + rad, x + rad, y - rad, x - rad, y - rad, x - rad, y + rad))
    cur.execute('select nodeID,ST_AsText(position),name,poitype from POIs where MBRContains(ST_GeomFromText(@poly),planaxy)')
    queryResult = cur.fetchall()
    ans = []
    for row in queryResult:
        coordinate = row[1].strip().split(' ')
        lons = float(coordinate[0][6:])
        lats = float(coordinate[1][:-1])
        d = ut.calc_dist(lat, lon, lats, lons)
        if d <= rad:
            ans.append((row[0], (lons, lats), row[2], row[3], d))
    return(sorted(ans, key=operator.itemgetter(4)))


def Query5ByLL(lat, lon):
    (y, x) = ut.mapping(lat, lon)
    rad = 10
    queryResult = []
    flag = 1
    ans = []
    while True:
        cur.execute("set @poly='Polygon((%f %f,%f %f,%f %f,%f %f,%f %f))'" % (x - rad, y + rad, x + rad, y + rad, x + rad, y - rad, x - rad, y - rad, x - rad, y + rad))
        cur.execute('select nodeID,ST_AsText(position) from nonPOIs where MBRContains(ST_GeomFromText(@poly),planaxy)')
        queryResult = cur.fetchall()
        ans = []
        for row in queryResult:
            coordinate = row[1].strip().split(' ')
            lons = float(coordinate[0][6:])
            lats = float(coordinate[1][:-1])
            d = ut.calc_dist(lat, lon, lats, lons)
            if d <= rad:
                ans.append((row[0], (lons, lats), d))
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
            rad = rad * 2.7
    return ans


def Query6By2LL(lat1, lon1, lat2, lon2):
    cur.execute("set @poly='Polygon((%f %f,%f %f,%f %f,%f %f,%f %f))'" % (lon1, lat1, lon2, lat1, lon2, lat2, lon1, lat2, lon1, lat1))
    cur.execute('select nodeid, ST_AsText(position), otherinfo from nonPOIs where MBRContains(ST_GeomFromText(@poly),position)')
    queryResult_NPOI = cur.fetchall()
    cur.execute('select nodeid, ST_AsText(position), name, poitype, otherinfo from POIs where MBRContains(ST_GeomFromText(@poly),position)')
    queryResult_POI = cur.fetchall()
    queryResult_WN = []
    for each in queryResult_NPOI:
        cur.execute("select ways.wayid, ways.name, ways.otherinfo from waynode, ways where waynode.nodeid=%s and waynode.wayid=ways.wayid and ways.isroad <> '0'" % (each[0]))
        subres = list(cur.fetchall())
        queryResult_WN = queryResult_WN + subres
    return (queryResult_NPOI, queryResult_POI, queryResult_WN)

if __name__ == "__main__":
    (lat1, lon1) = (31.2629820000, 121.5345790000)
    (lat2, lon2) = (31.2626770000, 121.5353520000)
    rad = 50
    print ('Q1:')
    print (Query1ByNodeID(28111460))

    print ('Q2:')
    print (Query2ByWayID(4531289))
    print ('Q4:')
    print (Query4ByLLR(lat1,lon1,rad))
    print('Q5:')
    print(Query5ByLL(lat1, lon1))
    print('Q6:')
    print(Query6By2LL(lat1, lon1, lat2, lon2))
