import os
import xml.etree.ElementTree as ET

# 定义类别映射
class_mapping = {
    "standing": 0,
    "falldown": 1,
}

# 输入和输出目录
input_dir = "./image/"
output_dir = "./yolo_type/"

# 确保输出目录存在
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 遍历XML文件
for xml_file in os.listdir(input_dir):
    if xml_file.endswith(".xml"):
        xml_path = os.path.join(input_dir, xml_file)

        # 解析XML文件
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # 获取图像尺寸
        image_size = root.find('size')
        image_width = float(image_size.find('width').text)
        image_height = float(image_size.find('height').text)

        # 构建输出文件路径
        txt_filename = os.path.splitext(xml_file)[0] + ".txt"
        txt_path = os.path.join(output_dir, txt_filename)

        # 打开要保存YOLO格式数据的文本文件
        with open(txt_path, 'w') as output_file:
            for obj in root.findall('object'):
                class_name = obj.find('name').text
                if class_name not in class_mapping:
                    continue
                class_id = class_mapping[class_name]

                # 获取边界框坐标
                bndbox = obj.find('bndbox')
                xmin = float(bndbox.find('xmin').text)
                ymin = float(bndbox.find('ymin').text)
                xmax = float(bndbox.find('xmax').text)
                ymax = float(bndbox.find('ymax').text)

                # 计算归一化后的中心点坐标和宽度/高度
                x_center = round((xmin + xmax) / (2.0 * image_width), 4)
                y_center = round((ymin + ymax) / (2.0 * image_height), 4)
                width = round((xmax - xmin) / image_width, 4)
                height = round((ymax - ymin) / image_height, 4)

                # 将YOLO格式的数据写入文件
                output_line = f"{class_id} {x_center} {y_center} {width} {height}\n"
                output_file.write(output_line)

        print(f"已处理文件: {xml_file}，结果保存为: {txt_filename}")

print("批量转换完成。")
