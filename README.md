# DBVTranslator
这个小工具将帮助你将一个`sql`文件转化为`xls`文件，以帮助进行数据字典的构建。

## 环境依赖
- python 3.6
- xlwt

## 快速上手
`python src/dbvd.py --path "./test/test.sql"`

将可以把`test/test.sql`中的相关文件转化为`output.xls`，如：
```
/* 表1注释 */
CREATE TABLE IF NOT EXISTS test1 (
    /* 标题1 */ id INT NOT NULL AUTO_INCREMENT /* 备注1 */,  
    /* 标题2 */ V1 INT DEFAULT 0 /* 备注2 */, 
    PRIMARY KEY (id),
    FOREIGN KEY (V1) REFERENCES test3 (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```
将被转化为：

![](/.github/demo.jpg)

> 注意：目前仅支持如`test/test.sql`文件所示的sql语句标准排版格式。

## 命令行参数
参数|说明|示例值
:-:|:-:|:-:
--path|sql文件路径|"./test/test.sql"
--charset|sql文件字符集|"utf-8"
--output|xls文件输出路径|"./output.xls"
--debug|输出debug信息|True