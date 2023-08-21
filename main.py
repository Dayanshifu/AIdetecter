#           智能图像识别器
#######################################
# 需要的第三方库(使用pip安装，python3.10版本):
# Pillow==9.2.0
# windnd==1.0.7
# opencv-python==4.6.0.66(含numpy==1.23.2)
# requests==2.28.1
# 请在windows系统下编译运行此程序
# 请将压缩包内的images文件夹与源程序放在同一文件夹下
# 建议使用100%dpi的显示器体验本程序
#######################################

from tkinter import *
from tkinter import filedialog, scrolledtext
from tkinter import font
from PIL import Image, ImageTk, ImageGrab
import os, json, base64, requests, cv2, windnd
import easygui

FILEPATH = os.path.dirname(__file__)

main = Tk()
main.title('智能图像识别器')
main.iconbitmap(FILEPATH+'\\images\\desktop.ico')
main.minsize(1157, 568)

imagePath = FILEPATH+'\\images\\bg.png'
image = ImageTk.PhotoImage(Image.open(imagePath))

class ai():
    def face(b64):
        url = 'api/getaiface'
        postData = {"data":{"auth":{"id":"id","secret":"secret","client":"client"},"image":b64,"field":"age,beauty,gender,face_shape,expression,glasses,face_type,mask,emotion"}}
        headers = {'Content-type':'application/json', 'Accept':'*/*'}
        postData = json.dumps(postData)
        try:
            Res = requests.post(url, postData, headers=headers)
        except:
            return '获取异常, 请检查网络'
        try:
            Res = json.loads(Res.text)
        except:
            return '100 错误'
        if int(Res['status']['success'])==1:
            text = '人脸识别结果:\n\n'
            for i in Res['data']['facelist']:
                text += '年龄:' + str(i['age'])+'\n'
                text += '颜值:' + str(i['beauty'])+'\n'
                text += '性别:' + i['gender']['type']+'\n'
                text += '脸型:' + i['face_shape']['type']+'\n'
                text += '表情:' + i['expression']['type']+'\n'
                text += '眼镜:' + i['glasses']['type']+'\n'
                text += '人脸类型:' + i['face_type']['type']+'\n'
                text += '口罩:' + str(i['mask']['type'])+'\n'
                text += '情绪:' + i['emotion']['type']+'\n\n'
            return text
        else:
            return str(Res['status']['error_code']) +' '+Res['status']['msg']
    
    def body(b64):
        url = 'api/getaibodyanalysis'
        postData = {"data":{"auth":{"id":"id","secret":"secret","client":"client"},"image":b64}}
        headers = {'Content-type':'application/json', 'Accept':'*/*'}
        postData = json.dumps(postData)
        try:
            Res = requests.post(url, postData, headers=headers)
        except:
            return '获取异常, 请检查网络'
        try:
            Res = json.loads(Res.text)
        except:
            return '100 错误'
        if int(Res['status']['success'])==1:
            text = '手势识别结果:\n\n'
            for i in Res['data']['gesturelist']:
                text += '名称:' + i['classname']+'\n'
                text += '置信度:' + str(i['probability'])+'\n\n'
            return text
        else:
            return str(Res['status']['error_code']) +' '+Res['status']['msg']
    
    def ocr(b64):
        url = 'api/getaiocr'
        postData = {"data":{"auth":{"id":"id","secret":"secret","client":"client"},"image":b64}}
        headers = {'Content-type':'application/json', 'Accept':'*/*'}
        postData = json.dumps(postData)
        try:
            Res = requests.post(url, postData, headers=headers)
        except:
            return '获取异常, 请检查网络'
        try:
            Res = json.loads(Res.text)
        except:
            return '100 错误'
        if int(Res['status']['success'])==1:
            text = ''
            for i in Res['data']['wordslist']:
                text += i['words']+'\n'
            return text
        else:
            return str(Res['status']['error_code']) +' '+Res['status']['msg']
    
    def ai(b64):
        url = 'api/getaidetect'
        postData = {"data":{"auth":{"id":"id","secret":"secret","client":"client"},"image":b64}}
        headers = {'Content-type':'application/json', 'Accept':'*/*'}
        postData = json.dumps(postData)
        try:
            Res = requests.post(url, postData, headers=headers)
        except:
            return '获取异常, 请检查网络'
        try:
            Res = json.loads(Res.text)
        except:
            return '100 错误'
        if int(Res['status']['success'])==1:
            text = '智能识别结果:\n\n'
            for i in Res['data']['classifylist']:
                if float(i['score']) >= 0.7:
                    text+='最有可能!\n'
                if float(i['score']) <= 0.25:
                    continue
                text += '名称:' + i['keyword']+'\n'
                text += '相似度:' + str(i['score'])+'\n'
                text += '分类:' + i['root']+'\n\n'
            return text
        else:
            return str(Res['status']['error_code']) +' '+Res['status']['msg']
    
    def plant(b64):
        url = 'api/getaiplantdetect'
        postData = {"data":{"auth":{"id":"id","secret":"secret","client":"client"},"image":b64,"baikenum":"5"}}
        headers = {'Content-type':'application/json', 'Accept':'*/*'}
        postData = json.dumps(postData)
        try:
            Res = requests.post(url, postData, headers=headers)
        except:
            return '获取异常, 请检查网络'
        try:
            Res = json.loads(Res.text)
        except:
            return '100 错误'
        if int(Res['status']['success'])==1:
            text = '植物识别结果:\n\n'
            for i in Res['data']['plantlist']:
                if float(i['score']) >= 0.7:
                    text+='最有可能!\n'
                if float(i['score']) <= 0.25:
                    continue
                text += '名称:' + i['name']+'\n'
                text += '相似度:' + str(i['score'])+'\n'
                try:
                    text += '百科信息:\n' + i['baike_info']['description']+'\n'
                except:pass
                text += '\n'

            return text
        else:
            return str(Res['status']['error_code']) +' '+Res['status']['msg']
    
    def animal(b64):
        url = 'api/getaianimaldetect'
        postData = {"data":{"auth":{"id":"id","secret":"secret","client":"client"},"image":b64,"baikenum":"5"}}
        headers = {'Content-type':'application/json', 'Accept':'*/*'}
        postData = json.dumps(postData)
        try:
            Res = requests.post(url, postData, headers=headers)
        except:
            return '获取异常, 请检查网络'
        try:
            Res = json.loads(Res.text)
        except:
            return '100 错误'
        if int(Res['status']['success'])==1:
            text = '动物识别结果:\n\n'
            for i in Res['data']['animallist']:
                if float(i['score']) >= 0.7:
                    text+='最有可能!\n'
                if float(i['score']) <= 0.25:
                    continue
                text += '名称:' + i['name']+'\n'
                text += '相似度:' + str(i['score'])+'\n'
                try:
                    text += '百科信息:\n' + i['baike_info']['description']+'\n'
                except:pass
                text += '\n'
                
            return text
        else:
            return str(Res['status']['error_code']) +' '+Res['status']['msg']
    
    def dish(b64):
        url = 'api/getaidishdetect'
        postData = {"data":{"auth":{"id":"id","secret":"secret","client":"client"},"image":b64,"baikenum":"5"}}
        headers = {'Content-type':'application/json', 'Accept':'*/*'}
        postData = json.dumps(postData)
        try:
            Res = requests.post(url, postData, headers=headers)
        except:
            return '获取异常, 请检查网络'
        try:
            Res = json.loads(Res.text)
        except:
            return '100 错误'
        if int(Res['status']['success'])==1:
            text = '菜肴识别结果:\n\n'
            for i in Res['data']['dishlist']:
                if float(i['probability']) >= 0.7:
                    text+='最有可能!\n'
                if float(i['probability']) <= 0.25:
                    continue
                text += '名称:' + i['name']+'\n'
                text += '置信度:' + str(i['probability'])+'\n'
                try:
                    text += '卡路里:' + str(i['calorie'])+'\n'
                except:pass
                try:
                    text += '百科信息:\n' + i['baike_info']['description']+'\n'
                except:pass
                text += '\n'
                
            return text
        else:
            return str(Res['status']['error_code']) +' '+Res['status']['msg']
    
    def car(b64):
        url = 'api/getaicardetect'
        postData = {"data":{"auth":{"id":"id","secret":"secret","client":"client"},"image":b64,"baikenum":"5","num":"5"}}
        headers = {'Content-type':'application/json', 'Accept':'*/*'}
        postData = json.dumps(postData)
        try:
            Res = requests.post(url, postData, headers=headers)
        except:
            return '获取异常, 请检查网络'
        try:
            Res = json.loads(Res.text)
        except:
            return '100 错误'
        if int(Res['status']['success'])==1:
            text = '车辆识别结果:\n\n'
            for i in Res['data']['carlist']:
                if float(i['score']) >= 0.6:
                    text+='最有可能!\n'
                if float(i['score']) <= 0.2:
                    continue
                text += '名称:' + i['name']+'\n'
                text += '相似度:' + str(i['score'])+'\n'
                text += '颜色:'+Res['data']['color']+'\n'
                text += '年份:' + i['year']+'\n'
                try:
                    text += '百科信息:\n' + i['baike_info']['description']+'\n'
                except:pass
                text += '\n'
                
            return text
        else:
            return str(Res['status']['error_code']) +' '+Res['status']['msg']
    
    def qr(b64):
        url = 'api/getqrcodecontent'
        postData = {"data":{"auth":{"id":"id","secret":"secret","client":"client"},"image":b64}}
        headers = {'Content-type':'application/json', 'Accept':'*/*'}
        postData = json.dumps(postData)
        try:
            Res = requests.post(url, postData, headers=headers)
        except:
            return '获取异常, 请检查网络'
        try:
            Res = json.loads(Res.text)
        except:
            return '100 错误'
        if int(Res['status']['success'])==1:
            text = '二维码识别结果:\n\n'
            text += '类型:' + Res['data']['qrtype']+'\n'
            text += '内容:' + Res['data']['qrcontent']+'\n\n'
            return text
        else:
            return str(Res['status']['error_code']) +' '+Res['status']['msg']
        

def f2b64(path):
    f = open(path, 'rb')
    b64 = base64.b64encode(f.read())
    f.close()
    return str(b64, encoding='utf-8')

def getcam():
    choicebox= Tk()
    choicebox.title('选择摄像头')
    choicebox.iconbitmap(FILEPATH+'\images\cam.ico')
    choicebox.geometry('360*130')
    choicebox.resizable(0,0)

    Label(choicebox, text='选择一个摄像头')


def camera(video):
    cam = cv2.VideoCapture(video, cv2.CAP_DSHOW)
    while 1 :
        a, img=cam.read()
        img = cv2.flip(img, 1)
        cv2.imshow('Camera', img)
        key = cv2.waitKey(10)
        if key == ord(' '):
            path = FILEPATH+'\\images\\test.png'
            img = cv2.flip(img, 1)
            cv2.imwrite(path, img)
            break
        elif key == ord('\x1b'):
            path=''
            break
    cam.release()
    cv2.destroyAllWindows()
    return path
            
def setImg(path):
    global imagePath, image
    re=imagePath
    imagePath = path
    try:
        image = ImageTk.PhotoImage(Image.open(imagePath))
    except:
        imagePath = re
        image = ImageTk.PhotoImage(Image.open(imagePath))
    main.title('智能图像识别器  -'+os.path.basename(imagePath))
    imageCanvas.config(scrollregion=(0,0,image.width(),image.height()))
    imageCanvas.create_image(0,0,anchor=NW,image=image)
    return 0

def grabscreen():
    scr = Tk()
    scr.title('截图工具')
    scr.geometry('800x418')
    scr.iconbitmap(FILEPATH+'\\images\\scr.ico')
    scr.attributes('-alpha', 0.7)
    scr.wm_attributes('-topmost', 1)

    path = FILEPATH+'\\images\\test.png'

    def clip():
        scr.destroy()
        img = ImageGrab.grabclipboard()
        img.save(path)
        setImg(path)
        return 0

    def screen(bbox=None):
        scr.destroy()
        img = ImageGrab.grab(bbox=bbox)
        img.save(path)
        setImg(path)
        return 0

    def go():
        info.config(text=f'截图范围:\n位置:({scr.winfo_x()+8}, {scr.winfo_y()})\n窗口大小:{scr.winfo_width()}x{scr.winfo_height()+32}')
        scr.after(10, go)

    info = Label(scr)
    frame = Frame(scr)
    btn = Button(frame, text='截图', font=('微软雅黑', 12), command=lambda:screen(bbox=(scr.winfo_x()+8,scr.winfo_y(),scr.winfo_x()+8+scr.winfo_width(),scr.winfo_y()+scr.winfo_height()+32)))
    btn1 = Button(frame, text='剪贴板', font=('微软雅黑', 12),command=lambda:clip())

    frame.pack(side=BOTTOM)
    btn.pack(side=LEFT)
    btn1.pack(side=LEFT)
    info.pack(side=TOP)

    go()

    scr.mainloop()

    return 0

def setTxt(txt):
    txtAr.config(state=NORMAL)
    txtAr.delete(1.0, END)
    txtAr.insert(INSERT, txt)
    txtAr.config(state=DISABLED)
    return 0

def dragged_files(files):
    path = ''.join(i.decode() for i in files)
    def f():
        df.destroy()
        setImg(path)
    df = Tk()
    f()
    df.mainloop()

leftFrame = Frame(main)
imageFrame= Frame(leftFrame)
imageCanvas = Canvas(imageFrame, width=800, height=450, scrollregion=(0,0,image.width(),image.height()))
xScroll = Scrollbar(imageFrame, orient=HORIZONTAL, command=imageCanvas.xview)
yScroll = Scrollbar(imageFrame, orient=VERTICAL, command=imageCanvas.yview)
imageCanvas.config(xscrollcommand=xScroll.set, yscrollcommand=yScroll.set)
imageCanvas.create_image(0,0,anchor=NW,image=image)

btnFrame = Frame(leftFrame)
btnFrame1 = Frame(leftFrame)

filebtn = Button(btnFrame, text='选择文件', font=('微软雅黑',12), command=lambda:setImg(filedialog.askopenfilename(parent=main)))
cvbtn = Button(btnFrame, text='拍摄照片', font=('微软雅黑',12), command=lambda:setImg(camera()))
grabbtn = Button(btnFrame, text='屏幕截图', font=('微软雅黑',12), command=lambda:grabscreen())
facebtn = Button(btnFrame, text='人脸识别', font=('微软雅黑',12), command=lambda:setTxt(ai.face(f2b64(imagePath))))
bodybtn = Button(btnFrame, text='手势识别', font=('微软雅黑',12), command=lambda:setTxt(ai.body(f2b64(imagePath))))
ocrbtn = Button(btnFrame, text='OCR识别', font=('微软雅黑',12), command=lambda:setTxt(ai.ocr(f2b64(imagePath))))
aibtn = Button(btnFrame1, text='智能识别', font=('微软雅黑',12), command=lambda:setTxt(ai.ai(f2b64(imagePath))))
plantbtn = Button(btnFrame1, text='植物识别', font=('微软雅黑',12), command=lambda:setTxt(ai.plant(f2b64(imagePath))))
animalbtn = Button(btnFrame1, text='动物识别', font=('微软雅黑',12), command=lambda:setTxt(ai.animal(f2b64(imagePath))))
dishbtn = Button(btnFrame1, text='菜肴识别', font=('微软雅黑',12), command=lambda:setTxt(ai.dish(f2b64(imagePath))))
carbtn = Button(btnFrame1, text='车辆识别', font=('微软雅黑',12), command=lambda:setTxt(ai.car(f2b64(imagePath))))
qrbtn = Button(btnFrame1, text='二维码识别', font=('微软雅黑',12), command=lambda:setTxt(ai.qr(f2b64(imagePath))))

txtAr = scrolledtext.ScrolledText(main, width=35, font=('微软雅黑', 11), state=DISABLED)
setTxt('智能图像识别器')

leftFrame.pack(side=LEFT, expand=True, fill=BOTH)
imageFrame.pack(side=TOP, expand=True, fill=BOTH)
yScroll.pack(side=RIGHT, fill=Y)
xScroll.pack(side=BOTTOM,fill=X)
imageCanvas.pack(side=TOP, expand=True, fill=BOTH)

btnFrame.pack(side=TOP)
btnFrame1.pack(side=TOP)
filebtn.pack(side=LEFT)
cvbtn.pack(side=LEFT)
grabbtn.pack(side=LEFT)
facebtn.pack(side=LEFT)
bodybtn.pack(side=LEFT)
ocrbtn.pack(side=LEFT)
aibtn.pack(side=LEFT)
plantbtn.pack(side=LEFT)
animalbtn.pack(side=LEFT)
dishbtn.pack(side=LEFT)
carbtn.pack(side=LEFT)
qrbtn.pack(side=LEFT)

Label(leftFrame).pack(side=TOP)

txtAr.pack(side=RIGHT,fill=Y)

windnd.hook_dropfiles(main, func=dragged_files)

main.mainloop()