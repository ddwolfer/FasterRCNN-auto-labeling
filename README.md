# FasterRCNN-auto-labeling
CH:
<br>
從這裡的FasterRCNN做訓練 : 
<br>
https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10
<br>
然後你會有東西出現在 inference_graph 資料夾裡面
<br>
把 inference_graph 裡面的東西複製過來
<br>
還有 training 裡面的 labelmap.pbtxt
<br>
沒有意外的話大概就可以跑了 下面蔡英文翻譯
<br>
<br>
EN:
<br>
you can train your model form this github:
<br>
https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10
<br>
and then you can get your model from folder "inference_graph" 
<br>
copy whole data from inference_graph and labelmap.pbtxt in training folder
<br>
if there are no accident, it should run
<br>
<br>



##### 可以用下列的指令測試 you can test with the following command

```bash
python main.py --video_name=test.mp4
```
##### 可以更改的變數(main.py裡面也可以看) arguments(you can also see these in main.py)
```bash
video_name : 影片名稱
video_group_folder : 如果你想要一口氣測很多影片，把他們放在同一個資料夾，然後在這邊輸入資料夾名稱
video_frame : 幾個frame辨識一次，預設30，如果影片60frame，就是1秒測2次
num_classes : 有幾個要偵測的物件，預設1
model_path : model來源，預設inference_graph
save_path : 儲存的資料夾，預設output
model_threshold : 偵測目標的閥值，預設0.8，也就是80%準確度
resize_width && resize_height : 如果圖片需要更改比例，可以在這邊調整，預設-1 也就是不調整
```
##### 本人測試的環境 my environment(用 pip list 叫出來的)
```bash
absl-py            0.8.1
astor              0.8.0
attrs              19.3.0
backcall           0.2.0
bleach             3.1.5
certifi            2020.6.20
colorama           0.4.3
cycler             0.10.0
Cython             0.29.14
decorator          4.4.2
defusedxml         0.6.0
entrypoints        0.3
gast               0.3.2
grpcio             1.16.1
importlib-metadata 1.7.0
ipykernel          5.3.0
ipython            7.16.1
ipython-genutils   0.2.0
jedi               0.17.1
Jinja2             2.11.2
jsonschema         3.2.0
jupyter-client     6.1.5
jupyter-core       4.6.3
kiwisolver         1.1.0
Markdown           3.1.1
MarkupSafe         1.1.1
matplotlib         3.1.1
mistune            0.8.4
mkl-fft            1.0.6
mkl-random         1.0.1
nbconvert          5.6.1
nbformat           5.0.7
notebook           6.0.3
numpy              1.15.4
object-detection   0.1
olefile            0.46
packaging          20.4
pandas             0.25.3
pandocfilters      1.4.2
parso              0.7.0
pickleshare        0.7.5
Pillow             7.0.0
pip                19.3.1
prometheus-client  0.8.0
prompt-toolkit     3.0.5
protobuf           3.6.0
Pygments           2.6.1
pyparsing          2.4.6
pypiwin32          223
pyrsistent         0.16.0
python-dateutil    2.8.1
pytz               2019.3
pywin32            227
pywin32-ctypes     0.2.0
pywinpty           0.5.7
pyzmq              19.0.1
Send2Trash         1.5.0
setuptools         44.0.0.post20200106
six                1.13.0
TBB                0.1
tensorboard        1.10.0
tensorflow         1.10.0
termcolor          1.1.0
terminado          0.8.3
testpath           0.4.4
tornado            6.0.3
traitlets          4.3.3
wcwidth            0.2.5
webencodings       0.5.1
Werkzeug           0.16.0
wheel              0.33.6
wincertstore       0.2
zipp               3.1.0
```
