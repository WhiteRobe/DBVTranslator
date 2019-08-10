import xlwt
import re
import os

class TABLE:
    def __init__(self, sentence):
        self.comment, self.table_name, self.columns, self.engine, self.charset = self.parse(sentence)

    def parse(self, s):
        comment, table_name, columns, engine, charset = "None", "None", [], "Default", "Default"
        primary_keys, foreign_keys = [], []
        res = re.search(r'(/\*.*\*/)?\s*CREATE TABLE(?: IF NOT EXISTS)?\s*(\w+)\s*\(.*\)', s, re.I|re.S)
        if res:
            comment, table_name = res.groups()
        engine, charset = self.pick_value(s, ['ENGINE', 'DEFAULT CHARSET'])
        res = re.search(r'(?:/\*.*\*/)?\s*CREATE TABLE(?: IF NOT EXISTS)?\s*\w+\s*\((.*)\)', s, re.I|re.S)
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
                    columns.append(COLUMN(i))

        # 构建键约束
        for i in primary_keys:
            for c in columns:
                if(c.column_name == i[0]):
                    c.key_constraint = 'Primary'
        for i in foreign_keys:
            for c in columns:
                if(c.column_name == i[0]):
                    c.key_constraint = 'Foreign %s.%s' % (i[1], i[2])

        return comment, table_name, columns, engine, charset
    
    def pick_value(self, s, keys):
        values = []
        for k in keys:
            value, res = "Default", re.search(r''+k+' *= *(\w+)', s, re.I)
            if res:
                value = res.group(1)
            values.append(value)
        return tuple(values)


    def output(self, xls):
        bold_title = xlwt.easyxf('font: name Times New Roman, bold on; align:horiz center, vert center')
        normal_style = xlwt.easyxf('font: name Times New Roman; align:horiz center, vert center')
        sheet = xls.add_sheet(self.table_name, cell_overwrite_ok=True)
        sheet.write(0, 0, "表名", bold_title)
        sheet.write(0, 1, self.table_name, normal_style)
        sheet.write(0, 2, "表说明", bold_title)
        sheet.write_merge(0, 0, 2, 9, self.comment, normal_style)

        sheet.write(1, 0, "引擎", bold_title)
        sheet.write(1, 1, self.engine, normal_style)
        sheet.write(1, 2, "编码集", bold_title)
        sheet.write(1, 3, self.charset, normal_style)

        sheet.write(2, 0, "字段名", bold_title)
        sheet.write(2, 1, "标题", bold_title)
        sheet.write(2, 2, "键类型", bold_title)
        sheet.write(2, 3, "值类型", bold_title)
        sheet.write(2, 4, "默认值/枚举值", bold_title)
        sheet.write(2, 5, "非空", bold_title)
        sheet.write_merge(2, 2, 6, 9, "备注", bold_title)

        row = 3
        for c in self.columns:
            sheet.write(row, 0, c.column_name, normal_style)
            sheet.write(row, 1, c.title, normal_style)
            sheet.write(row, 2, c.key_constraint, normal_style)
            sheet.write(row, 3, c.key_type, normal_style)
            sheet.write(row, 4, c.default_value, normal_style)
            sheet.write(row, 5, c.not_null, normal_style)
            sheet.write_merge(row, row, 6, 9, c.desc, normal_style)
            row += 1

    def __str__(self):
        return "comment=%s, table_name=%s, columns_len=%d, engine=%s, charset=%s" \
            % (self.comment, self.table_name, len(self.columns), self.engine, self.charset)

class COLUMN:
    def __init__(self, sentence):
        self.title, self.column_name, self.key_constraint, \
         self.key_type, self.default_value, self.not_null, self.desc = self.parse(sentence)
    
    def parse(self, s):
        title, column_name, key_constraint, key_type, default_value, not_null, desc = "/", "/", "", "/", "", True, "/"

        res = re.search(r'/\*(.*)\*/\s*(\w+) ([\w\(\)]+).*/\*(.*)\*/', s, re.I)
        if res:
            title, column_name, key_type, desc = res.groups()

        # 查询默认值或枚举值
        # res = re.search(r'DEFAULT (\d|(?:\'.*?\'))', s, re.I)
        # if res:
        #     print(res.groups())

        # res = re.search(r'ENUM ?\( ?(.*?) ?\)', s, re.I)
        # if res:
        #     print(res.groups())

        # 查询默认值或枚举值
        res = re.search(r'DEFAULT (\d|(?:\'.*?\'))|ENUM ?\( ?(.*?) ?\)', s, re.I)
        if res:
            default_value = res.group(1) if res.group(1) is not None else res.group(2)
            desc += "; ENUM" if res.group(2) is not None else "" # 是否为枚举值，如是则标注到备注里

        # 是否可空
        not_null = re.search(r'NOT NULL', s, re.I) is not None

        # 是否自增，在备注中标出
        desc += "; AUTO_INC" if re.search(r'AUTO_INCREMENT', s, re.I) is not None else ""

        return title, column_name, key_constraint, key_type, default_value, not_null, desc
    
    def __str__(self):
        return "title=%s, column_name=%s, key_constraint=%s, key_type=%s, default_value=%s, not_null=%s, desc=%s" \
            % (self.title, self.column_name, self.key_constraint, self.key_type, self.default_value, self.not_null, self.desc)


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
                tables.append(TABLE(i))

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
                