curl -fsSL https://ollama.com/install.sh | sh

nohup ollama serve > ollama_output.txt 2>&1 &
ollama list
ollama run xxx

mkdir Modelfile
"
FROM ./DeepSeek-V2-Lite-Chat.Q4_K_M.gguf
"
ollama create deepseekv2-lite-chat -f Modelfile

ollama stop xxx
