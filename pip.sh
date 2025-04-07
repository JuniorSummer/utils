pip install xxx -i https://pypi.tuna.tsinghua.edu.cn/simple
conda install -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main pytorch==2.4.0 torchvision==0.19.0 torchaudio==2.4.0 pytorch-cuda=12.4 -c pytorch -c nvidia

# 保存环境
pip freeze > pip_requirements.txt
# 可以直接创建conda环境：conda create --name <env> --file <this file>
conda list -e > conda_requirements.txt
# conda删除环境
conda remove --name ktransformers --all

# 查看pip下载的缓存
pip cache dir
# 清空pip缓存
pip cache purge

# 查看conda下载的缓存
conda clean --all --dry-run
# 清空conda下载的缓存
conda clean --all
