import trimesh
import numpy as np
import os
from pyproj import Proj
import time

def get_numeric_subdirectories(directory_path):
    subdirectories = [name for name in os.listdir(directory_path) 
                      if os.path.isdir(os.path.join(directory_path, name)) and name.isdigit()]
    return subdirectories

def write_subdirectories_to_file(sorted_subdirectories, file_path):
    with open(file_path, 'w') as f:
        # 将每个子目录名称写入文件，每个名称占一行
        for directory in sorted_subdirectories[:-1]:
            f.write(directory + "\n")
        # 最后一行领出来for循环写，避免文件末尾多出一行空行
        f.write(sorted_subdirectories[-1])

def read_data_between_brackets(file_path):
    data = []
    inside_brackets = False

    with open(file_path, 'r') as file:
        for line in file:
            if ')\n' == line:
                inside_brackets = False
                break
            if inside_brackets:
                line = float(line.rstrip('\n'))  # 移除行末的换行符
                data.append(line)
            if '(\n' == line:
                inside_brackets = True
    return data

def generate_color_gradient(num_segments, start_color, end_color):
    # 获取颜色渐变数组
    gradient_colors = [(255,255,255)]
    for i in range(num_segments-1):
        t = i / (num_segments - 1)
        r = start_color[0] + (end_color[0] - start_color[0]) * t
        g = start_color[1] + (end_color[1] - start_color[1]) * t
        b = start_color[2] + (end_color[2] - start_color[2]) * t
        gradient_colors.append([round(r), round(g), round(b)])  # 将颜色值为0-255的范围 round()四省五入取整

    return gradient_colors


def get_interval_index(H, intervals):
    # 区间定义，第一个元素表示最小值，最后一个元素表示无穷大，其他值为各个区间的上限值
    # intervals = [0,0.01, 0.25, 0.50, 1.0, 1.50, 2.0, 2.5,
    #              3, 3.5, 4, 4.5, 5, 7.5, 10, float('inf')]

    # 循环遍历所有区间，找到第一个H小于等于的区间，然后返回对应的索引
    for i in range(len(intervals)):
        if H <= intervals[i+1]:
            return i

    # 如果H小于所有区间的第一个值，则属于第一个区间
    return 0

# 主函数main()
# 记录开始时间
start_time = time.time()
directory_path = './flood/30years'
subdirectories = get_numeric_subdirectories(directory_path)
# 按照数字大小排序
sorted_subdirectories = sorted(subdirectories, key=lambda x: int(x))

# 因为每个文件夹里面的DEM数据都是不变的，读取一份就行
S_file_path = os.path.join(directory_path, sorted_subdirectories[1], 'S')
S_data = read_data_between_brackets(S_file_path)  # 关键数据 DEM

# 生成颜色渐变数组，从浅蓝色到深蓝色
intervals = [0, 0.01,0.25, 0.50, 1.0, 1.50, 2.0, 2.5,
             3, 3.5, 4, 4.5, 5, 7.5, 10, float('inf')]
num_segments = len(intervals)-1
start_color = [149, 208, 238]
end_color = [10, 9, 145]
gradient_colors = generate_color_gradient(
    num_segments, start_color, end_color)
# 定义一个空列表用于存储面信息
faces = []
# 定义一个空列表用于存储顶点信息
vertices = []

# 打开并读取文件
with open( os.path.join(
    directory_path, '../mesh_1108.2dm'), 'r') as file:
    # 逐行读取文件内容
    for line in file:
        # 如果行以'E3T'开头，提取第3到5个数，并将其转为整数后减1（因为索引从0开始）
        if line.startswith('E3T'):
            face_data = list(map(int, line.split()[2:5]))
            face_data = [x - 1 for x in face_data]  # 减1以符合Python的索引规则
            faces.append(face_data)
        if line.startswith('ND'):
            vertex_data = list(map(float, line.split()[2:5]))
            vertices.append(vertex_data)
# 输出faces
# print(faces)


# 定义一个UTM投影坐标系统，用做center.txt坐标（utm113）转换为经纬度坐标
utm113 = Proj("+proj=tmerc +lon_0=113.35 +y_0=0 +x_0=500000 +ellps=IAU76 \
+towgs84=-7.849095,18.661172,12.682502,0.809388,-1.667217,-56.719783,-3.30421e-007 +units=m +no_defs")

count = 1
threshold = 0.05
for directory in sorted_subdirectories:
    print(f'当前正在写入第{count}/{len(sorted_subdirectories)}个文件夹----{directory}')

    # Hrgb_inputfile_path = os.path.join(
    #     directory_path, directory, 'Hrgb.txt')
    glb_outputfile_directory = os.path.join(
        directory_path, 'glb', directory)
    
    # 检查文件夹路径是否存在，如果不存在则创建它
    if not os.path.exists(glb_outputfile_directory):
        os.makedirs(glb_outputfile_directory)
    glb_outputfile_path = os.path.join(glb_outputfile_directory, 'triangle_mesh_' + str(threshold) + '.glb')
    # 从不同时刻文件读取数据并拆分成顶点坐标和颜色信息
    # data = np.loadtxt(Hrgb_inputfile_path, delimiter=',')
    # H = data[:, :1]  # 第一列是H
    H_file_path = os.path.join(directory_path,  directory, 'H')
    H = read_data_between_brackets(H_file_path)  # 关键数据 水深
    # facesColor = data[:, 1:]    # 后三列是r, g, b颜色值
    # faces = [[0, 1, 2],[0, 1, 3]]

    rectify_vertices = np.array(vertices)
    position_min_x = float('inf')
    position_min_y = float('inf')
    position_min_z = float('inf')
    position_max_x = 0
    position_max_y = 0
    position_max_z = 0
    for i, value in enumerate(faces):
        # print(value)
        for index in value:
            if rectify_vertices[index,2] == vertices[index][2]:
                rectify_vertices[index,2] += H[i]
                # if H[i] > threshold:
                #     if rectify_vertices[index,0] < position_min_x:
                #         position_min_x = rectify_vertices[index,0]
                #     elif rectify_vertices[index,0] > position_max_x:
                #         position_max_x = rectify_vertices[index,0]

                #     if rectify_vertices[index,1] < position_min_y:
                #         position_min_y = rectify_vertices[index,1]
                #     elif rectify_vertices[index,1] > position_max_y:
                #         position_max_y = rectify_vertices[index,1]
                    
                #     if rectify_vertices[index,2] < position_min_z:
                #         position_min_z = rectify_vertices[index,2]
                #     elif rectify_vertices[index,2] > position_max_z:
                #         position_max_z = rectify_vertices[index,2]

    # utm_x = (position_min_x + position_max_x)/2
    # utm_y = (position_min_y + position_max_y)/2
    # height = position_min_z
    # longitude, latitude = utm113(utm_x, utm_y, inverse=True)
    # 中心点修正 ---> utm_x: 505817.0445, utm_y: 3509140.655, Height: 61.0309417
    # 中心点修正 ---> longitude: 113.39592268502284, latitude: 31.704985763068212, Height: 61.0309417
    longitude = 113.39592268502284
    latitude = 31.704985763068212
    height = 61.0309417
    # 修改vertices，纠正glb中心点
    position_file_path = os.path.join(
        directory_path, directory, 'center_point_position_'+str(threshold)+'.txt')
    # 打开文件并读取内容
    # with open(position_file_path, 'r') as file:
    #     line = file.readline().strip()  # 读取并去除首尾空白字符
    #     longitude, latitude, height = map(float, line.split())
    utm_x, utm_y = utm113(longitude, latitude, inverse=False)
    print(f"中心点修正 ---> longitude: {longitude}, latitude: {latitude}, Height: {height}")
    print(f"中心点修正 ---> utm_x: {utm_x}, utm_y: {utm_y}, Height: {height}")
    
    # rectify_vertices = np.array(vertices)
    rectify_vertices = rectify_vertices - np.array([utm_x,utm_y,height])
    # 把下表面 + H 变为 上表面
    # rectify_vertices[:,2] =  rectify_vertices[:,2] + np.array(H)
    rectify_vertices = rectify_vertices.tolist()

    # 清除H<0.05的faces数据
    clearFaces = []
    clearFacesColor = []
    for i, h in enumerate(H):
        if(h > threshold):
            clearFaces.append(faces[i])

            # 获取对应 H 的颜色表示 rgb
            index = get_interval_index(h, intervals)
            rgbList = gradient_colors[index]
            # 伽马值γ < 1的情况有时被称作编码伽马值（encoding gamma），
            # 而执行这个编码运算所使用上述幂定律的过程也叫做伽马压缩（gamma compression）；
            # 相对地，伽马值γ > 1的情况有时也被称作解码伽马值（decoding gamma），
            # 而执行这个解码运算所使用上述幂定律的过程也叫做“伽马展开（gamma expansion）”。
            # clearFacesColor.append(rgbList[i])
            clearFacesColor.append([(val / 255) ** 2.2 * 255 for val in rgbList])
            # clearFacesColor.append([149, 208, 238])


    mesh = trimesh.Trimesh(vertices=rectify_vertices, faces=clearFaces)
    mesh.visual.face_colors = clearFacesColor    
    
    # 创建一个字典来存储自定义属性（可能有问题，目前还没起作用 -> 0927）
    custom_attributes = {}  
    # 为每个面分配自定义数据（例如，面的编号）
    for i, face in enumerate(mesh.faces):
        custom_attributes[i] = {"KHR_materials_unlit": {}}

    # 将自定义属性分配给网格
    mesh.metadata['face_attributes'] = custom_attributes

    # 保存为glb格式
    mesh.export(glb_outputfile_path, file_type='glb')
    
    count += 1
    # 用trimesh内置的方法进行可视化
    # mesh.show()

# 保存子目录为directory_path = '/flood/30years/glb' 里面的subcontent.txt文件
subcontent_file_path = os.path.join(
    directory_path, 'glb/subcontent.txt')
# 调用函数，将子目录名称写入 subcontent.txt 文件
write_subdirectories_to_file(sorted_subdirectories, subcontent_file_path)
# 记录结束时间
end_time = time.time()
# 计算运行时间
execution_time = end_time - start_time
print("代码运行时间为：", execution_time, "秒")
# 代码运行时间为： 500.0 秒