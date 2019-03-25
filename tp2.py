import sys
import os.path
import glob
import errno
import tokenizer

def main(argv):


    ##------------------------------------------------------------------------##
    if not os.path.isdir(argv[0]) :
       print(argv[0] ," No es un directorio " )
       sys.exit(2)

    if len(argv)==2 :
        if not os.path.isfile(argv[1]):
            print(argv[1], "No es un archivos")
            sys.exit(2)

    ##------------------------------------------------------------------------##
    ##                                Read dir
    ##------------------------------------------------------------------------##
    path = argv[0]+'/*.txt'
    files = glob.glob(path)
    for name in files:
        try:
            with open(name, encoding="UTF-8") as f:
                pass
                ##------open files------#
                filedata = f.read()
                lista_tokens=tokenizer.split(filedata," ")

                ##lista_palabras = filedata.split(" ")
                print(lista_tokens)


        except IOError as exc:
            if exc.errno != errno.EISDIR:
                raise


if __name__ == "__main__":
    main(sys.argv[1:])