import torch
import time

size = 4096

print("PyTorch 사용 가능한 GPU:", torch.cuda.device_count())


# PyTorch 큰 행렬 곱셈 반복 (GPU)
a_torch = torch.randn(size, size, device='cuda' if torch.cuda.is_available() else 'cpu')
b_torch = torch.randn(size, size, device='cuda' if torch.cuda.is_available() else 'cpu')

start_torch = time.time()
for i in range(1000):
    c_torch = torch.matmul(a_torch, b_torch)
    print(f"[PyTorch] {i+1}회 연산 완료")
end_torch = time.time()

print(f"[PyTorch] 총 소요 시간: {end_torch - start_torch:.2f}초")
