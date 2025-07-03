import numpy as np
import os
import time
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from pyproj import Proj
import matplotlib.tri as mtri
import gc


def get_numeric_subdirectories(directory_path):
    subdirectories = [
        name
        for name in os.listdir(directory_path)
        if os.path.isdir(os.path.join(directory_path, name)) and name.isdigit()
    ]
    return subdirectories


def read_data_between_brackets(file_path):
    data = []
    inside_brackets = False

    with open(file_path, "r") as file:
        for line in file:
            if ")\n" == line:
                inside_brackets = False
                break
            if inside_brackets:
                line = float(line.rstrip("\n"))  # 移除行末的换行符
                data.append(line)
            if "(\n" == line:
                inside_brackets = True
    return data


# 主函数main()
# 记录开始时间
start_time = time.time()
directory_path = "./flood/50years/openForm"
subdirectories = get_numeric_subdirectories(directory_path)
# 按照数字大小排序
sorted_subdirectories = sorted(subdirectories, key=lambda x: int(x))

# 因为每个文件夹里面的DEM数据都是不变的，读取一份就行
S_file_path = os.path.join(directory_path, sorted_subdirectories[1], "S")
S_data = read_data_between_brackets(S_file_path)  # 关键数据 DEM

# 定义一个空列表用于存储面信息
faces = []
# 定义一个空列表用于存储顶点信息
vertices = []

# 打开并读取文件
with open(os.path.join(directory_path, "../../mesh_1108.2dm"), "r") as file:
    # 逐行读取文件内容
    for line in file:
        # 如果行以'E3T'开头，提取第3到5个数，并将其转为整数后减1（因为索引从0开始）
        if line.startswith("E3T"):
            parts = line.split()
            face_data = [int(parts[2]) - 1, int(parts[3]) - 1, int(parts[4]) - 1]
            faces.append(face_data)
        elif line.startswith("ND"):
            parts = line.split()
            vertex_data = [float(parts[2]), float(parts[3]), float(parts[4])]
            vertices.append(vertex_data)

# 转换为numpy数组以提高后续计算效率
faces = np.array(faces)
vertices = np.array(vertices)

# 转换为numpy数组以提高后续计算效率
faces = np.array(faces)
vertices = np.array(vertices)

# 预计算边界范围和网格参数（这些在所有时间步中都是相同的）
points = vertices[:, :2]  # XY 平面点坐标
x_min, x_max = points[:, 0].min(), points[:, 0].max()
y_min, y_max = points[:, 1].min(), points[:, 1].max()
width = x_max - x_min
height = y_max - y_min

print(f"边界范围: x_min={x_min}, x_max={x_max}, y_min={y_min}, y_max={y_max}")
print(f"网格宽度: {width}, 网格高度: {height}")
print(f"经纬度范围: ({x_min}, {y_max}) to ({x_max}, {y_min})")
utm113 = Proj(
    "+proj=tmerc +lon_0=113.35 +y_0=0 +x_0=500000 +ellps=IAU76 \
+towgs84=-7.849095,18.661172,12.682502,0.809388,-1.667217,-56.719783,-3.30421e-007 +units=m +no_defs"
)
lon_x_min, lat_y_min = utm113(x_min, y_min, inverse=True)
print(f"WGS84: lon_x_min={lon_x_min}, lat_y_min={lat_y_min}")
lon_x_max, lat_y_max = utm113(x_max, y_max, inverse=True)
print(f"WGS84: lon_x_max={lon_x_max}, lat_y_max={lat_y_max}\n")

resolution = 1.0
Nx = int(width / resolution)
Ny = int(height / resolution)

# 构造插值网格（只需要计算一次）
grid_y, grid_x = np.mgrid[y_min : y_max : Ny * 1j, x_min : x_max : Nx * 1j]

# 预定义颜色区间和渐变色
intervals = [0.01, 0.25, 0.50, 1.0, 1.50, 2.0, 2.5, 3, 3.5, 4, float("inf")]
start_color = np.array([149, 208, 238])
end_color = np.array([10, 9, 145])
gradient_colors = [
    np.round(
        start_color + (end_color - start_color) * (i / (len(intervals) - 1))
    ).astype(int)
    for i in range(len(intervals) - 1)
]

count = 1  # 打印进度

for directory in sorted_subdirectories:
    # if count < 109:
    #     count += 1
    #     continue
    print(
        f"当前正在生成第 {count}/{len(sorted_subdirectories)} 个PNG图像----{directory}"
    )

    # 读取水深数据
    H_file_path = os.path.join(directory_path, directory, "H")
    H = np.array(read_data_between_brackets(H_file_path))  # 转为numpy数组

    # 计算水深值 - 使用向量化操作
    rectify_vertices = vertices.copy()

    # 把OpenFoam计算的面H值加到对应的顶点上（简化处理，第一个遍历到的点+H值）
    for i, value in enumerate(faces):
        # 这里遍历每个面的3个顶点索引
        for index in value:
            if rectify_vertices[index, 2] == vertices[index][2]:
                rectify_vertices[index, 2] += H[i]

    values = rectify_vertices[:, 2] - vertices[:, 2]

    # 进行插值
    # grid_z = griddata(points, values, (grid_x, grid_y), method="linear", fill_value=0)

    # 构建三角剖分对象
    triang = mtri.Triangulation(points[:, 0], points[:, 1], triangles=faces)

    # 使用线性插值
    interpolator = mtri.LinearTriInterpolator(triang, values)

    # 插值执行
    grid_z = interpolator(grid_x, grid_y).filled(0)

    # # 构造 RGB 图像 - 使用更高效的向量化操作
    rgb_image = np.zeros((grid_z.shape[0], grid_z.shape[1], 4), dtype=np.uint8)

    # 创建掩码用于透明区域
    valid_mask = grid_z > 0.00001

    if np.any(valid_mask):
        # 使用 np.digitize 进行高效的区间分类
        valid_h = grid_z[valid_mask]
        color_indices = np.digitize(valid_h, intervals[1:])  # 跳过第一个值

        # 批量应用颜色
        for k in range(len(gradient_colors)):
            color_mask = color_indices == k
            if np.any(color_mask):
                rgb = gradient_colors[k]
                valid_coords = np.where(valid_mask)
                selected_rows = valid_coords[0][color_mask]
                selected_cols = valid_coords[1][color_mask]
                rgb_image[selected_rows, selected_cols] = [rgb[0], rgb[1], rgb[2], 255]

    # 保存前进行垂直翻转
    rgb_image = np.flipud(rgb_image).copy()

    # 创建PNG保存目录
    png_output_directory = os.path.join(directory_path, "../png", directory)
    if not os.path.exists(png_output_directory):
        os.makedirs(png_output_directory)

    # 保存为 PNG 图像
    png_output_path = os.path.join(png_output_directory, "flood_interpolated.png")
    plt.imsave(png_output_path, rgb_image)
    print(f"PNG图像已保存到: {png_output_path}")

    count += 1
    # 清理内存,要不然整个大循环会导致内存不够
    del H, rectify_vertices, values, triang, interpolator, grid_z, rgb_image
    # 手动触发垃圾回收
    if count % 10 == 0:
        gc.collect()

# 计算总运行时间
end_time = time.time()
total_time = end_time - start_time
print(f"\n总共处理了 {len(sorted_subdirectories)} 个时间步")
print(f"总运行时间: {total_time:.2f} 秒")
print(f"平均每个时间步: {total_time/len(sorted_subdirectories):.2f} 秒")
