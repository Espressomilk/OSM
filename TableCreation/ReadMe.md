# table

Nodes (  nodeID varchar(12),
         version boolean,
         primary key(nodeID)
) ENGINE=MyISAM

POIs(    nodeID varchar(12),
         position point not null, spatial index(position),
         name varchar(100), index(name),
         poitype varchar(100), index(poitype),
         otherInfo text,
         primary key(nodeID)
) ENGINE=MyISAM

NonPOIs( nodeID varchar(12),
         position point not null, spatial index(position),
         otherInfo text,
         primary key(nodeID)
) ENGINE=MyISAM

Ways (   wayID varchar(12),
         LineString linestring,
         name varchar(100), index(name),
         isRoad boolean,
         otherInfo text,
         primary key(wayID)
) ENGINE=MyISAM

WayNode( wayID varchar(12), index(wayID),
         nodeID varchar(12), index(nodeID),
         node_order int(2),
         foreign key (nodeID) references nodes(nodeID),
         foreign key (wayID) references ways(wayID)
) ENGINE=MyISAM
