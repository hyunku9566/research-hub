# Windows WSL 환경 GPU 설정 가이드

## 개요
- **환경**: Windows WSL 환경에서 GPU 활용 2060super
- **목적**: TensorFlow 2.13 활용을 위한 Python 3.9 이상 환경 구성
- **주요 구성요소**: CUDA, cuDNN, TensorFlow, PyTorch

## 1. Python 환경 설정

### Conda 가상환경 생성
```bash
conda create -n aiot-gpu python=3.9 -y
conda activate aiot-gpu
```

## 2. NVIDIA 드라이버 및 CUDA 설치

### 2.1 저장소 Pin 파일 등록
```bash
# 1) 저장소 Pin 파일 등록
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-wsl-ubuntu.pin
sudo mv cuda-wsl-ubuntu.pin /etc/apt/preferences.d/cuda-repository-pin-600
```

### 2.2 로컬 설치 패키지 다운로드 및 등록
```bash
# 2) 로컬 설치 패키지 다운로드 및 등록
wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda-repo-wsl-ubuntu-11-8-local_11.8.0-1_amd64.deb
sudo dpkg -i cuda-repo-wsl-ubuntu-11-8-local_11.8.0-1_amd64.deb
```

### 2.3 GPG 키 복사 및 시스템 업데이트
```bash
# 3) GPG 키 복사 및 업데이트
sudo cp /var/cuda-repo-wsl-ubuntu-11-8-local/cuda-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
```

### 2.4 CUDA Toolkit 설치
```bash
# 4) CUDA Toolkit 설치 (드라이버 제외)
sudo apt-get install -y cuda-toolkit-11-8
```

## 3. cuDNN 설치

### 3.1 필수 의존성 설치
```bash
# 홈 디렉토리로 이동
cd ~  

# 패키지 리스트 갱신
sudo apt update  

# libtinfo5 다운로드 및 설치
wget http://security.ubuntu.com/ubuntu/pool/universe/n/ncurses/libtinfo5_6.3-2ubuntu0.1_amd64.deb  
ls -lh libtinfo5_6.3-2ubuntu0.1_amd64.deb  
sudo apt install ./libtinfo5_6.3-2ubuntu0.1_amd64.deb  

# zlib1g 의존성 설치
sudo apt-get install -y zlib1g
```

### 3.2 cuDNN 라이브러리 설치
```bash
# tarball 압축 해제
tar -xvf cudnn-linux-x86_64-8.6.0.163_cuda11-archive.tar.xz

# 헤더 및 라이브러리 복사
sudo cp cudnn-*-archive/include/cudnn*.h /usr/local/cuda/include
sudo cp -P cudnn-*-archive/lib/libcudnn* /usr/local/cuda/lib64
sudo chmod a+r /usr/local/cuda/include/cudnn*.h /usr/local/cuda/lib64/libcudnn*
```

## 4. 환경변수 설정

### 4.1 라이브러리 경로 설정
```bash
# WSL 내부 libcuda 위치 우선
echo 'export LD_LIBRARY_PATH=/usr/lib/wsl/lib:$LD_LIBRARY_PATH' >> ~/.bashrc

# CUDA bin 경로 추가 (선택사항)
echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.bashrc

# 설정 적용
source ~/.bashrc
sudo ldconfig
```

## 5. 머신러닝 프레임워크 설치

### 5.1 TensorFlow 설치
```bash
pip install --upgrade pip
pip install tensorflow==2.13.*
```

### 5.2 PyTorch 설치

#### 방법 1: 기본 설치
```bash
conda install pytorch torchvision torchaudio cudatoolkit=11.8 -c pytorch
```

#### 방법 2: 채널 우선순위 조정 후 설치
```bash
conda config --set channel_priority flexible
conda install pytorch torchvision torchaudio cudatoolkit=11.8 -c pytorch -c nvidia
```

## 6. 설치 검증

### CUDA 및 PyTorch GPU 사용 가능 여부 확인
```bash
python - <<EOF
import torch
print(torch.cuda.is_available())
EOF
```

## 주의사항
- WSL 환경에서는 Windows에 설치된 NVIDIA 드라이버를 공유하므로, WSL 내부에서 별도의 드라이버 설치는 불필요
- CUDA 버전과 cuDNN 버전 호환성 확인 필요
- TensorFlow 2.13은 CUDA 11.8과 호환됨 