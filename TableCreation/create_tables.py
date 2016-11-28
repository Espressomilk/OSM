import pymysql.cursors

Ways_Create = """create table ways(
                    wayID varchar(12),
                    LineString linestring,
                    name varchar(100), index(name),
                    isRoad boolean,
                    otherInfo text,
                    primary key(wayID)
                ) ENGINE=MyISAM
              """

Nodes_Create = """create table nodes(
                    nodeID varchar(12),
                    version boolean,
                    primary key(nodeID)
                ) ENGINE=MyISAM
               """

POIs_Create = """create table POIs(
                    nodeID varchar(12),
                    position point not null, spatial index(position),
                    planaxy point not null, spatial index(planaxy),
                    name varchar(100), index(name),
                    poitype varchar(100), index(poitype),
                    otherInfo text,
                    primary key(nodeID)
                ) ENGINE=MyISAM
                """

NonPOIs_Create = """create table nonPOIs(
                    nodeID varchar(12),
                    position point not null, spatial index(position),
                    planaxy point not null, spatial index(planaxy),
                    otherInfo text,
                    primary key(nodeID)
                ) ENGINE=MyISAM
                """

WayNode_Create = """create table WayNode(
                        wayID varchar(12), index(wayID),
                        nodeID varchar(12), index(nodeID),
                        node_order int(2),
                        foreign key (nodeID) references nodes(nodeID),
                        foreign key (wayID) references ways(wayID)
                    ) ENGINE=MyISAM
                    """

db = pymysql.connect(host="localhost", user='root', db="OSM4")
cur = db.cursor()
try:
    cur.execute(Ways_Create)
except Exception as e:
    print("Exception", ":", e)
try:
    cur.execute(Nodes_Create)
except Exception as e:
    print("Exception", ":", e)
try:
    cur.execute(POIs_Create)
except Exception as e:
    print("Exception", ":", e)
try:
    cur.execute(NonPOIs_Create)
except Exception as e:
    print("Exception", ":", e)
try:
    cur.execute(WayNode_Create)
except Exception as e:
    print("Exception", ":", e)
db.commit()
