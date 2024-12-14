# Music-recognition
 实现了调用api实现识别music

# 功能列表
- [x] 从麦克风识别音乐
- [x] 从文件识别音乐
- [ ] 从扬声器识别音乐(其实已经实现了，但是因环境无法测试)
- [ ] 路径（暂时不能带双引号否则会报错）

# 相关文献
实现音乐识别：[点我前往](https://blog.csdn.net/gitblog_01123/article/details/142081755)
实现音乐识别：[点我前往](https://github.com/shazamio/ShazamIO)
扬声器音乐录制：[点我前往](https://docs.python.org/zh-cn/3/library/winsound.html)

# 环境
python3.11

# 安装依赖
```
pip install -r requirements.txt
```
建议使用虚拟环境进行编译，因为可能需要降级pip(库文件不支持高版本pip)

# 其他
由于是在win11上开发，没有适配win10，所以扬声器识别必须有What U Hear设备才行，且在win10上可能会报错。