

class Job:
    job_type = ""  # 岗位类别包括六种：软件开发、数据分析、算法、测试、AI、安全
    job_name = ""  # 岗位名称
    job_salary = ""  # 岗位薪酬
    job_place = ""  # 岗位工作地点
    job_diploma = ""  # 岗位学历要求
    job_experience = ""  # 岗位经验要求
    job_company = ""  # 岗位企业名称
    job_company_scale = ""  # 岗位企业规模
    job_company_place = ""  # 岗位公司地域
    job_duty = ""  # 岗位职责
    job_requirement = ""  # 岗位要求

    def __init__(self, source):
        # 输入一个json格式数据，解析基本属性
        self.job_name = source['jobName']
        self.job_salary = source['provideSalaryString']
        self.job_place = source['jobAreaString']
        self.job_diploma = source['degreeString']
        self.job_experience = source['workYearString']
        self.job_company = source['fullCompanyName']
        self.job_company_scale = source['companySizeString']
        self.job_company_place = source['jobAreaString']

    def __str__(self):
        return "岗位类型 : %s\n岗位名称 : %s\n岗位薪资 : %s\n工作地点 : %s\n学历要求 : %s\n经历要求 : %s\n公司名称 : %s\n公司规模 : %s\n公司地点 : %s\n工作职责 : %s\n工作要求 : %s\n" % (self.job_type, self.job_name, self.job_salary, self.job_place, self.job_diploma, self.job_experience, self.job_company, self.job_company_scale, self.job_company_place, self.job_duty, self.job_requirement)

    def set_type(self, job_type):
        self.job_type = job_type

    def set_duty(self, job_duty):
        self.job_duty = job_duty

    def set_requirement(self, job_requirement):
        self.job_requirement = job_requirement
