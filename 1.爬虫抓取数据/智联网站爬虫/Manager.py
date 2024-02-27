import pymysql


class Manager:
    DB_host = "bj-cynosdbmysql-grp-buhkitz0.sql.tencentcdb.com"
    DB_user = "root"
    DB_password = "21306Train"
    DB_db = "worm"
    connection = pymysql.connect(
            host=DB_host,
            user=DB_user,
            password=DB_password,
            db=DB_db,
            port=20638
        )
    cursor = connection.cursor()

    def __init__(self):
        pass

    # 给url库里添加一个url，输入url和他的岗位类型
    def push_url(self, url, type):
        try:
            sql = "insert into url values(%s,%s,%s,%s)"
            values = (None, url, False, type)
            self.cursor.execute(sql, values)
            self.connection.commit()
            print("push_url success...")
        except:
            print("push_url error!")
            self.connection.rollback()

    # 返回一个url库里还没有被爬取的url和他的岗位类型
    def pop_url(self):
        sql = "select * from url where status = FALSE"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        # 如果结果为空就说明没有url了，并返回None
        if result is None:
            return None, None
        # 修改这条数据的status从未读FALSE改为已读TRUE
        try:
            id = result[0]
            sql = "update url set status = TRUE where id = %s" % id
            self.cursor.execute(sql)
            self.connection.commit()
            print("pop_url success...")
        except:
            print("pop_url error!")
            self.connection.rollback()
        return result[1], result[3]

    # 将爬取结果Job类型存入到result表内
    def save(self, job):
        try:
            sql = "insert into result values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (None, job.job_type, job.job_name, job.job_salary, job.job_place, job.job_diploma, job.job_experience, job.job_company, job.job_company_scale, job.job_company_place, job.job_duty, job.job_requirement)
            self.cursor.execute(sql, values)
            self.connection.commit()
            print("save success...")
        except:
            print("save error!")
            self.connection.rollback()
