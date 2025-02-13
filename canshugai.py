import os
import sys
def modify_parameters(aa, bb, ba):
    linebuffer = ""  
    buffer1 = ""    
    buffer2 = ""    
    buffer3 = ""    
    xshift1 = aa  
    zshift1 = bb  
    ba1 = ba
    try:
        with open("./canshu/canshu.txt", "r+") as fp:
            lines = fp.readlines()  
            for i, line in enumerate(lines):
                linebuffer = line.strip()
                parts = linebuffer.split("=")
                if len(parts) > 1:
                    buffer1, buffer2 = parts[0], parts[1].split(";")[0]

                    if buffer1.strip() == "xshift":
                        lines[i] = f"xshift={xshift1};\n".ljust(len(line))  
                        break
            for i, line in enumerate(lines):
                linebuffer = line.strip()
                parts = linebuffer.split("=")
                if len(parts) > 1:
                    buffer1, buffer2 = parts[0], parts[1].split(";")[0]

                    if buffer1.strip() == "zshift":
                        lines[i] = f"zshift={zshift1};\n".ljust(len(line))  
                        break
            for i, line in enumerate(lines):
                linebuffer = line.strip()
                parts = linebuffer.split("=")
                if len(parts) > 1:
                    buffer1, buffer2 = parts[0], parts[1].split(";")[0]

                    if buffer1.strip() == "ba":
                        lines[i] = f"ba={ba1};\n".ljust(len(line)) 
                        break            
            fp.seek(0)
            fp.writelines(lines)
            fp.truncate()
    except FileNotFoundError:
        print("Error: File not found")
        return -1
    except IOError as e:
        print(f"I/O error: {e}")
        return -1
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("用法: python canshugai.py <AA> <BB>")
        sys.exit(1)

    AA = sys.argv[1]
    BB = sys.argv[2]
    ba = sys.argv[3]
    modify_parameters(AA, BB, ba)