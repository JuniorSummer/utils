from modelscope import snapshot_download
snapshot_download(
  repo_id = "unsloth/DeepSeek-R1-GGUF",
  local_dir = "/data01/DeepSeek-R1-Q4_K_M/", # 本地位置
  allow_patterns = ["*R1-Q4_K_M*"], # 选择要下载的模型权重
)
