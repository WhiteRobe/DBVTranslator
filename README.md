# DBVTranslator

![License](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)
<a href="https://zenodo.org/badge/latestdoi/201638527"><img src="https://zenodo.org/badge/201638527.svg" alt="DOI"></a>

这个轻量化的小工具将帮助你将一个`sql`文件转化为`xls`文件，以帮助进行数据字典的构建。同时，也可以直接从数据库里导出表结构到`xls`文件。(当前仅支持Mysql数据库)

## 环境依赖

<img src="https://img.shields.io/badge/python-3.5+-blue.svg?logo=python&style=flat-square"/>

需要执行 `pip install -r requirement.txt` 以安装以下轮子：

- xlwt
- pymysql

## 快速上手

### ① 转化sql文件到xls文件
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

**命令行参数**

参数|说明|示例值
:-:|:-:|:-:
--path|sql文件路径|"./test/test.sql"
--charset|sql文件字符集|"utf-8"
--output|xls文件输出路径|"./output.xls"
--debug|输出debug信息|True

### ② 从数据库中导出

`python src/dbvc.py --u root --p password --db database`

导出结果如下：

![](/.github/demo2.jpg)

> 注意：通过此方式导出的数据库结构将会缺少外键信息和标题注释等信息；且目前仅支持MySQL数据库

**命令行参数**

参数|说明|示例值
:-:|:-:|:-:
host|数据库域名|localhost
port|数据库端口|3306
u|数据库访问用户名|root
p|数据库访问密码|password
db|要导出的数据库名|db
output|xls文件输出路径|"./output.xls"
--debug|输出debug信息|True


