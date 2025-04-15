git config --global user.email=xiayuancheng333@163.com
git config --global user.name=spike

# 查看全局配置
git config --list
# 清除全局配置
git config --global --unset user.name
git config --global --unset user.email
# 取消仓库关联
git remote remove origin
