
from optparse import OptionParser
import sys

parser = OptionParser()
parser.add_option("-i","--infile",dest="infile", help="dispense file name")
options,args = parser.parse_args()
maxvol = 950
if options.infile is not None:
    print "Reading dispense list %s" % options.infile
    pass
else :
    parser.print_help()
    sys.exit()
startstop = {}

def matrixify(componentarray):
    matrixdict = {}
    for x in range(8):
        for y in range(12):
        #	print x , y , componentarray[(y) + (12 * x)]
            matrixdict[x,y] = float(componentarray[(y) + (12 * x)])
        return matrixdict


def check_not_done(mat, cname):
    print "Checking %s" % cname
    for x in range(8):
        for y in range(12):
            if mat[(x,y)] > 0:
                return True
            else:
                pass
    return False

def connectivity(mat,row,col,direction):
    scanparam = { 96 : (8,12) , 24 : (4 ,6) , 384 : ( 24 , 48)}
    scanindex = scanparam[len(mat.keys())]
    con = 0
    if direction == "alongrow":
        for i in range(col,12, 1):
            if int(mat[(row,i)]) > 0:
                con = con + 1
            else:
                return con
    elif direction == "alongcol":
        for i in range(row,8, 1):
            if mat[(i,col)] > 0:
                con = con + 1
            else:
                return con

    return con

def con_mat(mat):
    scanparam = { 96 : (8,12) , 24 : (4 ,6) , 384 : ( 24 , 48)}
    scanindex = scanparam[len(mat.keys())]
    deduce = {}
    for i in range(scanindex[0]):
        for j in range(scanindex[1]):
            c =  connectivity(mat,i,j,"alongcol")
            r =  connectivity(mat,i,j,"alongrow")
            deduce[(i,j)] = (r,c)
    return deduce
def containsColumnRow(paramInt1,paramInt2,startrow,startcol,stoprow,stopcol):
    return ((paramInt1 >= startcol) & (paramInt1 <= stopcol) & (paramInt2 >= startrow) & (paramInt2 <= stoprow))

def getbyte(paramInt1,paramInt2,startcol,stopcol,startrow,stoprow):
    arrayOfByte1 =[]
    i = 0
    strfirsttwo = "%02X%02X" % (paramInt1,paramInt2)
    arrayofbyte1 = strfirsttwo
    j = 0
    k = 0

    for l in range(0,paramInt1,1):
        # print "l", l
        for i1 in range(0,paramInt2,1):
            # print "j" , j
            i3 = 0
            if (containsColumnRow(l,i1,startrow,startcol,stoprow,stopcol)):
                i3 = 1 << j
                k = k|i3
            #	print "k,i3 j<6 ",k,i3
            j = j +1
            if (j > 6):
                i3 = 48 + k
                # print "k,i3 j>6 ", k,i3
                arrayofbyte1 = arrayofbyte1 + chr(i3)
                j = 0
                k = 0
    if ( j > 0):
        l = 48 + k
        arrayofbyte1 = arrayofbyte1 + chr(l)

    return arrayofbyte1


def pretty_print_mat(mat):
    li = []
    ri = []
    for k in mat.keys():
        li.append(k[0])
        ri.append(k[1])

    lmax = max(li) + 1
    rmax = max(ri) + 1
    for xi in range(lmax):
        for yj in range(rmax):
            print mat[(xi,yj)],
        print

mat = {}
f = open (options.infile , "r")
print f.readline()
deduce ={}
for line in f:
    component_name = line.split("\t")[0]
    mat = matrixify(line.split("\t")[3:])
    print "Printing raw matrix for component: %s" % (component_name), 
    pretty_print_mat(mat)
    passcounter = 0
    while check_not_done(mat,component_name):
        print component_name
        pretty_print_mat(con_mat(mat))
        for i in range(8):
            for j in range (12):
                c =  connectivity(mat,i,j,"alongcol")
                r =  connectivity(mat,i,j,"alongrow")
                deduce[i,j] = (r,c)
                if r == 0 and c == 0:
                    if mat[(i,j)] > 0:
                        print "Single dispense to %d %d" % (i,j)
                        print getbyte(12,8,i,i,j,j)
                    else:
                        continue
                elif r >= c  :
                    startx = i
                    starty = j
                    stopx = i
                    stopy = min(j + r,j+8)
                    vd = []
                    dispenses = []
                    for index in range(j,stopy ,1):
                            remainder = mat[(i,index)] - 950
                            dispenses.append((startx,index))
                            if remainder > 0:
                                vd.append(950)
                                mat[(i,index)] = remainder
                                print "Remainder %d" % remainder
                            else:
                                vd.append( mat[(i,index)])
                                mat[(i,index)] = 0
                    print "Volume Array:",vd
                    print "Dispense Volumes Horizontal from starx %d , starty %d to stopx %d , stop %d " % (startx,starty,stopx,stopy)
                    print getbyte(12,8,startx,stopx,starty,stopy)

                elif r < c :
                    startx = i
                    starty = j
                    stopx = i + c
                    stopy = j
                    vd = []
                    for index in range(i,i + c ,1):
                        remainder = mat[(index,j)] - 950
                        if remainder > 0:
                            vd.append(950)
                            mat[(index,j)] = remainder
                        else:
                            vd.append(mat[(index,j)])
                            mat[(index,j)] = 0
                    print "Volume Array:",vd
                    print "Dispense Volumes Vertical   from starx %d , starty %d to stopx %d , stop %d " % (startx,starty,stopx,stopy)
                    print getbyte(12,8,startx,stopx,starty,stopy)

                passcounter = passcounter + 1
                print "Matrix after pass:%d" % passcounter,
                pretty_print_mat(con_mat(mat))
                pretty_print_mat(mat)





