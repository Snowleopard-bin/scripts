import os, random, shutil
from pathlib import Path

####################################
#   param
Files_each_dir = 3
Max_size = 440000
####################################

def check_filesize(files):
    for name in files:
        size = os.path.getsize(name)
        if size>Max_size:
            return False
    return True
##############################
#   复制文件
##############################
def copyfiles(files, tarDir):
    for name in files:
        subdir = os.path.dirname(str(name)[23:])
        target_dir = os.path.join(tarDir, subdir)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        shutil.copy(name, os.path.join(target_dir,str(name).split('/')[-1]))
##############################
#   从文件夹中随机选择N个文件
#   复制到指定文件夹
##############################
def select_files(fileDir, tarDir):
    if os.path.isdir(fileDir):
        total_files = []
        for wav_path in Path(fileDir).rglob('*.wav'):
            total_files.append(wav_path)
        
        start = end = 0
        speaker = ''
        for i in range(len(total_files)):    
            wav_path = str(total_files[i])
            current_speaker = wav_path.split('/')[3]
            if i ==0:
                speaker = current_speaker
                continue

            if (current_speaker != speaker and i!=0) or i==len(total_files)-1:
                end = i
                while True:
                    files = random.sample(total_files[start:end], Files_each_dir)
                    if check_filesize(files):
                        break
                copyfiles(files, tarDir)

                speaker = current_speaker
                start = i
##############################
#   统计文件的数量，文件大小
##############################
def show_wav(fileDir):
    if os.path.isdir(fileDir):
        num=0
        for wav_path in Path(fileDir).rglob('*.wav'):
            size = os.path.getsize(wav_path)
            print(f'file: {wav_path}, size: {size}')
            num+=1
        print(num)

if __name__ == '__main__':
    select_files(fileDir = 'data/voxceleb/vox1_wav', tarDir='data/voxceleb/samples1')
    show_wav(fileDir = 'data/voxceleb/samples1')