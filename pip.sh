pip freeze > pip_requirements.txt
# 可以直接创建conda环境：conda create --name <env> --file <this file>
conda list -e > conda_requirements.txt

# 查看pip下载的缓存
pip cache dir
# 清空pip缓存
pip cache purge

# 查看conda下载的缓存
conda clean --all --dry-run
# 清空conda下载的缓存
conda clean --tarballs
