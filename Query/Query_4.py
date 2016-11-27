import pymysql.cursors
import utils as ut
db = pymysql.connect(host="localhost", user="root", db="OSM2", charset='utf8')
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


def Query4ByLLR(lat,lon,rad):
    (x,y) = ut.mapping(lat,lon)
    cur.execute("set @poly='Polygon((%f %f,%f %f,%f %f,%f %f,%f %f))'" %(x-rad,y+rad,x+rad,y+rad,x+rad,y-rad,x-rad,y-rad,x-rad,y+rad))
    cur.execute('select * from POIs where MBRContains(ST_GeomFromText(@poly),g)')
    queryResult = cur.fetchall()
    return queryResult


if __name__ == "__main__":
    print(Query1ByNodeID(28111460))
    print(Query2ByWayID(4531289))
