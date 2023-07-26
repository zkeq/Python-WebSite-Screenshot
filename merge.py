from PIL import Image

# 打开图片
img1 = Image.open("0_1080.png")
img2 = Image.open("1080_2160.png")
img3 = Image.open("2160_3240.png")
img4 = Image.open("3240_4000.png")

# 裁剪图片
cropped_img1 = img1.crop((0, 0, img1.width, 1080))
cropped_img2 = img2.crop((0, 0, img2.width, 1080))
cropped_img3 = img3.crop((0, 0, img3.width, 1080))
cropped_img4 = img4.crop((0, 0, img4.width, 760))

# 创建新图像
new_img = Image.new("RGB", (img1.width, 4000))

# 粘贴图片
new_img.paste(cropped_img1, (0, 0))
new_img.paste(cropped_img2, (0, 1080))
new_img.paste(cropped_img3, (0, 2160))
new_img.paste(cropped_img4, (0, 3240))

# 保存图片
new_img.save("new_image.jpg")

