# UERemoteRendering

UE局域网多节点渲染脚本

1. ssh链接渲染子节点

2. 工程渲染信息读取

3. 渲染子节点挂在远程硬盘（如果有链接存储SAN，可以修改取代这部分）

4. 拷贝工程到临时本地文件夹（如果带宽允许，可以修改取代这部分）

5. 开始渲染工程

6. 回传渲染结果

7. 本地文件确认

8. 退出ssh链接
   
   

UE LAN multi-node rendering script

1. The ssh link renders child nodes

2. Read project rendering information

3. The rendering child node is hung on the remote hard disk (if there is a link storage SAN, you can modify and replace this part)

4. Copy the project to a temporary local folder (if bandwidth permits, you can modify and replace this part)

5. Start rendering project

6. Return the rendering result

7. Local file confirmation

8. Exit ssh connection



---



参数位于：The parameters are located at:

```
utils_params.py
```

执行文件：Running with:

```
python uerender_Main.py
```



---



@juneleng 

juneleungchan@163.com

20230629
