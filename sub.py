import re
class store:
    dic={}
class gen_all:
    poi=[]
class gen_start_end:
    poi=[]  
class gen_intersection:
    poi=[]
class gen_valid:
    poi=[]
class gen_multi_intersection:
    poi=[]
class gen_valid_poi:
    a={}
class ready_to_remove:
    poi=[]
class segment_output:
    seg=[]

def parse(line):
    
    streetna=re.findall(r"\s\"(.*)\"\s",line)  
    coord=re.findall(r"\(\-?[0-9]+\,\-?[0-9]+\)",line)
    
    check_streetna="".join(streetna)+"".join(coord)
    check_streetna=check_streetna.replace(" ","")
    for i in range (0,len(coord)):
       coord[i]=eval(coord[i])
    if line.replace(" ","").replace("\"","")[1:]!=check_streetna:
       print("Error:Unrecognize command.")
       return("","")
    if len(streetna)!=1:
       print("Error:Wrong street name.")
       return("","")
    else:
        streetna=streetna[0]
        
##    print(streetna)
    if not coord:
        print ("Error:No route.")
      
##    print(streetna,coord)    
    return (streetna,coord)

def parse_remove(line):
    streetna=re.findall(r"\s\"(.*)\"",line)  
    check_streetna="".join(streetna)
    check_streetna=check_streetna.replace(" ","")
    streetna=streetna[0]
    
    if line.replace(" ","").replace("\"","")[1:]!=check_streetna:
        print("Error:Unrecognize command.")
        return('')
    return(streetna)
    
def add(streetna,coord):
    if  streetna and coord:
        try:
          if streetna in store.dic:
             raise Exception ("Error:This street has already exist.")
          if len(coord)<=1:
             raise Exception ("Error:At least two point to build a street.")
    ##         print(streetna)
          store.dic[streetna]=coord
    ##      print store.dic
        except Exception as error:
             print(error)
      

def change(streetna,coord):
    if  streetna and coord:
        try:
            if streetna not in store.dic:
               raise Exception ("Error:This street doesn't exsit.")
            if len(coord)<=1:
               raise Exception ("Error:At least two point to build a street.")
            store.dic[streetna]=coord
        except Exception as error:
             print(error)

def remove(streetna):
    if streetna :
        try:
            if not streetna:
                raise Exception ("Error:No street records..")
            if streetna not in store.dic:
                raise Exception ("Error:"+"The street"+" "+ streetna +" "+"doesn't exsit.")
            else:
                del store.dic[streetna]
        except Exception as error:
             print(error)

def generate_graph():
    
    gen_intersection.poi=[]
    
    gen_all.poi=[]
    gen_start_end.poi=[]
    gen_multi_intersection.poi=[]
    ready_to_remove.poi=[]
    gen_valid_poi.a={}
    gen_valid.poi=[]
    segment_output.seg=[]
    count=0

    street=store.dic.values()
    for i in range (0,len(street)-1):
      for j in range (0,len(street[i])-1):
         for m in range (i+1,len(street)):
           for n in range (0,len(street[m])-1):
              l1=Line(street[i][j],street[i][j+1])
              l2=Line(street[m][n],street[m][n+1])
              intersect_point=intersect(l1,l2)     
  
    for k in range(0,len(gen_intersection.poi)):
        if gen_intersection.poi[k] not in gen_valid.poi:
           gen_valid.poi.append(gen_intersection.poi[k])
                                  
    for q in range(0,len(gen_start_end.poi)):
        if gen_start_end.poi[q] not in gen_valid.poi:
           gen_valid.poi.append(gen_start_end.poi[q])
    #print gen_valid.poi
    for t in range(0,len(gen_valid.poi)):
         gen_valid_poi.a[t+1]=gen_valid.poi[t]
        
   # print  gen_valid_poi.a                 
##    generate_output()
    

class Point(object):
    def __init__ (self, x, y):
        self.x = float(x)
        self.y = float(y)
    def __str__ (self):
        return '(' + str(self.x) + ',' + str(self.y) + ')'

class Line(object):
    def __init__ (self, src, dst):
        self.src = src
        self.dst = dst
    def __str__(self):
        return str(self.src) + '-->' + str(self.dst)

def intersect (l1, l2):
    
    
    x1, y1 = float(l1.src[0]), float(l1.src[1])
    x2, y2 = float(l1.dst[0]), float(l1.dst[1])
    x3, y3 = float(l2.src[0]), float(l2.src[1])
    x4, y4 = float(l2.dst[0]), float(l2.dst[1])

    xnum = float(((x1*y2-y1*x2)*(x3-x4) - (x1-x2)*(x3*y4-y3*x4)))
    xden = float(((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)))
   

    ynum = float((x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4-y3*x4))
    yden = float((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
 
    if xden*yden!=0:
       xcoor = float(xnum / xden)
       ycoor = float(ynum / yden)
       
       if (xcoor-x1)*(x2-xcoor)>=0 and (y1-ycoor)*(ycoor-y2)>=0 and (xcoor-x3)*(x4-xcoor)>=0 and (y3-ycoor)*(ycoor-y4)>=0:

           intersect_point=(xcoor,ycoor)

           if intersect_point not in gen_intersection.poi:
              if intersect_point:
                 gen_intersection.poi.append(intersect_point)  
                # print gen_intersection.poi
       
           gen_all.poi.append([(x1,y1),(x2,y2),intersect_point])
           gen_all.poi.append([(x3,y3),(x4,y4),intersect_point])

           gen_start_end.poi.append((x1,y1))
           gen_start_end.poi.append((x2,y2))
           gen_start_end.poi.append((x3,y3))
           gen_start_end.poi.append((x4,y4))


def delete_multi_intersction_segemnt():
    
    #check multi intersection
    for i in range (0,len(gen_all.poi)-1):
       
        for j in range (i+1,len(gen_all.poi)):
          
            #print(gen_all.poi[i][0],gen_all.poi[j][0],gen_all.poi[i][1],gen_all.poi[j][1])
            if gen_all.poi[i][0]==gen_all.poi[j][0] and gen_all.poi[i][1]==gen_all.poi[j][1]:
               
                if gen_all.poi[i][2]!=gen_all.poi[j][2] :
                    
                    if ([gen_all.poi[i][0],gen_all.poi[i][1],gen_all.poi[i][2],gen_all.poi[j][2]]) not in gen_multi_intersection.poi:
                       gen_multi_intersection.poi.append([gen_all.poi[i][0],gen_all.poi[i][1],gen_all.poi[i][2],gen_all.poi[j][2]])
##                       print gen_multi_intersection.poi
    if gen_multi_intersection.poi:
    #delete multi intersection segment
        for m in range (0,len(gen_all.poi)):
            if gen_all.poi[m][0] in gen_multi_intersection.poi[0] and gen_all.poi[m][1] in gen_multi_intersection.poi[0] and gen_all.poi[m][2] in gen_multi_intersection.poi[0]:
               
                ready_to_remove.poi.append(gen_all.poi[m])
        for n in range (0,len(ready_to_remove.poi)):
               gen_all.poi.remove(ready_to_remove.poi[n])
    #print  gen_all.poi



def single_intersction_output():
 
   for p in range (0,len(gen_all.poi)):
      point_start=gen_valid_poi.a.keys()[gen_valid_poi.a.values().index(gen_all.poi[p][0])]
      point_end=gen_valid_poi.a.keys()[gen_valid_poi.a.values().index(gen_all.poi[p][1])]
      point_intersection=gen_valid_poi.a.keys()[gen_valid_poi.a.values().index(gen_all.poi[p][2])]
      segment1="<"+ str(point_start)+","+ str(point_intersection) +">"
      segment2= "<"+ str(point_end)+","+ str(point_intersection) +">"
      if segment1 not in segment_output.seg:
         segment_output.seg.append(segment1)
      if segment2 not in segment_output.seg:
         segment_output.seg.append(segment2)
   #print segment_output.seg

      
def multi_intersction_output():
    
    if gen_multi_intersection.poi:
        
        for q in range(0,len(gen_multi_intersection.poi[0])-1):
          point_1=gen_valid_poi.a.keys()[gen_valid_poi.a.values().index(gen_multi_intersection.poi[0][q])]
          point_2=gen_valid_poi.a.keys()[gen_valid_poi.a.values().index(gen_multi_intersection.poi[0][q+1])]
          segment3="<"+ str(point_1)+","+ str(point_2) +">"
          if segment3 not in segment_output.seg:
              segment_output.seg.append(segment3)
   #print  segment_output.seg

def generate_output():
    
    print("V={ " )
    n=len(gen_valid.poi) 
    for i in range (0,n):
       print(" %d:%s"%(i+1,gen_valid.poi[i]))
    print("}")

    print("E={ " )
    for j in range (0,len(segment_output.seg)):
      if (j < len(segment_output.seg)-1):
          print " "+segment_output.seg[j]+","
      else:
          print " "+segment_output.seg[j]

    print("}")

##def gen_command():
##    generate_graph()
##    delete_multi_intersction_segemnt()
##    single_intersction_output()
##    multi_intersction_output()
##    generate_output()
##    
##if __name__ == '__main__':
##    add("a",((2,-1),(2,2),(5,5),(5,6),(3,8)))
##    add("b" ,((4,2),(4,8)))
##    add("c",((1,4),(5,8)))
##    gen_command()
