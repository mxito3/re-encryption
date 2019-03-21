import numpy as np
circleLeastTime= 100 #写数据的最小次数
circleHignTime = 1000 #写数据的最大次数
need_create_file = 10 # 需要创建的样本的数量
per_data = "hello,I am yapie,someone loves laughing\n"
def writePerFile(write_time,fileName):
    file=open(fileName, 'w') # open for 'w'riting 
    for index in range(write_time):
        file.write(per_data)
    file.close() # close the file

def writeData():
    for index in range(need_create_file):
        fileName = 'patient'+str(index)
        needWriteTime = np.random.randint(circleLeastTime,circleHignTime)
        writePerFile(needWriteTime,fileName)

if __name__ == "__main__":
    writeData()