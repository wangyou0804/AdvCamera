import os


def readname(filePath):
    name = os.listdir(filePath)
    return name
 
 
if __name__ == "__main__":
    prefix = 'F:\\dachuang\\animals\\testfile\\'
    name = readname('F:\\dachuang\\animals\\testfile')
   
    
    for i in name:
        os.system('python ' + 'F:\\dachuang\\animals\\example9\\imagenet_tools_mxnet.py ' + prefix + i)
        os.system('python ' + 'F:\\dachuang\\animals\\example9\\imagenet_tutorial_fgsm_mxnet.py ' + prefix + i + ' ' + i)
        break
    
    