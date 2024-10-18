import requests
from bs4 import BeautifulSoup
import os
import time

# Tạo thư mục để lưu ảnh
if not os.path.exists('images'):
    os.makedirs('images')

# Tìm kiếm từ khóa
search_query = 'Dangerous label on the container'
url = f'https://www.google.com/search?hl=vi&tbm=isch&q={search_query}'

# Gửi yêu cầu đến trang web
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Tìm tất cả các thẻ <div> có chứa thông tin ảnh
image_divs = soup.find_all('div', class_='isv-r PNCib MSM1fd BUooTd')

# Tải và lưu ảnh
count = 0
max_images = 10  # Giới hạn số lượng ảnh tải xuống

for div in image_divs:
    if count >= max_images:
        break
    
    try:
        # Trích xuất URL ảnh từ thuộc tính data-ou
        img_url = div.find('img')['data-src']
        if not img_url:
            img_url = div.find('img')['src']
        
        # Tải ảnh
        img_data = requests.get(img_url, headers=headers).content
        
        # Lưu ảnh
        with open(f'images/image_{count}.jpg', 'wb') as f:
            f.write(img_data)
        
        count += 1
        print(f"Đã tải ảnh {count}/{max_images}")
        
        # Tạm dừng để tránh bị chặn
        time.sleep(1)
    
    except Exception as e:
        print(f"Lỗi khi tải ảnh: {str(e)}")

print('Đã tải xong ảnh!')