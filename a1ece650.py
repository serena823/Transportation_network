import sys
from sub import * 

def main():
     while True:
        try:
            line=sys.stdin.readline().strip();
            if line =="":
               break  
            if line =="\0":
               break    
            if line.startswith('a'):
               (streetna,coord)=parse(line)
               add(streetna,coord)
            elif line.startswith('c'):
               (streetna,coord)=parse(line)
               change(streetna,coord)
            elif line.startswith('r'):
               streetna=parse_remove(line)
               remove(streetna)
            elif line.startswith('g'):
               generate_graph()
               delete_multi_intersction_segemnt()
               single_intersction_output()
               multi_intersction_output()
               generate_output()
            else:
                raise Exception ("Error:invalid command")
        except Exception as error:
               print(error)
     sys.exit(0)



if __name__=='__main__':

    main()
