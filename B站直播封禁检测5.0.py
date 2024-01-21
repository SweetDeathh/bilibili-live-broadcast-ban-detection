import sys
import os
import re
import requests
import shutil
import time
import datetime


def my_function():
    # 设置需要提取数字的文件路径
    directory = ''

    # 创建结果存储txt文件
    output_file = 'room_numbers.txt'
    with open(output_file, 'w') as f:
        # 遍历目录下所有文件
        for filename in os.listdir(directory):
            # 使用正则表达式匹配文件名中的数字
            numbers = re.findall('\d+', filename)
            # 如果匹配到数字则写入到txt文件中
            if numbers:
                f.write(' '.join(numbers) + '\n')

    # 定义检查直播间是否被封禁的函数
    def check_room_status(room_id):
        url = f'https://api.live.bilibili.com/room/v1/Room/room_init?id={room_id}'
        response = requests.get(url)

        if response.status_code == 200:
            json_data = response.json()
            if json_data['code'] == 0:
                return json_data['data']['is_locked']
            else:
                print(f'获取房间{room_id}信息失败，错误码：{json_data["code"]}')
                return False
        else:
            print(f'获取房间{room_id}信息失败，状态码：{response.status_code}')
            return False

    # 读取包含B站直播房间号的txt文件并检查直播间是否被封禁
    filename = 'room_numbers.txt'
    banned_rooms = []

    with open(filename, 'r') as f, open('banned_rooms.txt', 'w') as out_file:
        for line in f:
            # 利用正则表达式匹配直播房间号
            match = re.search(r'\d{6,}', line)
            if match:
                room_id = match.group()
                if check_room_status(room_id):
                    banned_rooms.append(room_id)
                    out_file.write(f'{room_id}\n')
                    print(f'房间{room_id}已被封禁，直播间链接为 https://live.bilibili.com/{room_id}')
                else:
                    pass
            else:
                print(f'文本行"{line.strip()}"不包含有效的B站直播房间号')

    print('检查完成！被封禁的房间号已输出到banned_rooms.txt文件。')

    # 读取被封禁的房间号列表
    banned_rooms = []
    with open('banned_rooms.txt', 'r') as f:
        for line in f:
            match = re.search(r'\d{6,}', line)
            if match:
                room_id = match.group()
                banned_rooms.append(room_id)

    
    source_dir = ''
    dest_dir = ''
# 以下为对录播文件进行处理的操作 可省去
   # 移动文件夹
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    # 递归遍历源目录
    for root, dirs, files in os.walk(source_dir, topdown=False):
        for dir_name in dirs:
            # 检查目录名称中是否包含任何被封禁的房间号码，如果包含，则移动到目标目录中
            if any(room in dir_name for room in banned_rooms):
                source_folder = os.path.join(root, dir_name)
                dest_folder = os.path.join(dest_dir, dir_name)

                # 尝试移动文件夹，如果失败，则输出错误信息并继续处理下一个文件夹
                try:
                    shutil.move(source_folder, dest_folder)
                    print(f"移动文件夹 {source_folder} 到 {dest_folder}")
                except Exception as e:
                    print(f"无法移动文件夹 {source_folder}: {e}")
            else:
                continue


                      
    #删除不匹配的文件夹                    
    
    flv_dir = 'D:\B站录播' 
    def remove_folder(folder_path):
        # 递归删除文件夹及其子目录下的所有文件
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                try:
                    os.remove(file_path)
                except OSError as e:
                    print(f"无法删除 {file_path}. 原因: {e}")
                    print("0.1秒后重试...")
                    time.sleep(0.1)
                    try:
                        os.remove(file_path)
                    except OSError as e:
                        print(f"无法删除 {file_path}. 原因: {e}")
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                remove_folder(dir_path)
        # 删除空文件夹
        try:
            os.rmdir(folder_path)
        except OSError as e:
            print(f"无法删除 {folder_path}. 原因: {e}")
            print("0.1秒后重试...")
            time.sleep(0.1)
            try:
                os.rmdir(folder_path)
            except OSError as e:
                print(f"无法删除 {folder_path}. 原因: {e}")

    for root, dirs, files in os.walk(flv_dir, topdown=False):
        for dir_name in dirs:
            if any(room in dir_name for room in banned_rooms):
                # 如果文件夹名包含任何一个被封禁的房间号，则跳过该文件夹
                continue
            else:
                # 否则递归删除该文件夹及其子目录下的所有文件
                folder_to_remove = os.path.join(root, dir_name)
                print(f"删除文件夹: {folder_to_remove}")
                remove_folder(folder_to_remove)

if __name__ == '__main__':
    while True:
        my_function()
        print('程序运行结束时间：', datetime.datetime.now())
        time.sleep(86400)  # 每24小时运行一次
    



