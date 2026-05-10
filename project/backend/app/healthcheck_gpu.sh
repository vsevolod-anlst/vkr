#!/bin/bash

nvidia-smi >/dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "GPU not responding"
  exit 1
fi

echo "OK"
exit 0
