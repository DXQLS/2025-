import pandas as pd
import os
import sys


def excel_to_sql(excel_file_path, bas_deduction_rule_id, medicine_type):
    """
    将Excel文件转换为SQL插入脚本

    参数:
    excel_file_path (str): Excel文件路径
    bas_deduction_rule_id (str): 扣除规则ID
    medicine_type (str): 药品类型
    """
    # 读取Excel文件
    try:
        df = pd.read_excel(excel_file_path)
    except Exception as e:
        print(f"错误: 无法读取Excel文件 - {e}")
        return

    # 目标字段映射 (Excel列名: SQL列名: 默认值)
    field_mapping = {
        '项目名称': {'sql_col': 'item_name', 'default': "''"},
        '项目代码': {'sql_col': 'item_code', 'default': "''"},
        '费用类别': {'sql_col': 'fee_type', 'default': "''"},
        '诊疗名称': {'sql_col': 'common_name', 'default': "''"},
        '费用等级': {'sql_col': 'fee_level', 'default': "'0'"},
        '在职自付比例': {'sql_col': 'common_ratio', 'default': "'0.0000'"},
        '项目内含': {'sql_col': 'include', 'default': "''"},
        '除外项目': {'sql_col': 'exception', 'default': "''"},
        '备注': {'sql_col': 'remark', 'default': "''"}
    }

    # 确保所有需要的字段都存在于Excel中
    missing_fields = [excel_col for excel_col in field_mapping.keys() if excel_col not in df.columns]
    if missing_fields:
        print(f"警告: Excel文件中缺少以下列: {', '.join(missing_fields)}")
        print("这些字段将使用默认值")

    # 生成SQL文件名 (使用Excel文件名)
    file_name, _ = os.path.splitext(os.path.basename(excel_file_path))
    sql_file_path = f"{file_name}.sql"

    # 打开SQL文件进行写入
    with open(sql_file_path, 'w', encoding='utf-8') as sql_file:
        # 写入SQL文件头部注释
        sql_file.write(f"-- SQL脚本: {sql_file_path}\n")
        sql_file.write(f"-- 从Excel文件: {os.path.basename(excel_file_path)}\n")
        sql_file.write(f"-- 生成时间: {pd.Timestamp.now()}\n\n")

        # 遍历DataFrame的每一行
        for _, row in df.iterrows():
            # 构建SQL值列表
            values = []

            # 添加映射的字段值
            for excel_col, info in field_mapping.items():
                value = row.get(excel_col, None)

                # 使用默认值如果值为空
                if pd.isna(value):
                    values.append(info['default'])
                elif isinstance(value, str):
                    # 替换反斜杠为正斜杠
                    value = value.replace("\\", "/")
                    # 转义单引号并添加引号
                    escaped_value = value.replace("'", "''")
                    values.append(f"'{escaped_value}'")
                elif isinstance(value, (int, float)):
                    # 数值类型直接转换为字符串
                    values.append(str(value))
                else:
                    # 其他类型转换为字符串并添加引号
                    values.append(f"'{str(value)}'")

            # 添加额外的两个字段
            values.append(f"'{bas_deduction_rule_id}'")  # bas_deduction_rule_id
            values.append(f"'{medicine_type}'")  # medicine_type

            # 构建INSERT语句
            columns = ', '.join(
                [info['sql_col'] for info in field_mapping.values()]) + ', bas_deduction_rule_id, medicine_type'
            values_str = ', '.join(values)
            sql = f"INSERT INTO bas_medicine ({columns}) VALUES ({values_str});\n"

            # 写入SQL语句到文件
            sql_file.write(sql)

    print(f"成功生成SQL脚本: {sql_file_path}")
    print(f"共处理 {len(df)} 条记录")


if __name__ == "__main__":
    # =============== 在这里修改你的参数 ===============
    EXCEL_FILE_PATH = "河北省石家庄目录亿保2025-诊疗库 (1).xls"  # 替换为你的Excel文件路径
    BAS_DEDUCTION_RULE_ID = "17"  # 替换为你的扣除规则ID
    MEDICINE_TYPE = "2"  # 替换为你的药品类型
    # =================================================

    # 检查文件是否存在
    if not os.path.exists(EXCEL_FILE_PATH):
        print(f"错误: 文件 '{EXCEL_FILE_PATH}' 不存在")
        sys.exit(1)

    # 执行转换
    excel_to_sql(EXCEL_FILE_PATH, BAS_DEDUCTION_RULE_ID, MEDICINE_TYPE)