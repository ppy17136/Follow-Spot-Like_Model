import os
import subprocess
import glob
from canshugai import modify_parameters
from ccccc import modify_write_data_file, extract_parameters
from tiqup import tiqup
from tiqun import tiqun
canshu="./canshu/canshu.txt"
data_car="Fe_exp46x1x80_12-1_-111_101"
data_data=f"data.{data_car}"
luo_alloy="luo_fe"
inluo=f"in.{luo_alloy}"
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
def main(AA0,BB0,ba0):
    for ba in ba0:
        for AA in AA0:
            for BB in BB0:
                    modify_parameters(AA, BB, ba)
                    extracted_params = extract_parameters(canshu)  
                    modify_write_data_file("./src/WriteDataFile.c", extracted_params)
                    os.chdir("./src")
                    subprocess.run(["make"], check=True)
                    os.chdir("..")
                    subprocess.run(["cp", "./src/msi2lmp.exe", "./"], check=True)
                    subprocess.run([
                        "./msi2lmp.exe", data_car, "-class", "I", "-frc", "./cvff"
                    ], stdout=open(f"data.{data_car}", "w"), stderr=subprocess.PIPE, check=True)
                    subprocess.run(["rm", "./msi2lmp.exe", "./src/WriteDataFile.o", "./src/msi2lmp.exe"], check=True)                    
                    log_file = f"{luo_alloy}_{AA}_48_{BB}_48_{ba}.log"
                    os.environ["OMP_NUM_THREADS"] = "1"
                    subprocess.run([
                        "mpirun", "--mca","coll_hcoll_enable", "0","-np", "8", "lmp_gpu", "-sf", "gpu", "-pk", "gpu", "1", "-in", f"{inluo}{ba}", "-log", log_file
                    ], check=True)
                    data_file = f"{data_car}_{AA}_48_{BB}_48_{ba}.data"
                    subprocess.run(["mv", f"{data_car}.data", data_file], check=True)
                    model_dir = f"./modelfe48_{ba}/"
                    ensure_directory_exists(model_dir)
                    subprocess.run(["mv", data_file, model_dir], check=True)
                    [cfg_files := glob.glob("*.cfg"), [os.rename(file, f"{AA}_48_{BB}_48_{ba}_" + file) for file in cfg_files]]
                    [atom_files := glob.glob("*.atom"), [os.rename(file, f"{AA}_48_{BB}_48_{ba}_" + file) for file in atom_files]]
                    atom_dir = f"./atomfilesfe48_{ba}/"
                    cfg_dir = f"./cfgfilesfe48_{ba}/"
                    log_dir = f"./logfilesfe48_{ba}/"
                    ensure_directory_exists(atom_dir)
                    ensure_directory_exists(cfg_dir)
                    ensure_directory_exists(log_dir)
                    subprocess.run(["mv"] + glob.glob('./*.atom') + [atom_dir], check=True)
                    subprocess.run(["mv"] + glob.glob('./*.cfg') + [cfg_dir], check=True)
                    subprocess.run(["mv"] + glob.glob('./*.log') + [log_dir], check=True)
        log_dir = f"./logfilesfe48_{ba}"
        tiqup(log_dir, AA0,BB0, ba)
        tiqun(log_dir, AA0,BB0, ba)
if __name__ == "__main__":
    AA0 = list(range(0,25+1))  
    BB0 = list(range(0,25+1))    
    ba0 = [0,0.5]
    main(AA0,BB0,ba0)    
    

    
