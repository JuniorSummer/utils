# 检测端口
netstat -tlnp | grep 1927

# 查询当前文件夹所占空间
du -sh . && df -h .
du -sh
df -hl

# 删除容器和镜像
docker rm -f CONTAINER ID
docker rmi -f IMAGE ID
# 保存镜像
docker commit 7ca736d99653 yolov5:v6.2
docker save -o yolov5-v6.2.tar yolov5:v6.2
docker load -i yolov5-v6.2.tar
