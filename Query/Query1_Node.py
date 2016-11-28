#-*-coding:utf8-*-
import pymysql.cursors

db = pymysql.connect(host="localhost", user="root", db="OSM2", charset='utf8')
cur = db.cursor(pymysql.cursors.DictCursor)


def FindAllIntersection():
    cur.execute()


def Query1ByNodeID(nodeID):
    cur.execute('select * from ways where wayID in (select wayID from waynode where nodeID=%s)' % nodeID)
    queryResult = cur.fetchall()
    isIntersection = 0
    if(len(queryResult) > 1):
        isIntersection = 1
    return isIntersection, queryResult


def Query2ByWayID(wayID):
    # cur.execute('select nodeID from waynode where wayID=%s' % wayID)
    # tmpQueryResult = cur.fetchall()
    # print(tmpQueryResult)
    # cur.execute('select * from nodes where version = 1 and nodeID in (select nodeID from waynode where wayID=%s)' % wayID)
    # poiQueryResult = cur.fetchall()
    # cur.execute('select * from nodes where version <> 1 and nodeID in (select nodeID from waynode where wayID=%s)' % wayID)
    # nonpoiQueryResult = cur.fetchall()
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


def Query6ByRectangular(x1, y1, x2, y2):
    poly = 'Polygon((%s %s, %s %s, %s %s, %s %s, %s %s))' % (x1, y1, x1, y2, x2, y2, x2, y1, x1, y1)
    cur.execute("select count(*) from pois where MBRContains(GeomFromText('%s'), position)" % poly)
    poiresult = cur.fetchall()
    cur.execute("select count(*) from nonpois where MBRContains(GeomFromText('%s'), position)")
    nonpoiresult = cur.fetchall()
    print(result)


if __name__ == "__main__":
    # print(Query1ByNodeID(28111460))
    # print(Query2ByWayID(4531289))
    # Query3ByNameOfRoad('东川')
    Query6ByRectangular(121.3, 31.2, 121.5, 31.4)
