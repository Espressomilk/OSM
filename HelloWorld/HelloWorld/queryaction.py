# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.template.context_processors import csrf
from Query import Query1ByNodeID, Query2ByWayID, Query3ByNameOfRoad, Query4ByLLR, Query5ByLL, Query6By2LL
from wsgiref.util import FileWrapper
import mimetypes
from django.http import HttpResponse
import re
import json

# 接收Post请求数据
def queryaction(request):
    ctx = {}
    ctx.update(csrf(request))
    if request.POST:
        ctx['class233'] = "mainpart"
        queryNo = request.POST['queryno']
        ctx['querydetail'] = queryNo + ": " + request.POST['q']
        if queryNo == "Query1":
            nodeID = request.POST['q']
            isIntersection, queryResult = Query1ByNodeID(nodeID)
            if len(queryResult) == 0:
                ctx['resultflag'] = 0
            else:
                ctx['resultflag'] = 1
                ctx['itsct'] = isIntersection
                ctx['rlt'] = queryResult
        elif queryNo == "Query2":
            wayID = request.POST['q']
            ans = Query2ByWayID(wayID)
            if len(ans) == 0:
                ctx['resultflag'] = 0
            else:
                ctx['resultflag'] = 2
                ctx['rlt'] = ans
                xy = re.split('\(|\)', ans[0][0]["position"])[1].split()
                ctx['coord_x'] = json.dumps(xy[1])
                ctx['coord_y'] = json.dumps(xy[0])
        elif queryNo == "Query3":
            name = request.POST['q']
            result = Query3ByNameOfRoad(name)
            if len(result) == 0:
                ctx['resultflag'] = 0
            else:
                ctx['resultflag'] = 3
                ctx['rlt'] = result
        elif queryNo == "Query4":
            llr = request.POST['q']
            try:
                [lat, lon, rad] = llr.split("/") ## exceptions
            except:
                ctx['resultflag'] = 8
                return render(request, "espressomilk.html", ctx)
            ctx['querydetail'] = "Query4: coordinates(" + lat + ", " + lon + ") & radis: " + rad
            roadlist = Query4ByLLR(float(lat), float(lon), float(rad))
            if len(roadlist) == 0:
                ctx['resultflag'] = 0
            else:
                ctx['resultflag'] = 4
                ctx['rlt'] = roadlist
                ctx['poi_x'] = json.dumps(float(lat))
                ctx['poi_y'] = json.dumps(float(lon))
                ctx['radius'] = json.dumps(float(rad))
                ctx['coord'] = json.dumps(roadlist)
        elif queryNo == "Query5":
            ll = request.POST['q']
            try:
                [lat, lon] = ll.split("/")
            except:
                ctx['resultflag'] = 8
                return render(request, "espressomilk.html", ctx)
            ctx['querydetail'] = "Query5: coordinates(" + lat + ", " + lon + ")"
            road = Query5ByLL(float(lat), float(lon))
            if len(road) == 0:
                ctx['resultflag'] = 0
            else:
                ctx['resultflag'] = 5
                ctx['rlt'] = road
        elif queryNo == "Query6":
            llll = request.POST['q']
            try:
                [lat1, lon1, lat2, lon2] = llll.split("/")
            except:
                ctx['resultflag'] = 8
                return render(request, "espressomilk.html", ctx)
            filename = "OnlyOneFile.xml"
            Query6By2LL(filename, float(lat1), float(lon1), float(lat2), float(lon2))
            ctx['resultflag'] = 6
            ctx['rlt'] = "Please get the file as your will"
        else:
            ctx['resultflag'] = 9
    return render(request, "espressomilk.html", ctx)

def file_download(request):
    filepath = "../XML/OnlyOneFile.xml"
    wrapper = FileWrapper(open(filepath, 'rb'))
    content_type = mimetypes.guess_type(filepath)[0]
    response = HttpResponse(wrapper, content_type='application/json')
    response['Content-Disposition'] = "attachment; filename=%s" % "OnlyOneFile.xml"
    return response
