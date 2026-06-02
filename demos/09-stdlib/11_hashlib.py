#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hashlib模块 - Python标准库哈希与消息摘要

涵盖内容:
  1. md5 - MD5 哈希 (不推荐用于安全)
  2. sha1 - SHA1 哈希 (不推荐用于安全)
  3. sha256 / sha512 - SHA2 安全哈希
  4. 文件哈希计算
  5. HMAC - 密钥哈希消息认证码

参考: https://docs.python.org/zh-cn/3/library/hashlib.html
"""

import hashlib
import hmac
import os
import tempfile


# ============================================================
# 1. MD5 哈希 (已不安全, 仅用于教学/非安全场景)
# ============================================================
print("=" * 60)
print("1. MD5 哈希 (已过时, 不应用于安全场景)")
print("=" * 60)

msg = "Hello, Python!"

# md5 计算 (16字节 = 128位)
md5 = hashlib.md5(msg.encode())
print(f"原文: '{msg}'")
print(f"MD5  (32位hex): {md5.hexdigest()}")
print(f"MD5  (16字节):  {md5.digest()}")

# 分段更新 (大文件常用)
m = hashlib.md5()
m.update(b"Hello, ")
m.update(b"Python!")
print(f"分段更新MD5: {m.hexdigest()}")
print(f"一次计算MD5: {hashlib.md5(b'Hello, Python!').hexdigest()}")
print(f"结果一致: {m.hexdigest() == hashlib.md5(b'Hello, Python!').hexdigest()}")

# [!] 安全警告
print("\n[!] MD5 和 SHA1 已被破解, 不应用于密码存储或安全签名!")
print("   推荐使用: SHA256, SHA512, SHA3, blake2b")

# ============================================================
# 2. SHA 系列哈希
# ============================================================
print("\n" + "=" * 60)
print("2. SHA 系列哈希")
print("=" * 60)

msg = "Hello, Python!".encode()

# sha1 - 160位
print(f"SHA1   (160位): {hashlib.sha1(msg).hexdigest()}")

# sha224 - 224位
print(f"SHA224 (224位): {hashlib.sha224(msg).hexdigest()}")

# sha256 - 256位 (推荐)
print(f"SHA256 (256位): {hashlib.sha256(msg).hexdigest()}")

# sha384 - 384位
print(f"SHA384 (384位): {hashlib.sha384(msg).hexdigest()}")

# sha512 - 512位 (推荐)
print(f"SHA512 (512位): {hashlib.sha512(msg).hexdigest()}")

# 摘要长度对比
print("\n摘要长度对比:")
for algo in ("md5", "sha1", "sha224", "sha256", "sha384", "sha512"):
    h = hashlib.new(algo, msg)
    print(f"  {algo:<6} → {h.digest_size} 字节 ({h.digest_size * 4:>3} 位hex)")

# ============================================================
# 3. 雪崩效应演示
# ============================================================
print("\n" + "=" * 60)
print("3. 雪崩效应 - 微小变化导致巨大差异")
print("=" * 60)

a = "Hello, Python!"
b = "Hello, Python?"  # 只改了最后一个字符

ha = hashlib.sha256(a.encode()).hexdigest()
hb = hashlib.sha256(b.encode()).hexdigest()

print(f"原文 a: {a}")
print(f"原文 b: {b}")
print(f"\nSHA256(a): {ha}")
print(f"SHA256(b): {hb}")

# 计算差异
diff = sum(1 for ca, cb in zip(ha, hb) if ca != cb)
print(f"\n差异位数: {diff} / {len(ha)} (雪崩! 一个字符的改动导致巨大差异)")

# ============================================================
# 4. 文件哈希计算
# ============================================================
print("\n" + "=" * 60)
print("4. 文件哈希计算")
print("=" * 60)


def file_hash(filename, algorithm="sha256"):
    """计算文件哈希 (分块读取, 适合大文件)"""
    h = hashlib.new(algorithm)
    with open(filename, "rb") as f:
        while chunk := f.read(8192):  # 每次读8KB
            h.update(chunk)
    return h.hexdigest()


# 创建临时文件
tmpfile = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt',
                                      encoding='utf-8')
tmp_path = tmpfile.name
try:
    tmpfile.write("这是用于演示文件哈希计算的示例内容。\n" * 1000)
    tmpfile.close()

    # 计算文件哈希
    print(f"文件: {tmp_path}")
    print(f"  MD5:    {file_hash(tmp_path, 'md5')}")
    print(f"  SHA256: {file_hash(tmp_path, 'sha256')}")
    print(f"  SHA512: {file_hash(tmp_path, 'sha512')}")

finally:
    os.unlink(tmp_path)
    print(f"\n已删除临时文件")

# ============================================================
# 5. HMAC - 密钥哈希消息认证码
# ============================================================
print("\n" + "=" * 60)
print("5. HMAC - 密钥哈希消息认证码")
print("=" * 60)

# 共享密钥 (实际应用中需安全保管)
secret_key = b"my_secret_key_12345"
message = "重要消息: 转账 1000元".encode()

# 计算 HMAC
h = hmac.new(secret_key, message, hashlib.sha256)
print(f"消息:   {message.decode()}")
print(f"密钥:   {secret_key.decode()}")
print(f"HMAC-SHA256: {h.hexdigest()}")

# 验证 HMAC - 接收方用相同密钥计算并对比
print("\n=== HMAC 验证演示 ===")

# 正确的验证
h2 = hmac.new(secret_key, message, hashlib.sha256)
is_valid = hmac.compare_digest(h.hexdigest(), h2.hexdigest())
print(f"正确密钥验证:   {'[OK] 通过' if is_valid else '[XX] 失败'} (compare_digest 防时序攻击)")

# 错误密钥验证
wrong_key = b"wrong_secret_key"
h3 = hmac.new(wrong_key, message, hashlib.sha256)
is_valid2 = hmac.compare_digest(h.hexdigest(), h3.hexdigest())
print(f"错误密钥验证:   {'[OK] 通过' if is_valid2 else '[XX] 失败'}")

# 篡改消息验证
tampered_msg = "重要消息: 转账 10000元".encode()  # 多了一个0
h4 = hmac.new(secret_key, tampered_msg, hashlib.sha256)
is_valid3 = hmac.compare_digest(h.hexdigest(), h4.hexdigest())
print(f"篡改消息验证:   {'[OK] 通过' if is_valid3 else '[XX] 失败'}")

# ============================================================
# 6. 密码哈希最佳实践
# ============================================================
print("\n" + "=" * 60)
print("6. 密码哈希最佳实践")
print("=" * 60)

print("[XX] 错误做法 - 直接哈希密码:")
password = "my_password123"
bad_hash = hashlib.sha256(password.encode()).hexdigest()
print(f"  SHA256('{password}') = {bad_hash[:32]}...")
print(f"  问题: 无盐值, 易受彩虹表攻击和暴力破解")

print("\n[OK] 正确做法 - 使用专门的密码哈希库:")
print("  Python 推荐方案:")
print("  1. hashlib.pbkdf2_hmac() - PBKDF2 密钥派生")
print("  2. 第三方库: bcrypt, argon2-cffi")
print("  核心: 盐值 + 多轮迭代 + 慢哈希 → 暴力破解成本极高")

# hashlib 内置的 PBKDF2 示例
print("\n=== hashlib.pbkdf2_hmac() 演示 ===")

password = b"my_secure_password"
salt = os.urandom(16)  # 生成随机盐值 (实际应用需存储盐值)

# PBKDF2 (Password-Based Key Derivation Function 2)
dk = hashlib.pbkdf2_hmac(
    'sha256',            # 哈希算法
    password,            # 密码
    salt,                # 盐值 (16+字节随机数)
    100000,              # 迭代次数 (推荐 ≥ 100,000)
    dklen=32,            # 派生密钥长度 (字节)
)

print(f"原始密码: {password.decode()}")
print(f"盐值 (hex): {salt.hex()}")
print(f"派生密钥 (hex, 前32位): {dk.hex()[:32]}...")

# 验证密码
print(f"\n验证演示:")
salt_stored = salt  # 假设这是之前存储的盐值
dk_stored = dk      # 假设这是之前存储的哈希

# 用相同的盐值和参数验证密码
dk_verify = hashlib.pbkdf2_hmac('sha256', password, salt_stored, 100000)
print(f"  正确密码: {'[OK] 匹配' if dk_verify == dk_stored else '[XX] 不匹配'}")

dk_wrong = hashlib.pbkdf2_hmac('sha256', b'wrong_password', salt_stored, 100000)
print(f"  错误密码: {'[OK] 匹配' if dk_wrong == dk_stored else '[XX] 不匹配'}")
