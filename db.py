from database import get_conn
class Db:
    __conn = ''
    __cursor=''
    __table = ''
    __object=''
    __sql = {
        'filed':'*',
        'where':'',
        'group':'',
        'order':'',
        'having':'',
        'limit':'',
    }


    #初始化构造方法
    def __init__(self):
        #清空缓存
        self. __sql = {
            'filed':'*',
            'where':'',
            'group':'',
            'order':'',
            'having':'',
            'limit':'',
        }
        self.__conn=get_conn()
        self.__cursor = self.__conn.cursor()


    def table(self,table):
            self.__table = table
            return self

    #获取表的主键字段名
    def getPrikey(self):
        sql = "select COLUMN_NAME as id from INFORMATION_SCHEMA.COLUMNS where table_name=\'%s\' AND COLUMN_KEY='PRI' LIMIT 1" % self.__table
        self.__cursor.execute(sql)
        rows = self.__cursor.fetchall()
        # self.__cursor.close()
        # self.__conn.close()
        return rows[0]['id']


    #添加数据并返回自增ID
    def insertGetLastID(self,data):
        if not type(data).__name__=='dict':
            return '类型错误'
        keys = ','.join('`'+str(key)+'`' for key in data.keys())
        values = ','.join('\''+str(val)+'\'' for val in data.values())
        sql = "INSERT INTO `{table}` ({my_keys}) " \
                       "VALUES ({my_values});".\
                        format(table=self.__table,my_keys=keys,my_values=values)
        row=self.__cursor.execute(sql)
        self.__conn.close()
        if row >0:
            return self.__cursor.lastrowid
        else:
            return '添加失败'



    # 添加数据并返回影响行数
    def insert(self, data):
        if not type(data).__name__ == 'dict':
            return '类型错误'
        keys = ','.join('`' + str(key) + '`' for key in data.keys())
        values = ','.join('\'' + str(val) + '\'' for val in data.values())
        sql = "INSERT INTO `{table}` ({my_keys}) " \
              "VALUES ({my_values});". \
            format(table=self.__table, my_keys=keys, my_values=values)
        row = self.__cursor.execute(sql)
        self.__conn.close()
        if row > 0:
            return row
        else:
            return '添加失败'


    #修改数据
    def update(self,data,id=None):
        allstr=''
        if not type(data).__name__ == 'dict':
            return '类型错误'
        for key,value in data.items():
            str= "`{my_key}`='{my_value}'".format(my_key=key,my_value=value)
            allstr+=str+","
        set_str=allstr.strip(',')
        #根据主键id修改
        if not id==None:
            #获取主键DI名称
            pri_name = self.getPrikey()
            sql ="UPDATE {table} SET {set_str} WHERE {pri_name}={id}".\
                format(table=self.__table,set_str=set_str,pri_name=pri_name,id=id)
            row=self.__cursor.execute(sql)
            self.__conn.close()
            return row
        #根据where条件修改
        else:
            sql = "UPDATE {table} SET {set_str} {where}". \
                format(table=self.__table, set_str=set_str,where=self.__sql['where'])
            row = self.__cursor.execute(sql)
            self.__conn.close()
            return row



    #WHERE 语句,数据类型字典,和原声sql
    def where(self,data):
        if type(data).__name__ == 'dict':
            allstr = ''
            for key,value in data.items():
                str= "`{my_key}`='{my_value}'".format(my_key=key,my_value=value)
                allstr+=str+" and "
            set_str=allstr.strip('and ')
            self.__sql['where']='WHERE'+set_str
            return self
        elif type(data).__name__ == 'str':
            self.__sql['where'] = 'WHERE' + data
            return self
        else:
            return '数据类型错误'



    #字段条件,数据类型list
    def field(self,data):
        if not type(data).__name__ == 'list':
            return '数据类型错误'
        field='`,`'.join(data)
        self.__sql['filed']="`{field}`".format(field=field)
        return self

    # 分组条件,数据类型str
    def group(self, data):
        if not type(data).__name__ == 'str':
            return '数据类型错误'
        self.__sql['filed'] = "GROUP BY `{data}`".format(data=data)
        return self

    # 排序条件
    def order(self,key,param):
        if param==None:
            return self
        self.__sql['order']="ORDER BY `{key}` {param}".format(key=key,param=param)
        return self

    #二次筛选
    def having(self,str):
        if not type(str).__name__ == 'str':
            return '数据类型错误'
        self.__sql['order'] = "HAVING {str}".format(str=str)
        return self

    #分页
    def limit(self,*args):
        if len(args)==0:
            return self
        elif len(args)==1:
            self.__sql['limit'] = "LIMIT {data}".format(data=args[0])
            return self
        elif len(args)==2:
            self.__sql['limit'] = "LIMIT {data1},{data2}".format(data1=args[0],data2=args[1])
            return self



    #查询
    def select(self):
        sql = "SELECT {field} "\
              "FROM {table} " \
              "{where} " \
              "{order} " \
              "{group} " \
              "{having} " \
              "{limit}"\
              .format(
                field=self.__sql['filed'],
                table=self.__table,
                where=self.__sql['where'],
                order=self.__sql['order'],
                group=self.__sql['group'],
                having=self.__sql['having'],
                limit=self.__sql['limit'],
               )
        row = self.__cursor.execute(sql)
        self.__conn.close()
        self.__cursor.close()
        return self.__cursor.fetchall()

    # 执行原声的sql
    def query(self,sql):
        row = self.__cursor.execute(sql)
        if 'SELECT' in sql or 'select' in sql:
            self.__conn.close()
            return self.__cursor.fetchall()
        else:
            self.__conn.close()
            return row

    # 删除
    def delete(self, *args):
        if len(args)==0:
            sql = "DELETE FROM {table} {where}" \
                .format(table=self.__table, where=self.__sql['where'])
            row = self.__cursor.execute(sql)
            self.__conn.close()
            return row

        key_name = self.getPrikey()
        if len(args)==1:
            ids = args[0]
        else:
            ids = ','.join(id for id in args)

        sql = "DELETE FROM {table} WHERE {key_name} IN ({ids})" \
            .format(table=self.__table, key_name=key_name, ids=ids)
        row = self.__cursor.execute(sql)
        self.__conn.close()
        return row


    #获取单条数据
    def find(self,id=None):
        # 获取主键ID
        if not id==None:
            key_name = self.getPrikey()
            sql = "SELECT {field} " \
                  "FROM {table} " \
                  "where {key_name}={id}" \
                  "{order} " \
                  "{group} " \
                  "{having} " \
                  "{limit}" \
                .format(
                field=self.__sql['filed'],
                table=self.__table,
                key_name=key_name,
                id=id,
                order=self.__sql['order'],
                group=self.__sql['group'],
                having=self.__sql['having'],
                limit=self.__sql['limit'],
            )
            row = self.__cursor.execute(sql)
            self.__conn.close()
            return self.__cursor.fetchone()
        else:
            sql = "SELECT {field} " \
                  "FROM {table} " \
                  "{where} " \
                  "{order} " \
                  "{group} " \
                  "{having} " \
                  "{limit}" \
                .format(
                field=self.__sql['filed'],
                table=self.__table,
                where=self.__sql['where'],
                order=self.__sql['order'],
                group=self.__sql['group'],
                having=self.__sql['having'],
                limit=self.__sql['limit'],
            )
            row = self.__cursor.execute(sql)
            self.__conn.close()
            return self.__cursor.fetchone()
