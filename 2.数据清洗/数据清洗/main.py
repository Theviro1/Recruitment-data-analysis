import pandas as pd
import re


def switch_keyword(f_keyword, f_name):
    f_type = ""
    f_detail = ""
    if f_keyword == 'AI' or f_keyword == '深度学习' or f_keyword == '神经网络':
        f_type = '计算机科学'
        f_detail = '人工智能'

    elif f_keyword == 'DSP' or f_keyword == '天线通信' or f_keyword == '通信技术工程师' or f_keyword == '通信算法' or f_keyword == '卫星' or f_keyword == '卫星导航' or f_keyword == '光纤':
        f_type = '通信工程'
        f_detail = '通信技术'

    elif f_keyword == 'FPGA' or f_keyword == '单片机' or f_keyword == '电子' or f_keyword == '电子工程师':
        f_type = '电子科学与技术'
        f_detail = '数字电子'

    elif f_keyword == 'C/C++开发' or f_keyword == 'golang开发' or f_keyword == 'Java开发' or f_keyword == 'python开发' or f_keyword == '软件开发' or f_keyword == '软件开发工程师':
        f_type = '软件工程'
        f_detail = '前后端'

    elif f_keyword == '测试' or f_keyword == '测试工程师' or f_keyword == '软件测试':
        f_type = '软件工程'
        f_detail = '软件测试'

    elif f_keyword == '定位' or f_keyword == '单片机' or f_keyword == '计算机视觉' or f_keyword == '数据结构与算法' or f_keyword == '算法安全' or f_keyword == '算法工程师' or f_keyword == '图像处理':
        f_type = '计算机科学'
        f_detail = '算法'
    elif f_keyword == '优化' and '算' in f_name:
        f_type = '计算机科学'
        f_detail = '算法'

    elif f_keyword == '网络安全' or f_keyword == '网信安全' or f_keyword == '信息安全':
        f_type = '网络工程'
        f_detail = '网络安全'

    elif f_keyword == '数据安全' or f_keyword == '数据分析' or f_keyword == '数据分析工程师':
        f_type = '信息管理'
        f_detail = '数据分析'

    elif f_keyword == '大数据' or f_keyword == '数据开发':
        f_type = '信息管理'
        f_detail = '数据开发'

    elif f_keyword == '电路设计':
        f_type = '微电子与集成电路'
        f_detail = '集成电路'

    elif f_keyword == 'FPGA' or f_keyword == '单片机' or f_keyword == '电子' or f_keyword == '电子工程师':
        f_type = '电子科学与技术'
        f_detail = '数字电子'

    elif f_keyword == '电子元器件' or f_keyword == '光电技术' or f_keyword == '光电技术工程师' or f_keyword == '光电信息处理' or f_keyword == '光学系统':
        f_type = '电子科学与技术'
        f_detail = '光电'

    elif f_keyword == '嵌入式软件' or f_keyword == '嵌入式软件工程师':
        f_type = '电子信息工程'
        f_detail = '嵌入式'

    elif f_keyword == '仿真测试' or f_keyword == '控制':
        f_type = '电子信息工程'
        f_detail = '电气控制'

    elif f_keyword == 'SLAM' or f_keyword == '导航技术' or f_keyword == '导航技术工程师':
        f_type = '电子信息工程'
        f_detail = '导航'

    elif f_keyword == '安全工程师' or f_keyword == '安全':
        if '网' in f_name or 'Information' in f_name:
            f_type = '网络工程'
            f_detail = '网络安全'
        elif '数据' in f_name:
            f_type = '信息管理'
            f_detail = '数据分析'
        elif '运维' in f_name:
            f_type = '网络工程'
            f_detail = '网络运维'
        elif '算法' in f_name:
            f_type = '计算机科学'
            f_detail = '算法'

    return f_type, f_detail


def switch_location(f_location):
    location_dict = {
        '西北': {
            '陕西省': ['西安', '铜川', '宝鸡', '咸阳', '渭南', '延安', '汉中', '榆林', '安康', '商洛'],
            '甘肃省': ['兰州', '嘉峪关', '金昌', '白银', '天水', '武威', '张掖', '平凉', '酒泉', '庆阳', '陇南'],
            '青海省': ['西宁', '海东', '海北藏族自治州', '黄南藏族自治州', '海南藏族自治州', '果洛藏族自治州', '玉树藏族自治州', '海西蒙古族藏族自治州'],
            '宁夏回族自治区': ['银川', '石嘴山', '吴忠', '固原', '中卫'],
            '新疆维吾尔自治区': ['乌鲁木齐', '克拉玛依', '吐鲁番', '哈密', '昌吉回族自治州', '博尔塔拉蒙古自治州',
                                 '巴音郭楞蒙古自治州', '阿克苏地区', '克孜勒苏柯尔克孜自治州', '喀什地区'],
        },
        '北方': {
            '内蒙古自治区': ['呼和浩特', '包头', '乌海', '赤峰', '通辽', '鄂尔多斯', '呼伦贝尔', '巴彦淖尔', '乌兰察布', '兴安盟'],
        },
        '东北': {
            '辽宁省': ['沈阳', '大连', '鞍山', '抚顺', '本溪', '丹东', '锦州', '营口', '阜新', '辽阳', '葫芦岛'],
            '吉林省': ['长春', '吉林', '四平', '辽源', '通化', '白山', '松原', '白城', '延边朝鲜族自治州'],
            '黑龙江省': ['哈尔滨', '齐齐哈尔', '鸡西', '鹤岗', '双鸭山', '大庆', '伊春', '佳木斯', '七台河', '牡丹江'],
        },
        '华北': {
            '北京市': ['北京'],
            '天津市': ['天津'],
            '河北省': ['石家庄', '唐山', '秦皇岛', '邯郸', '邢台', '保定', '张家口', '承德', '沧州', '廊坊', '雄安'],
            '山西省': ['太原', '大同', '阳泉', '长治', '晋城', '朔州', '晋中', '运城', '忻州', '临汾', '吕梁'],
        },
        '华东': {
            '上海市': ['上海'],
            '江苏省': ['南京', '苏州', '无锡', '常州', '徐州', '南通', '连云港', '淮安', '盐城', '扬州', '常熟', '昆山', '太仓', '泰州', '张家港', '镇江'],
            '浙江省': ['杭州', '宁波', '温州', '绍兴', '湖州', '嘉兴', '金华', '衢州', '舟山', '台州', '海宁', '丽水', '义乌'],
            '安徽省': ['合肥', '芜湖', '蚌埠', '淮南', '马鞍山', '淮北', '铜陵', '安庆', '黄山', '滁州', '宣城'],
            '福建省': ['福州', '厦门', '漳州', '泉州', '三明', '莆田', '南平', '龙岩', '宁德'],
            '江西省': ['南昌', '景德镇', '萍乡', '九江', '新余', '鹰潭', '赣州', '吉安', '宜春', '抚州', '上饶'],
            '山东省': ['济南', '青岛', '淄博', '枣庄', '东营', '烟台', '潍坊', '济宁', '泰安', '威海', '滨州', '德州', '聊城', '临沂', '日照', ],
        },
        '华中': {
            '河南省': ['郑州', '开封', '洛阳', '平顶山', '安阳', '鹤壁', '新乡', '焦作', '濮阳', '许昌', '南阳', '驻马店'],
            '湖北省': ['武汉', '黄石', '十堰', '宜昌', '襄阳', '鄂州', '荆门', '孝感', '荆州', '黄冈', '咸宁'],
            '湖南省': ['长沙', '株洲', '湘潭', '衡阳', '邵阳', '岳阳', '常德', '张家界', '益阳', '娄底', '郴州'],
        },
        '华南': {
            '广西壮族自治区': ['南宁', '柳州', '桂林', '梧州', '北海', '防城港', '钦州', '贵港', '玉林', '百色'],
            '广东省': ['东莞', '佛山', '广州', '河源', '惠州', '江门', '清远', '汕头', '韶关', '深圳', '湛江', '肇庆', '中山', '珠海'],
            '海南省': ['海口', '三亚', '三沙', '儋州', '五指山', '琼海', '文昌', '万宁', '东方', '定安', '澄迈县'],
        },
        '西南': {
            '重庆市': ['重庆'],
            '四川省': ['成都', '自贡', '攀枝花', '泸州', '德阳', '绵阳', '广元', '遂宁', '内江', '乐山', '达州', '广安'],
            '贵州省': ['贵阳', '六盘水', '遵义', '安顺', '毕节', '铜仁', '黔西南布依族苗族自治州', '黔东南苗族侗族自治州', '黔南布依族苗族自治州'],
            '云南省': ['昆明', '曲靖', '玉溪', '保山', '昭通', '丽江', '普洱', '临沧', '楚雄彝族自治州', '大理白族自治州', '楚雄州'],
            '西藏自治区': ['拉萨', '日喀则', '昌都', '林芝', '山南', '那曲', '阿里'],
        },
        '南部': {
            '香港特别行政区': ['香港'],
            '澳门特别行政区': ['澳门'],
            '台湾省': ['台湾'],
        }
    }
    for key_1, value_1 in location_dict.items():  # value_1是大区域key_1下的省份的集合
        for key_2, value_2 in value_1.items():  # value_2是大省份key_2下的城市的列表
            for value in value_2:  # 遍历列表里的每一个城市
                if f_location == value:
                    return key_1, key_2
    return None, None


def switch_experience(f_years):
    f_result = ''
    if '0-1年' in f_years or '一年以下' in f_years or '应届' in f_years:
        f_result = '在校/应届生'
    elif '10年以上' in f_years:
        f_result = '7年以上'
    elif '1-3年' in f_years or '1年' in f_years or '2年' in f_years:
        f_result = '1-3年'
    elif '3-5年' in f_years or '3-4年' in f_years:
        f_result = '3-5年'
    elif '5-10年' in f_years or '5-7年' in f_years or '8-9年' in f_years:
        f_result = '5-7年'
    elif '经验不限' in f_years or '无需经验' in f_years:
        f_result = '经验不限'
    else:
        f_result = '经验不限'

    return f_result


def switch_scale(f_scale):
    f_result = ''
    f_scale = str(f_scale)
    if f_scale == 'nan':
        return ''
    if '10000人以上' in f_scale:  # 只有10000人以上会出现‘以上‘这个字段
        f_result = '10000人以上'
    elif '少于50人' in f_scale:
        f_result = '100人以下'
    else:
        f_match = re.search(r'\d+-\d+', f_scale)
        if f_match is None:
            print(f_scale)
            return ''
        f_before, f_delimiter, f_after = f_match.group().partition('-')
        if int(f_after) < 100:
            f_result = '100人以下'
        elif int(f_before) >= 100 and int(f_after) <= 500:
            f_result = '100-499人'
        elif int(f_before) >= 500 and int(f_after) <= 1000:
            f_result = '500-999人'
        elif int(f_before) >= 1000 and int(f_after) <= 10000:
            f_result = '1000-9999人'
    return f_result


def switch_salary(f_salary):
    if '面议' in f_salary:
        return f_salary
    elif f_salary == 'nan' or f_salary is None:
        return ''
    else:
        power_time = 1  # 没有年月日默认以月为单位
        power_amount = 1  # 没有千或万默认以千为单位
        # 判断以年月日哪个为单位
        if '/年' in salary:
            power_time = float(1/12)
        elif '/天' in salary:
            power_time = 30.0
        else:
            power_time = 1.0
        # 判断以百千万哪个为单位
        if 'k' in salary or '千' in salary or 'K' in salary:  # 以千为单位
            power_amount = 1.0
        elif '万' in salary:  # 以万为单位
            power_amount = 10.0
        else:
            power_amount = 0.001  # 以元为单位

        if '-' in salary:
            f_before, f_delimiter, f_after = salary.partition('-')
            match_before = float(re.search(r'\d+(\.\d+)?', f_before).group())  # 匹配数字部分
            match_after = float(re.search(r'\d+(\.\d+)?', f_after).group())  # 匹配数字部分
            expect_salary = round(power_amount * power_time * (match_before + match_after)/2, 1)  # 平均薪资

        else:
            match = float(re.search(r'\d+(\.\d+)?', salary).group())
            expect_salary = round(power_amount * power_time * match, 1)
        if expect_salary >= 200:
            expect_salary /= 12  # 一个月不可能比20w还多，所以一定是原始数据没有注明年薪但是给的数据是年薪
        f_result = str(expect_salary) + 'K/月'
        return f_result


def switch_degree(f_degree):
    if '大专' in f_degree:
        f_result = '大专'
    elif '本科' in f_degree:
        f_result = '本科'
    elif '硕士' in f_degree:
        f_result = '硕士'
    elif '博士' in f_degree:
        f_result = '博士'
    else:
        f_result = '大专以下'
    return f_result


data = pd.read_csv('../final_data/final.csv')
order = ['id', '大类专业', '大类岗位', '岗位名称', '薪酬', '地点-区域', '地点-省', '地点-市', '学历要求', '经验要求', '企业名称', '所属行业', '企业规模', '岗位详情']
for index in data.index:
    # id
    data.loc[index, 'id'] = index+1  # 把序号重新编号，同index一样从1开始递增

    # 添加大类专业、岗位两个列
    keyword = str(data.loc[index, '岗位类别'])
    name = str(data.loc[index, '岗位名称'])
    type, detail = switch_keyword(keyword, name)  # 根据岗位类别和岗位名称获取到大类专业、大类岗位
    data.loc[index, '大类专业'] = type
    data.loc[index, '大类岗位'] = detail

    # 获取薪资数字
    salary = str(data.loc[index, '薪酬'])
    salary = switch_salary(salary)
    data.loc[index, '薪酬'] = salary

    # 获取地区信息，添加地点-区域、省、市三个列
    location = str(data.loc[index, '地点'])
    city = location  # 获取到省份
    if '・' in location:
        before, delimiter, after = location.partition('・')  # ・分隔符前边的
        city = before
    elif '-' in location:
        before, delimiter, after = location.partition('-')  # -分隔符前面的
        city = before
    part, province = switch_location(str(city))  # 获取到城市对应的大区域和省份
    if part is None:
        part = ''
    if province is None:
        province = ''
    data.loc[index, '地点-区域'] = part
    data.loc[index, '地点-省'] = province
    data.loc[index, '地点-市'] = city

    # 获取学历信息
    degree = str(data.loc[index, '学历要求'])
    degree = switch_degree(degree)
    data.loc[index, '学历要求'] = degree

    # 经验要求
    experience = str(data.loc[index, '经验要求'])
    experience = switch_experience(experience)
    data.loc[index, '经验要求'] = experience

    # 企业规模
    scale = str(data.loc[index, '企业规模'])
    scale = switch_scale(scale)
    data.loc[index, '企业规模'] = scale

    # 所属行业
    # 合并岗位要求和职责
    duty = str(data.loc[index, '岗位职责'])
    requirement = str(data.loc[index, '岗位要求'])
    if duty == 'nan':
        duty = ''
    if requirement == 'nan':
        requirement = ''
    info = duty + requirement
    data.loc[index, '岗位详情'] = info


data.drop('序号', axis=1, inplace=True)  # 删除岗位类别一列
data.drop('岗位类别', axis=1, inplace=True)  # 删除岗位类别一列
data.drop('岗位职责', axis=1, inplace=True)  # 删除岗位职责一列
data.drop('岗位要求', axis=1, inplace=True)  # 删除岗位要求一列
data.drop('地点', axis=1, inplace=True)  # 删除地点一列
data.drop('所属地域', axis=1, inplace=True)  # 删除所属地域一列
data = data[order]
print(data.to_csv('../final_data/final_result.csv', index=False))
