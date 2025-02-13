import os

def extract_parameters(file_path):
    params = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line_content = line.strip()
                if '=' in line_content and ';' in line_content:
                    key, value = line_content.split('=')[0].strip(), line_content.split('=')[1].split(';')[0].strip()
                    params[key] = value

    except FileNotFoundError:
        print("文件未找到: ", file_path)
    except IOError as e:
        print("文件操作错误: ", e)
    
    return params

def modify_write_data_file(file_path, params_to_update):
    try:
        with open(file_path, 'r+', encoding='utf-8') as file:
            lines = file.readlines()

            for i, line in enumerate(lines):
                line_content = line.strip()
                if '=' in line_content and ';' in line_content:
                    key, value = line_content.split('=')[0].strip(), line_content.split('=')[1].split(';')[0].strip()
                    if key in params_to_update:
                        new_value = params_to_update[key]
                        new_line = f"{key}={new_value};\n"
                        new_line = new_line.ljust(len(line))
                        lines[i] = new_line

            file.seek(0)
            file.writelines(lines)
            file.truncate()
            

    except FileNotFoundError:
        print("文件未找到: ", file_path)
    except IOError as e:
        print("文件操作错误: ", e)

if __name__ == "__main__":
    canshu_file = "./canshu/canshu.txt"
    write_data_file = "./src/WriteDataFile.c"
    print(f"从文件 {canshu_file} 提取参数...")
    extracted_params = extract_parameters(canshu_file)
    print(params)
    print(f"修改文件: {write_data_file}")
    modify_write_data_file(write_data_file, extracted_params)