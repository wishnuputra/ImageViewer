import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import math  # 回転の計算用
import numpy as np
import os

class ZImageViewer():
    def __init__(self):
        self.master = tk.Tk()
        self.master.geometry("800x600")

        self._pil_image = None
        self._title = "Image Viewer"
        self.master.title(self._title)

        self.setupWidget()

    def startApp(self):
        self.master.mainloop()

    def setupWidget(self):
        padx = 5
        pady = 5
        view_frame = tk.Frame(self.master, borderwidth=5, relief=tk.RIDGE, padx=padx)
        statusbar_frame = tk.Frame(view_frame)
        self._image_info_label = tk.Label(statusbar_frame, text="image info", anchor=tk.E, padx=5)
        self._image_pixel_label = tk.Label(statusbar_frame, text="(x, y)", anchor=tk.W, padx=5)
        self._image_info_label.pack(side=tk.RIGHT)
        self._image_pixel_label.pack(side=tk.LEFT)
        statusbar_frame.pack(side=tk.BOTTOM, fill=tk.X)


        # Canvas
        canvas_width = 1024
        canvas_height = 1024

        self.canvas = tk.Canvas(view_frame, width=canvas_width, height=canvas_height, bg="black")
        self.canvas.pack(expand=True, fill=tk.BOTH)


        self._interaction_frame = tk.Frame(self.master, borderwidth=5, relief=tk.RIDGE, padx=padx)
        first_interaction_frame = tk.Frame(self._interaction_frame, pady=pady)
        open_button = tk.Button(first_interaction_frame, text="Open Image", command=self.openImage)
        open_button.pack()
        first_interaction_frame.pack()
        self._interaction_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        view_frame.pack()

        # self.master.bind("<Button-1>", self.mouseDownLeftClick)  # MouseDown
        # self.master.bind("<B1-Motion>", self.mouseDragLeftClick)  # MouseDrag（ボタンを押しながら移動）
        # self.master.bind("<Motion>", self.mouseMovement)  # MouseMove
        # self.master.bind("<Double-Button-1>", self.mouseDoubleLeftClick)  # MouseDoubleClick
        # self.master.bind("<MouseWheel>", self.mouseWheel)  # MouseWheel

    def openImage(self, event=None):
        filename = tk.filedialog.askopenfilename(
            filetypes=[("Image file", ".bmp .png .jpg .tif"), ("Bitmap", ".bmp"), ("PNG", ".png"), ("JPEG", ".jpg"),
                       ("Tiff", ".tif")],
            initialdir=os.getcwd()
        )
        self.setupImage(filename)

    def setupImage(self, filename):
        if not filename:
            return

        self._image_pil = Image.open(filename)
        self.scaleFitImage(self._image_pil.width, self._image_pil.height)
        self.drawImage(self._image_pil)

        self.master.title(self._title + " - " + os.path.basename(filename))
        self._image_info_label[
            "text"] = f"{self._image_pil.format} : {self._image_pil.width} x {self._image_pil.height} {self._image_pil.mode}"
        os.chdir(os.path.dirname(filename))

    def drawImage(self, img):

        if self._image_pil == None:
            return

        self._image_pil = img

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        inv_mat = np.linalg.inv(self.affine_mat)

        # numpy arrayをアフィン変換用のタプルに変換
        affine_inv = (
            inv_mat[0, 0], inv_mat[0, 1], inv_mat[0, 2],
            inv_mat[1, 0], inv_mat[1, 1], inv_mat[1, 2]
        )

        # PILの画像データをアフィン変換する
        dst = self._image_pil.transform(
            (canvas_width, canvas_height),  # 出力サイズ
            Image.AFFINE,  # アフィン変換
            affine_inv,  # アフィン変換行列（出力→入力への変換行列）
            Image.NEAREST  # 補間方法、ニアレストネイバー
        )

        imgtk = ImageTk.PhotoImage(image=dst)

        item = self.canvas.create_image(
            0, 0,  # 画像表示位置(左上の座標)
            anchor='nw',  # アンカー、左上が原点
            image=imgtk  # 表示画像データ
        )

        self.image = imgtk

    def scaleFitImage(self, image_width, image_height):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if (image_width * image_height <= 0) or (canvas_width * canvas_height <= 0):
            return

        self.reset_transform()

        scale = 1.0
        offsetx = 0.0
        offsety = 0.0

        if (canvas_width * image_height) > (image_width * canvas_height):
            # ウィジェットが横長（画像を縦に合わせる）
            scale = canvas_height / image_height
            # あまり部分の半分を中央に寄せる
            offsetx = (canvas_width - image_width * scale) / 2
        else:
            # ウィジェットが縦長（画像を横に合わせる）
            scale = canvas_width / image_width
            # あまり部分の半分を中央に寄せる
            offsety = (canvas_height - image_height * scale) / 2

        # 拡大縮小
        self.scaleImage(scale)
        # あまり部分を中央に寄せる
        self.translateImage(offsetx, offsety)

    def scaleImage(self, scale: float):
        ''' 拡大縮小 '''
        mat = np.eye(3)  # 単位行列
        mat[0, 0] = scale
        mat[1, 1] = scale

        self.affine_mat = np.dot(mat, self.affine_mat)

    def translateImage(self, offset_x, offset_y):
        mat = np.eye(3)  # 3x3の単位行列
        mat[0, 2] = float(offset_x)
        mat[1, 2] = float(offset_y)

        self.affine_mat = np.dot(mat, self.affine_mat)

    def reset_transform(self):
        self.affine_mat = np.eye(3)

class ContrastSensitivityApp(ZImageViewer):
    def __init__(self):
        super().__init__()
        second_interaction_frame = tk.Frame(self._interaction_frame)
        start_button = tk.Button(second_interaction_frame, text="START")
        start_button.pack()
        second_interaction_frame.pack()


z = ContrastSensitivityApp()
z.startApp()
print(type(z))