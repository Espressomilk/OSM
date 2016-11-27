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
        import mapping as mp
        from math import atan,tan,sin,cos,pi,sqrt,atan2,asin
        (a1,b1)=mp.mapping(x1,y1)
        (a2,b2)=mp.mapping(x2,y2)
        return sqrt((a1-a2)**2+(b1-b2)**2)

