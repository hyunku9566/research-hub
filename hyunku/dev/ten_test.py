import tensorflow as tf
import time

print("사용 가능한 GPU:", tf.config.list_physical_devices('GPU'))

# 큰 행렬 곱셈 반복
size = 4096
a = tf.random.normal((size, size))
b = tf.random.normal((size, size))

start = time.time()
for i in range(1000):
    c = tf.matmul(a, b)
    print(f"{i+1}회 연산 완료")
end = time.time()

print(f"총 소요 시간: {end - start:.2f}초")