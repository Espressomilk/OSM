def mapping(x,y):
    from math import pi,log,tan
    L = 6381372 * pi * 2
    W = L;
    H = L/2;
    mill = 2.3
    a = x * pi / 180
    b = y * pi / 180
    a = 1.25 * log(abs(tan(0.25*pi+0.4*a)))
    b = (W/2) + (W/(2*pi))*b
    a = (H/2) - (H/(2*mill))*a
    return (a,b)

def calc_dist(x1,y1,x2,y2):
        from math import atan,tan,sin,cos,pi,sqrt,atan2,asin
        (a1,b1)=mapping(x1,y1)
        (a2,b2)=mapping(x2,y2)
        return sqrt((a1-a2)**2+(b1-b2)**2)

def vin_dist(x1,y1,x2,y2):
        from math import atan,tan,sin,cos,pi,sqrt,atan2,asin
        a = 6378137
        b = 6356752.3142
        f = 1/298.257223563
        L = (y2-y1)*pi/180
        U1 = atan((1-f)*tan(x1*pi/180))
        U2 = atan((1-f)*tan(x2*pi/180))
        sinU1 = sin(U1)
        cosU1 = cos(U1)
        sinU2 = sin(U2)
        cosU2 = cos(U2)
        lamb = L
        lambP = 2*pi
        itemlim = 20
        while abs(lamb-lambP)>1e-12 and itemlim>0:
            sinlamb = sin(lamb)
            coslamb = cos(lamb)
            sinSigma = sqrt((cosU2*sinlamb)*(cosU2*sinlamb)+
                            (cosU1*sinU2-sinU1*cosU2*coslamb)*(cosU1*sinU2-sinU1*cosU2*coslamb))
            if sinSigma == 0:
                print ('co-incident')
            cosSigma = sinU1*sinU2 + cosU1*cosU2*coslamb
            sigm = atan2(sinSigma,cosSigma)
            alpha = asin(cosU1*cosU2*sinlamb/sinSigma)
            cosSqAlpha = cos(alpha)*cos(alpha)
            cos2SigmaM = cosSigma-2*sinU1*sinU2/cosSqAlpha
            c = f/16*cosSqAlpha*(4+f*(4-3*cosSqAlpha))
            lambP = lamb
            lamb = L + (1-c)*f*sin(alpha)*(sigm+c*sinSigma*(cos2SigmaM+c*cosSigma*(-1+2*cos2SigmaM*cos2SigmaM)))
            itemlim = itemlim - 1
        if itemlim == 0:
            print ('diverge')
        uSq = cosSqAlpha *(a*a-b*b)/(b*b)
        A = 1 + uSq/16384*(4096+uSq*(-768+uSq*(320-175*uSq)))
        B = uSq/1024 * (256+uSq*(-128+uSq*(74-47*uSq)))
        deltaSigma = B*sinSigma*(cos2SigmaM+B/4*(cosSigma*(-1+2*cos2SigmaM*cos2SigmaM)-
                B/6*cos2SigmaM*(-3+4*sinSigma*sinSigma)*(-3+4*cos2SigmaM*cos2SigmaM)))
        s = b*A*(sigm-deltaSigma)
        d = s
        return d
