pip freeze > pip_requirements.txt
# 可以直接创建conda环境：conda create --name <env> --file <this file>
conda list -e > conda_requirements.txt

# 清空pip缓存
pip cache purge
