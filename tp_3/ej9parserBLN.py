import sys

def main(argv):
        with open("bln.txt", encoding="utf-8", errors="ignore") as f:
                data=f.readline()
                cont=1
                with open("queries.trec",encoding="utf-8", errors="ignore",mode="a") as q:
                        while data:
                                print(data)
                                print("Linea ",cont)

                                headers="<TOP> "
                                q.write(headers+"\n")
                                head_num="<NUM>"+str(cont)+"<NUM>"
                                q.write(head_num+"\n")
                                head_t="<TITLE>"
                                q.write(head_t+"\n")
                                q.write(data)
                                headers_top = "</TOP> "
                                q.write(headers_top+"\n")
                                q.write("\n")

                                cont+=1
                                data = f.readline()



if __name__ == "__main__":
        main(sys.argv[1:])