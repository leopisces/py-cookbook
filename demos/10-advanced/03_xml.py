"""
XML 处理 (XML Processing)
============================
Python xml.etree.ElementTree: 解析 XML 字符串/文件、创建 XML、查找元素
(find/findall/iter)、修改 XML、XML 序列化输出。

参考: https://www.runoob.com/python3/python3-xml-processing.html
"""

import xml.etree.ElementTree as ET
import os


# ========== 演示 1: 解析 XML 字符串 ==========
def demo_parse_string():
    """从字符串解析 XML"""
    print("=" * 50)
    print("演示 1: 解析 XML 字符串")
    print("=" * 50)

    # XML 字符串
    xml_string = """<?xml version="1.0" encoding="UTF-8"?>
    <bookstore>
        <book category="编程">
            <title>Python 入门指南</title>
            <author>张三</author>
            <year>2024</year>
            <price>59.00</price>
        </book>
        <book category="文学">
            <title>朝花夕拾</title>
            <author>鲁迅</author>
            <year>1928</year>
            <price>25.00</price>
        </book>
        <book category="编程">
            <title>深入理解计算机系统</title>
            <author>李四</author>
            <year>2023</year>
            <price>89.00</price>
        </book>
    </bookstore>"""

    # fromstring() 从字符串解析
    root = ET.fromstring(xml_string)

    # 根元素
    print(f"  根元素标签: {root.tag}")
    print(f"  根元素属性: {root.attrib}")

    # 遍历子元素
    print("\n  所有书籍:")
    for book in root:
        print(f"\n  [{book.attrib.get('category', '未分类')}] 类:")
        # 遍历 book 的子元素
        for child in book:
            print(f"    {child.tag}: {child.text.strip()}")
    print()


# ========== 演示 2: 解析 XML 文件 ==========
def demo_parse_file():
    """解析 XML 文件"""
    print("=" * 50)
    print("演示 2: 解析 XML 文件 (先创建再解析)")
    print("=" * 50)

    # 创建一个 XML 文件用于演示
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <catalog>
        <product id="001">
            <name>机械键盘</name>
            <price currency="CNY">399</price>
            <stock>50</stock>
        </product>
        <product id="002">
            <name>无线鼠标</name>
            <price currency="CNY">129</price>
            <stock>200</stock>
        </product>
        <product id="003">
            <name>显示器支架</name>
            <price currency="CNY">199</price>
            <stock>30</stock>
        </product>
    </catalog>"""

    filepath = os.path.join(os.path.dirname(__file__), "_demo_products.xml")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(xml_content)

    # parse() 从文件解析
    tree = ET.parse(filepath)
    root = tree.getroot()

    print(f"  根元素: {root.tag}")
    print(f"  子元素数量: {len(root)}")
    print()

    for product in root:
        pid = product.get("id")
        name = product.find("name").text
        price = product.find("price").text
        currency = product.find("price").get("currency", "")
        print(f"  产品 {pid}: {name} - {currency} {price}")

    # 清理临时文件
    os.remove(filepath)
    print()


# ========== 演示 3: 查找元素 - find / findall / iter ==========
def demo_find_elements():
    """使用 find / findall / iter 查找 XML 元素"""
    print("=" * 50)
    print("演示 3: 查找元素 (find / findall / iter)")
    print("=" * 50)

    xml_data = """<?xml version="1.0"?>
    <school>
        <class name="一年级">
            <student id="1" gender="男">小明</student>
            <student id="2" gender="女">小红</student>
            <student id="3" gender="男">小刚</student>
        </class>
        <class name="二年级">
            <student id="4" gender="女">小丽</student>
            <student id="5" gender="男">小强</student>
            <teacher>王老师</teacher>
        </class>
        <class name="三年级">
            <student id="6" gender="女">小芳</student>
            <student id="7" gender="男">小军</student>
        </class>
    </school>"""

    root = ET.fromstring(xml_data)

    # --- find(): 查找第一个匹配的元素 ---
    first_student = root.find(".//student")  # .// 表示任意层级
    print(f"  find('.//student'): {first_student.text} (id={first_student.get('id')})")

    # --- findall(): 查找所有匹配的元素 ---
    all_students = root.findall(".//student")
    print(f"\n  findall('.//student') 找到 {len(all_students)} 个学生:")
    for stu in all_students:
        print(f"    {stu.text} (id={stu.get('id')}, 性别={stu.get('gender')})")

    # --- 条件查找: 按属性筛选 ---
    print("\n  findall 按属性筛选:")
    # 查找 gender="女" 的学生
    female_students = root.findall(".//student[@gender='女']")
    for stu in female_students:
        print(f"    女生: {stu.text}")

    # --- iter(): 遍历所有指定标签的元素 ---
    print("\n  iter('student') 遍历所有 student 元素:")
    for stu in root.iter("student"):
        print(f"    {stu.text}")

    # --- iter() 遍历所有元素 ---
    print("\n  iter() 遍历所有元素:")
    tags = [elem.tag for elem in root.iter()]
    print(f"    所有标签: {tags}")
    print()


# ========== 演示 4: 创建 XML 文档 ==========
def demo_create_xml():
    """使用 ElementTree 创建新的 XML 文档"""
    print("=" * 50)
    print("演示 4: 创建 XML 文档")
    print("=" * 50)

    # 方法1: 使用 Element / SubElement
    # 创建根元素
    root = ET.Element("contacts")

    # 添加子元素
    contact1 = ET.SubElement(root, "contact", id="1")
    ET.SubElement(contact1, "name").text = "张三"
    ET.SubElement(contact1, "phone").text = "13800138000"
    ET.SubElement(contact1, "email").text = "zhangsan@example.com"

    contact2 = ET.SubElement(root, "contact", id="2")
    ET.SubElement(contact2, "name").text = "李四"
    ET.SubElement(contact2, "phone").text = "13900139000"

    # 创建 ElementTree 对象
    tree = ET.ElementTree(root)

    # 格式化输出 (Python 3.9+ 支持 ET.indent)
    ET.indent(tree, space="  ")

    # 转换为字符串
    xml_str = ET.tostring(root, encoding="unicode")
    print("  生成的 XML:")
    print(xml_str)

    # 方法2: 直接用字符串构造（适合固定模板）
    print("\n  也可以直接使用 f-string 或模板生成 XML 字符串")

    # 写入文件演示
    filepath = os.path.join(os.path.dirname(__file__), "_demo_contacts.xml")
    tree.write(filepath, encoding="utf-8", xml_declaration=True)
    print(f"\n  已写入文件: {filepath}")

    # 验证: 读回来
    tree2 = ET.parse(filepath)
    root2 = tree2.getroot()
    for contact in root2:
        name = contact.find("name").text
        phone_el = contact.find("phone")
        phone = phone_el.text if phone_el is not None else "无"
        print(f"  联系人 {contact.get('id')}: {name}, 电话: {phone}")

    os.remove(filepath)
    print()


# ========== 演示 5: 修改 XML 文档 ==========
def demo_modify_xml():
    """修改 XML: 更新文本、修改属性、添加/删除元素"""
    print("=" * 50)
    print("演示 5: 修改 XML 文档")
    print("=" * 50)

    xml_data = """<?xml version="1.0"?>
    <inventory>
        <item id="A001">
            <name>苹果</name>
            <quantity>50</quantity>
            <price>8.5</price>
        </item>
        <item id="A002">
            <name>香蕉</name>
            <quantity>30</quantity>
            <price>5.0</price>
        </item>
        <item id="A003">
            <name>橙子</name>
            <quantity>0</quantity>
            <price>6.0</price>
        </item>
    </inventory>"""

    root = ET.fromstring(xml_data)
    print("  原始 XML:")
    print(ET.tostring(root, encoding="unicode").strip())

    # --- 修改文本 ---
    print("\n  --- 修改文本 ---")
    # 修改第一个 item 的 name
    first_item = root.find("item")
    first_item.find("name").text = "红富士苹果"
    print(f"  item[0].name 改为: {first_item.find('name').text}")

    # --- 修改属性 ---
    print("\n  --- 修改属性 ---")
    second_item = root.findall("item")[1]
    second_item.set("id", "A002-MOD")  # 修改 id 属性
    print(f"  item[1] 的 id 改为: {second_item.get('id')}")

    # --- 添加新元素 ---
    print("\n  --- 添加新元素 ---")
    new_item = ET.SubElement(root, "item", id="A004")
    ET.SubElement(new_item, "name").text = "葡萄"
    ET.SubElement(new_item, "quantity").text = "25"
    ET.SubElement(new_item, "price").text = "15.0"

    # --- 删除元素 ---
    print("\n  --- 删除元素 ---")
    # 删除 quantity=0 的 item
    for item in root.findall("item"):
        qty = int(item.find("quantity").text)
        if qty == 0:
            root.remove(item)
            print(f"  已删除 quantity=0 的商品")

    # --- 最终结果 ---
    print("\n  修改后的 XML:")
    ET.indent(root, space="  ")
    print(ET.tostring(root, encoding="unicode").strip())

    # 库存汇总
    total_qty = sum(int(item.find("quantity").text) for item in root)
    print(f"\n  总库存量: {total_qty}")
    print()


# ========== 主程序入口 ==========
if __name__ == "__main__":
    demo_parse_string()
    demo_parse_file()
    demo_find_elements()
    demo_create_xml()
    demo_modify_xml()
    print("\n=== 所有 XML 处理演示完成! ===")
