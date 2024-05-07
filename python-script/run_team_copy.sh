#!/bin/bash

# 初始化目录
initialize_directories() {
    local INIT_SCRIPT="./initialize_directories.py"
    for json_file in "$@"; do
        echo "Initializing directories for: $json_file"
        python $INIT_SCRIPT "$json_file"
    done
}

# 执行文件操作
process_files() {
    local PYTHON_SCRIPT="./your_copy_script.py"
    local max_jobs=4
    local count=0

    for json_file in "$@"; do
        echo "Processing file: $json_file"
        python $PYTHON_SCRIPT "$json_file" &
        ((count++))
        if [[ $count -ge $max_jobs ]]; then
            wait
            count=0
        fi
    done
    wait
}

# 压缩目录
compress_directories() {
    local COMPRESS_SCRIPT="./compress_directory.py"
    for json_file in "$@"; do
        echo "Compressing directories for: $json_file"
        python $COMPRESS_SCRIPT "$json_file"
    done
}

# 主执行逻辑
main() {
    local json_files=()

    # 读取所有 JSON 文件到数组
    while IFS= read -r -d $'\0' json_file; do
        json_files+=("$json_file")
    done < <(find . -type f -name "*.json" -print0)

    # 初始化所有目录
    initialize_directories "${json_files[@]}"

    # 并行处理文件
    process_files "${json_files[@]}"

    # 压缩所有目录
    compress_directories "${json_files[@]}"
}

# 脚本开始执行
main "$@"
