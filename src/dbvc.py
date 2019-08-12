import xlwt
import pymysql
import re
import traceback
from structure import TABLE, COLUMN, DRIVER


class CoTableDriver(DRIVER):
    def parse(self, s):
        comment, table_name, columns, engine, charset = "", "None", [], "Default", "Default"
        table_name, columns = s
        return comment, table_name, columns, engine, charset


class CoColumnDriver(DRIVER):
    def parse(self, s):
        title, column_name, key_constraint, key_type, default_value, not_null, desc = "/", "/", "", "/", "", "YES", "/"
        column_name, key_type, not_null, key_constraint, default_value, desc = s

        default_value = "" if default_value is None else default_value

        # 将ENUM的信息提取出来
        # res = re.search(r'ENUM *\( *(.*?) *\)', key_type, re.I)
        # if res:
        #     default_value += res.group(1)
        #     key_type = "ENUM"
        #     desc += "; ENUM"
        
        # 转义空值定义 
        not_null = "YES" if not_null == "NO" else "NO"

        return title, column_name, key_constraint, key_type, default_value, not_null, desc

        
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default="localhost", type=str)
    parser.add_argument('--port', default=3306, type=int)
    parser.add_argument('--u', default="root", type=str)
    parser.add_argument('--p', default="password", type=str)
    parser.add_argument('--db', default="database", type=str)
    parser.add_argument('--output', default="./output.xls", type=str)
    parser.add_argument('--debug', default=False, type=bool)
    args = parser.parse_args()
    print(args)

    try:
        tables = []
        connection = pymysql.connect(host=args.host, port=args.port, user=args.u, password=args.p, db=args.db)
        with connection.cursor() as cursor:
            cursor.execute('SHOW TABLES')
            table_names = cursor.fetchall()

            for table_name in table_names:
                columns = []
                cursor.execute('DESC '+table_name[0])
                table_desc = cursor.fetchone()

                while table_desc:
                    columns.append(COLUMN(table_desc, CoColumnDriver()))
                    table_desc = cursor.fetchone()

                tables.append(TABLE((table_name[0], columns), CoTableDriver()))

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
        print('Warning: Key Constraint Information(Specific:Foreign Key) will be ignore.')
    except:
        print('Failed! Mysql Server not connected!')
        traceback.print_exc()
    finally:
        connection.close()

    