import os
##############################
#   递归批量修改文件夹中的文件名
##############################
def change_name(path):
    for catagory in os.listdir(path):
        current_path = os.path.join(path,catagory)
        if os.path.isdir(current_path)==True:
            change_name(current_path)

            new_name=catagory.lower()
            os.rename(current_path, os.path.join(path,new_name))
        elif os.path.isfile(current_path)==True:
            new_name = catagory.lower().replace('_','')
            os.rename(current_path, os.path.join(path,new_name))


if __name__ == "__main__":
    change_name('~/sv/TIMIT_dataset/TIMIT/')