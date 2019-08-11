import xlwt


class DRIVER:
    # An Interface
    def parse(self, s):
        return None # Return an tuple


class TABLE:
    def __init__(self, sentence, driver):
        self.comment, self.table_name, self.columns, self.engine, self.charset = driver.parse(sentence)

    def output(self, xls):
        bold_title = xlwt.easyxf('font: name Times New Roman, bold on; align:horiz center, vert center')
        normal_style = xlwt.easyxf('font: name Times New Roman; align:horiz center, vert center')
        sheet = xls.add_sheet(self.table_name, cell_overwrite_ok=True)
        sheet.write(0, 0, "表名", bold_title)
        sheet.write(0, 1, self.table_name, normal_style)
        sheet.write(0, 2, "表说明", bold_title)
        sheet.write_merge(0, 0, 3, 9, self.comment, normal_style)

        sheet.write(1, 0, "引擎", bold_title)
        sheet.write(1, 1, self.engine, normal_style)
        sheet.write(1, 2, "编码集", bold_title)
        sheet.write(1, 3, self.charset, normal_style)

        sheet.write(2, 0, "字段名", bold_title)
        sheet.write(2, 1, "标题", bold_title)
        sheet.write(2, 2, "键类型", bold_title)
        sheet.write(2, 3, "值类型", bold_title)
        sheet.write(2, 4, "默认值/枚举值", bold_title)
        sheet.write(2, 5, "非空/必填", bold_title)
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
    def __init__(self, sentence, driver):
        self.title, self.column_name, self.key_constraint, \
         self.key_type, self.default_value, self.not_null, self.desc = driver.parse(sentence)
    
    def __str__(self):
        return "title=%s, column_name=%s, key_constraint=%s, key_type=%s, default_value=%s, not_null=%s, desc=%s" \
            % (self.title, self.column_name, self.key_constraint, self.key_type, self.default_value, self.not_null, self.desc)


if __name__ == "__main__":
    print("Non-executable file!")