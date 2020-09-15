from tkinter import *
import easygui
import os
import hashlib
import boto3
from botocore.client import Config
import cv2
import numpy as np
import imageio
import glob

def deduplication():
    dir_path = easygui.diropenbox()
    files=os.listdir(dir_path)
    files=(file for file in files if os.path.isfile( path=os.path.join(dir_path, file)))
    files = sorted(files, key=lambda fn: os.path.getatime(os.path.join(dir_path, fn)))
    hash_table = dict()
    duplicates=[]
    for filename in files:
        filepath=os.path.join(dir_path,filename)
        with open(filepath,'rb') as filepointer:
            content=filepointer.read()
        hasher=hashlib.sha256()
        hasher.update(content)
        _hash=hasher.hexdigest()
        if _hash in hash_table.keys():
            duplicates.append(filepath)
        else:
            hash_table[_hash]=filepath
    for dup in duplicates:
        filename = os.path.split(dup)[1]
        choice = easygui.choicebox(title="Delete Duplicate?", msg="Can i Delete {FILENAME}?".format(FILENAME=filename), choices=['delete', 'ignore'])
        if choice == 'delete':
            os.remove(dup)
def upload():
    def popupmsg():
        popup = Tk()
        popup.wm_title("Completed")
        NORM_FONT = ("Helvetica", 10)
        label2=Label(popup, text="Uploaded", font=NORM_FONT)
        label2.pack(side="top", fill="x", pady=10)
        B1=Button(popup, text="OK", command = popup.destroy)
        B1.pack()
        popup.mainloop()
    ACCESS_KEY_ID = 'AKIAJOQYB3O5WJ4TMFFA'
    ACCESS_SECRET_KEY = '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'
    BUCKET_NAME = 'balu123'
    FILE_NAME = easygui.fileopenbox(multiple=True)
    list1=list(FILE_NAME)
    for elem in list1:
        FILE_NAME=elem
        data = open(FILE_NAME, 'rb')

        s3 = boto3.resource(
            's3',
            aws_access_key_id=ACCESS_KEY_ID,
            aws_secret_access_key=ACCESS_SECRET_KEY,
            config=Config(signature_version='s3v4')
        )
        for bucket in s3.buckets.all():
            print(bucket.name)
        s3.Bucket(BUCKET_NAME).put_object(Key=FILE_NAME, Body=data, ACL='public-read')
    popupmsg()
def imagededup():
    pic=easygui.fileopenbox()
    original=imageio.imread(pic)
    dir1=easygui.diropenbox()
    for path in glob.glob(dir1+"\\*.jpg"):
        im=imageio.imread(path)
        if im.shape==original.shape:
            print("images are same")
            cv2.imshow("duplicate image",im)
            choice = easygui.choicebox(title="Delete Duplicate?", msg="Can i Delete {FILENAME}?".format(FILENAME=path), choices=['delete', 'ignore'])
            if choice == 'delete':
                os.remove(path)
        else:
            print("no duplicates images")
window=Tk()
window.title("DEDUPLICATION")
window.geometry("500x500")
lbl1=Label(window, text="DEDUPLICATION", font=("Times New Roman", 25))
lbl1.pack(anchor="center")
btn1=Button(window,text="SCAN",bg="yellow",fg="red",height="2",width="20",command=deduplication)
btn2=Button(window,text="EXIT",bg="yellow",fg="red",height="2",width="20",command=window.destroy)
btn3=Button(window,text="UPLOAD DATA",bg="yellow",fg="red",height="2",width="20",command=upload)
btn4=Button(window,text="IMAGE DEDUP",bg="yellow",fg="red",height="2",width="20",command=imagededup)
btn1.pack(padx=30, pady=30)
btn3.pack(padx=40, pady=40)
btn4.pack(padx=50, pady=50)
btn2.pack(padx=60, pady=60)