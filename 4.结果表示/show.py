import pandas as pd
import os
import matplotlib.pyplot as plt


s = pd.read_csv('../结果归档/No3/result.csv')
data = {}
for index in s.index:
    key = str(s.loc[index, '大类岗位'])
    if key not in data:
        data[key] = {}
    group = int(s.loc[index, '分组'])
    # 获取详细信息
    job_name = str(s.loc[index, '岗位名称'])
    salary = str(s.loc[index, '薪酬'])
    job_salary = float(salary.replace('K/月', '')) if salary != '薪资面议' and salary != '面议' else 20
    job_location_1 = str(s.loc[index, '地点-区域'])
    job_location_2 = str(s.loc[index, '地点-省'])
    job_location_3 = str(s.loc[index, '地点-市'])
    job_degree = str(s.loc[index, '学历要求'])
    job_experience = str(s.loc[index, '经验要求'])
    job_scale = str(s.loc[index, '企业规模'])
    # 获取综合对象
    job = {
        '名称': job_name,
        '薪酬': job_salary,
        '区域': job_location_1,
        '省': job_location_2,
        '市': job_location_3,
        '学历': job_degree,
        '经验': job_experience,
        '规模': job_scale
    }
    # 添加进列表
    if group in data[key]:
        data[key][group].append(job)
    else:
        data[key][group] = [job]


# 遍历每一个专业
for subject in data:
    plt.rcParams['font.sans-serif'] = ['SimHei']
    path = './结果展示/' + subject + '/'
    cnt = []
    # 遍历每个专业里的分组
    for group in data[subject]:
        cnt.append(len(data[subject][group]))
        if not os.path.exists(path + str(group)):
            os.makedirs(path+str(group))
        salary = 0  # 薪资总和
        salary_degree = {}
        salary_experience = {}
        degree = {}  # 学历统计
        experience = {}  # 经验统计
        scale = {}  # 规模统计
        location_1 = {}
        location_2 = {}
        location_3 = {}
        for info in data[subject][group]:
            salary += info['薪酬']
            # 添加学历要求信息
            job_degree = info['学历']
            if job_degree == '大专以下':
                job_degree = '博士'
            if job_degree in degree:
                degree[job_degree] += 1
            else:
                degree[job_degree] = 1
            if job_degree in salary_degree:
                salary_degree[job_degree] += info['薪酬']
            else:
                salary_degree[job_degree] = info['薪酬']
            # 添加经验要求信息
            job_experience = info['经验']
            if job_experience in experience:
                experience[job_experience] += 1
            else:
                experience[job_experience] = 1
            if job_experience in salary_experience:
                salary_experience[job_experience] += info['薪酬']
            else:
                salary_experience[job_experience] = info['薪酬']
            # 添加地区信息
            job_location_1 = info['区域']
            job_location_2 = info['省']
            job_location_3 = info['市']
            if job_location_1 in location_1:
                location_1[job_location_1] += 1
            else:
                location_1[job_location_1] = 1
            if job_location_2 in location_2:
                location_2[job_location_2] += 1
            else:
                location_2[job_location_2] = 1
            if job_location_3 in location_3:
                location_3[job_location_3] += 1
            else:
                location_3[job_location_3] = 1
            # 添加规模信息
            job_scale = info['规模']
            if job_scale in scale:
                scale[job_scale] += 1
            else:
                scale[job_scale] = 1
        print(group)
        print(salary/len(data[subject][group]))
        salary = salary/len(data[subject][group])  # 平均薪资
        for key in salary_degree:
            salary_degree[key] /= degree[key]
        for key in salary_experience:
            salary_experience[key] /= experience[key]
        # 显示薪资
        values = list(salary_experience.values())
        values.append(salary)
        categories = list(salary_experience.keys())
        categories.append('平均薪资')
        plt.bar(categories, values)
        plt.savefig(path + str(group) + '/经验薪资.png')
        plt.close()

        values = list(salary_degree.values())
        values.append(salary)
        categories = list(salary_degree.keys())
        categories.append('平均薪资')
        plt.bar(categories, values)
        plt.savefig(path + str(group) + '/学历薪资.png')
        plt.close()
        # 显示区域
        values = list(location_1.values())
        categories = list(location_1.keys())
        plt.bar(categories, values)
        plt.savefig(path + str(group) + '/区域.png')
        plt.close()
        # 显示省份
        plt.figure(figsize=(30, 15))
        values = list(location_2.values())
        categories = list(location_2.keys())
        plt.bar(categories, values)
        plt.savefig(path + str(group) + '/省份.png')
        plt.close()
        # 显示学历
        values = list(degree.values())
        categories = list(degree.keys())
        plt.bar(categories, values)
        plt.savefig(path + str(group) + '/学历.png')
        plt.close()
        # 显示经验
        values = list(experience.values())
        categories = list(experience.keys())
        plt.bar(categories, values)
        plt.savefig(path + str(group) + '/经验.png')
        plt.close()
        # 显示公司规模
        values = list(scale.values())
        categories = list(scale.keys())
        plt.bar(categories, values)
        plt.savefig(path + str(group) + '/公司规模.png')
        plt.close()
    values = cnt
    categories = list(data[subject].keys())
    plt.bar(categories, values)
    plt.savefig('./结果展示/' + subject + '/分组分布.png')
    plt.close()


'''
data_1 = {
    '通信工程-通信技术': {
        0: [{'薪酬': 10, '地点': 'location', '学历要求': '硕士', '经验要求': '3-5', '企业规模': '100'}, {}, ],
        1: [{'薪酬': 10, '地点': 'location', '学历要求': '硕士', '经验要求': '3-5', '企业规模': '100'}, {}, ],
    },
    '软件工程-前后端': {
        0: [{'薪酬': 10, '地点': 'location', '学历要求': '硕士', '经验要求': '3-5', '企业规模': '100'}, {}, ],
    },
}
'''
