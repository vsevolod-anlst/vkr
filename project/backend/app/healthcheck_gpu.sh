#!/bin/bash

# 1. Проверяем, доступна ли CUDA через PyTorch
python3 - << 'EOF'
import torch
exit(0 if torch.cuda.is_available() else 1)
EOF

if [ $? -eq 0 ]; then
  echo "CUDA OK (PyTorch)"
  exit 0
fi

# 2. Если PyTorch не видит GPU — пробуем nvidia-smi
nvidia-smi >/dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "CUDA OK (nvidia-smi)"
  exit 0
fi

# 3. Если ничего не работает — GPU реально недоступна
echo "GPU not responding"
exit 1
