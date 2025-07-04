import os


def merge_sql_scripts(output_file='合并后的SQL脚本.sql'):
    """合并当前文件夹中的所有SQL脚本到一个文件中"""
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 获取所有SQL文件并排序
    sql_files = sorted(
        [f for f in os.listdir(current_dir) if f.lower().endswith('.sql') and f != output_file],
        key=lambda x: x.lower()
    )

    if not sql_files:
        print(f"错误：在当前文件夹中未找到SQL文件")
        return

    # 写入合并文件
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for sql_file in sql_files:
            file_path = os.path.join(current_dir, sql_file)
            # 添加文件分隔注释
            outfile.write(f"-- ==== 开始文件: {sql_file} ====\n")
            try:
                # 读取并写入文件内容
                with open(file_path, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                    # 确保文件间有换行分隔
                    if not infile.read().endswith('\n'):
                        outfile.write('\n')
                outfile.write(f"-- ==== 结束文件: {sql_file} ====\n\n")
                print(f"已合并: {sql_file}")
            except Exception as e:
                print(f"合并失败 {sql_file}: {str(e)}")
                outfile.write(f"-- 合并失败 {sql_file}: {str(e)}\n\n")

    print(f"\n合并完成！输出文件: {os.path.join(current_dir, output_file)}")


if __name__ == "__main__":
    merge_sql_scripts()