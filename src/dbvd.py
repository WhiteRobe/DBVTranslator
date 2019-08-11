import xlwt
import re
from structure import TABLE, COLUMN, DRIVER


class ReTableDriver(DRIVER):
    def parse(self, s):
        comment, table_name, columns, engine, charset = "", "None", [], "Default", "Default"
        primary_keys, foreign_keys = [], []

        # 提取表信息
        res = re.search(r'(/\*.*\*/)?\s*CREATE TABLE(?: IF NOT EXISTS)?\s*(\w+)\s*\(.*\)', s, re.I|re.S)
        if res:
            comment, table_name = res.groups()
        engine, charset = self.pick_value(s, ['ENGINE', 'DEFAULT CHARSET'])
        res = re.search(r'(?:/\*.*\*/)?\s*CREATE TABLE(?: IF NOT EXISTS)?\s*\w+\s*\((.*)\)', s, re.I|re.S)

        # 构建列信息
        if res:
            sentences = res.group(1).split('\n')  # Do not use re.split() here!
            for i in sentences: # every sentence only contains no more than 1 blank as devider
                if len(i)<=0:
                    continue
                res_pri = re.search(r'PRIMARY KEY ?\( *(\w+) *\)', i, re.I)
                res_for = re.search(r'FOREIGN KEY ?\( *(\w+) *\) ?REFERENCES (\w+) ?\( *(\w+) *\)', i, re.I)
                if res_pri:
                    primary_keys.append(res_pri.groups())
                    pass
                elif res_for:
                    foreign_keys.append(res_for.groups())
                    pass
                else:
                    columns.append(COLUMN(i, ReCulomnDriver()))

        # 构建键约束
        for i in primary_keys:
            for c in columns:
                if(c.column_name == i[0]):
                    c.key_constraint = 'PRI'
        for i in foreign_keys:
            for c in columns:
                if(c.column_name == i[0]):
                    c.key_constraint = 'FOR %s.%s' % (i[1], i[2])

        return comment, table_name, columns, engine, charset
        
    def pick_value(self, s, keys):
        # 按键值对获取信息，如 a=c，将返回c
        values = []
        for k in keys:
            value, res = "Default", re.search(r''+k+' *= *(\w+)', s, re.I)
            if res:
                value = res.group(1)
            values.append(value)
        return tuple(values)


class ReCulomnDriver(DRIVER):
    def parse(self, s):
        title, column_name, key_constraint, key_type, default_value, not_null, desc = "/", "/", "", "/", "", "YES", "/"

        # 提取列基本信息
        res = re.search(r'/\*(.*)\*/\s*(\w+) ([\w\(\)]+).*/\*(.*)\*/', s, re.I)
        if res:
            title, column_name, key_type, desc = res.groups()

        # 查询默认值或枚举值 r'DEFAULT (\d|(?:\'.*?\'))' || r'ENUM ?\( ?(.*?) ?\)'
        res = re.search(r'DEFAULT (\d|(?:\'.*?\'))|ENUM ?\( ?(.*?) ?\)', s, re.I)
        if res:
            default_value = res.group(1) if res.group(1) is not None else res.group(2)
            desc += "; ENUM" if res.group(2) is not None else "" # 是否为枚举值，如是则标注到备注里

        # 是否可空
        not_null = "YES" if re.search(r'NOT NULL', s, re.I) is not None or default_value != "" else "NO"

        # 查询是否为UNIQUE键值
        key_constraint = "UNI" if re.search(r'UNIQUE', s, re.I) is not None else ""

        # 查询是否为无符号值
        key_type += " UNSIGNED" if re.search(r'UNSIGNED', s, re.I) is not None else ""

        # 是否自增，在备注中标出
        desc += "; AUTO_INC" if re.search(r'AUTO_INCREMENT', s, re.I) is not None else ""

        return title, column_name, key_constraint, key_type, default_value, not_null, desc

        
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', default=None, type=str)
    parser.add_argument('--charset', default="utf-8", type=str)
    parser.add_argument('--output', default="./output.xls", type=str)
    parser.add_argument('--debug', default=False, type=bool)
    args = parser.parse_args()
    print(args)

    tables = []
    with open(args.path, encoding=args.charset) as file:
        sentences = re.sub(r'[ \t\r\f]+',' ', file.read()).split(";") # remove multiple blanks
        for i in sentences:
            if len(i)>0:
                tables.append(TABLE(i, ReTableDriver()))

        xls = xlwt.Workbook()
        for t in tables:
            # 控制台输出测试信息
            if args.debug:
                print(t)
                for c in t.columns:
                    print(c)
                print()
            t.output(xls)
        xls.save(args.output)
    
    print('Success!')
                