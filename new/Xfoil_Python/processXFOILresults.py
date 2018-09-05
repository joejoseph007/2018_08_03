# FILE: processXFOILresults.py
 
import string
import pylab as pl
import glob
 
from matplotlib import rc
 
# ------------------------------------------------------
"""
font.family        : serif
font.serif         : Times, Palatino, New Century Schoolbook, Bookman, Computer Modern Roman
font.sans-serif    : Helvetica, Avant Garde, Computer Modern Sans serif
font.cursive       : Zapf Chancery
font.monospace     : Courier, Computer Modern Typewriter
 
text.usetex        : true
"""
USETEX = True
if USETEX:
    rc('font',**{'family':'sans-serif',
                 'sans-serif':['Computer Modern Roman'],
                 'serif':'Computer Modern Roman',
                 'monospace':'Computer Modern Typewriter'})
    rc('text', usetex=True)
 
# ------------------------------------------------------
def line2floats(line):
    try:
        parts = string.split( line )
        floats = map( float, parts)
    except:
        parts = line[0:10], line[10:]
        floats = map( float, parts)
 
    return floats
 
def readTwoColumnFile(fname):
    fid = file(fname,'rt')
    lines = fid.readlines()
    lines = lines[1:] # remove header
 
    data = map(line2floats, lines)
    data = pl.array(data)
    fid.close()
 
    return data
 
def bisector(a,b):
    " assumes a and b are unit length"
    return (a+b)/pl.norm(a+b)
 
def postprocessCpData(data,geo,newxcount):
    x = data[:,0]
    y = geo[:,1]
    Cp = data[:,1]
 
    n = data.shape[0]
 
    # compute finite difference of x to classify points as upper and lower airfoil surface
    dx = pl.diff(x)
    dy = pl.diff(y)
    L = pl.sqrt(dx**2+dy**2)
    Tx = dx/L
    Ty = dy/L
    Nx = -Ty
    Ny = +Tx
    T = pl.array((Tx,Ty))
    T = T.transpose()
    N = pl.array((Nx,Ny))
    N = N.transpose()
 
    midx = (x[0:n-1]+x[1:n])/2.0
    midy = (y[0:n-1]+y[1:n])/2.0
    midcp = (Cp[0:n-1]+Cp[1:n])/2.0
 
    Tnode = pl.zeros( (n,2), pl.float64)
    Nnode = pl.zeros( (n,2), pl.float64)
    for i in range(1,n-1):
        Tnode[i,:] = bisector( T[i-1,:], T[i,:] )
        Nnode[i,:] = bisector( N[i-1,:], N[i,:] )
    Tnode[0,:] = bisector( T[0,:], T[-1,:] )
    Tnode[-1,:] = bisector( T[0,:], T[-1,:] )
    Nnode[0,:] = bisector( N[i-1,:], N[i,:] )
    Nnode[-1,:] = bisector( N[i-1,:], N[i,:] )
 
    # determine (safe) limits of x for interpolation
    xmin = min( min(x[dx<0]),min(x[dx>=0]) )
    xmax = max( max(x[dx<0]),max(x[dx>=0]) )
 
    # re-compute lower and upper Cp at new abscissae
    if ChebyshevSpacing:
        xnew = pl.linspace(pl.pi, 0, newxcount)
        xnew = (pl.cos(xnew)+1)/2.0
    else:
        xnew = pl.linspace(xmin, xmax, newxcount)
 
    newCpUpper = pl.interp(xnew, pl.flipud(x[dx<0]), pl.flipud(Cp[dx<0]))     newCpLower = pl.interp(xnew, x[dx>=0], Cp[dx>=0])
 
    return (x,y,Cp,L,T,N,midx,midy,midcp,Tnode,Nnode,xnew,newCpUpper,newCpLower)
 
# ------------------------------------------------------
 
datadir = './plots2'
 
CpFiles = glob.glob(datadir+'/dat/cpprof*.dat')
geofile = datadir+'/dat/e387coords.dat'
 
geodata = readTwoColumnFile(geofile)
 
count = 0
maxcount = 5
ChebyshevSpacing = True
 
postprocessResult = file('post.dat','wt')
postprocessResult.write( "%12s %12s %12s %12s %12s %12s\n" % ("AoA","FX","FY","MY","FD","FL") )
 
ForceMoment = []
 
for CpFile in CpFiles:
    alpha = -10+0.2*count
    print "reading Cp file" , CpFile
    data = readTwoColumnFile(CpFile)
 
    x, y, Cp, L, T, N, midx, midy, midcp, Tnode, Nnode, xnew, newCpUpper, newCpLower = postprocessCpData(data, geodata, 100)
 
    # panel Cp x and y components
    midcpx = midcp*N[:,0]
    midcpy = midcp*N[:,1]
 
    dx = pl.diff(x)
    dy = pl.diff(y)
 
    forceX = pl.trapz(midcpx*L)
    forceY = pl.trapz(midcpy*L)
    momentY = pl.trapz((midx-0.25)*midcpy*L)
    AoA = alpha*pl.pi/180.
    forceD = +forceX*pl.cos(AoA)+forceY*pl.sin(AoA)
    forceL = -forceX*pl.sin(AoA)+forceY*pl.cos(AoA)
    postprocessResult.write( "%12.6f %12.6f %12.6f %12.6f %12.6f %12.6f\n" % (AoA,forceX,forceY,momentY,forceD, forceL) )
 
    ForceMoment.append( [AoA,forceX,forceY,momentY,forceD,forceL])
 
    # plot upper and lower profile parts in different colors
    pl.figure()
    pl.plot( x[dx<0] ,data[dx<0] ,'r.-',lw=2)     pl.plot( x[dx>=0],data[dx>=0],'b.-',lw=2)
    pl.legend(['upper $C_p$','lower $C_p$'])
    pl.title(r'$C_p @ \alpha -10$')
 
    # plot upper and lower Cp in different color
    pl.figure()
    pl.plot( xnew,newCpUpper,'r.-',lw=2)
    pl.plot( xnew,newCpLower,'b.-',lw=2)
    pl.legend(['upper $C_p$','lower $C_p$'])
    pl.title(r'$C_p (\alpha=%6.3f)$' % (alpha,))
 
    # plot Cp difference between upper and lower profiles
    pl.figure()
    pl.plot( xnew,newCpUpper-newCpLower,'r.-',lw=2)
    pl.title(r'$\Delta C_p (\alpha=%6.3f)$' % (alpha,))
    pl.ylim([-5,14])
 
    pl.savefig(datadir+'/fig%02d.pdf' % (count,))
 
    count += 1
    if count>maxcount:
        break
 
postprocessResult.close()
 
ForceMoment = pl.array(ForceMoment)
 
pl.figure()
pl.plot( ForceMoment[:,0], ForceMoment[:,1], 'd-', ForceMoment[:,0], ForceMoment[:,2], 'o-', mec=None)
pl.xlabel('$x$')
pl.ylabel('$F$')
pl.legend( ('$F_x$','$F_y$') )
pl.grid()
pl.savefig('forceXY.pdf')
 
pl.figure()
pl.plot( ForceMoment[:,0], ForceMoment[:,4], 'd-', ForceMoment[:,0], ForceMoment[:,5], 'o-', mec=None)
pl.xlabel('$x$')
pl.ylabel('$F$')
pl.legend( ('$F_D$','$F_L$') )
pl.grid()
pl.savefig('forceDL.pdf')
 
pl.figure()
pl.plot( ForceMoment[:,0], ForceMoment[:,3], 'd-', mec=None)
pl.xlabel('$x$')
pl.ylabel('$M_y$')
pl.grid()
pl.savefig('momentY.pdf')
