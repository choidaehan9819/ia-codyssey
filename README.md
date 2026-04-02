````md
# AI-SW 개발 워크스테이션 구축 과제

## 1. 과제 개요
본 과제에서는 macOS 환경에서 터미널 기본 명령어를 실습하고, Docker를 이용하여 컨테이너 실행 및 웹 서버 구동을 수행하였다.  
또한 바인드 마운트와 Docker Volume을 통해 데이터 연결 방식과 영속성 차이를 확인하였고, Git 저장소 초기화 및 커밋을 통해 버전 관리까지 진행하였다.  
보너스 과제에서는 Docker Compose를 이용하여 멀티 컨테이너 환경을 구성하고, 컨테이너 간 네트워크 통신과 환경변수를 이용한 포트 설정을 확인하였다.

---

## 2. 수행 환경
- OS: macOS
- Docker Engine: 28.5.2
- Docker Compose: v2.40.3
- Git: 2.53.0
- Docker Context: orbstack

---

# 3. 기본 과제 수행 내용

## 3-1. 터미널 기본 명령어 실습

### 실습 목적
터미널에서 파일 및 디렉터리를 생성, 이동, 복사, 삭제하고 권한을 변경하는 기본 명령어를 익힌다.

### 수행 내용
- 작업 폴더 `ai-sw-workstation` 생성
- `README.md`, `practice`, `test.txt` 생성
- 복사/이동/삭제 및 권한 변경 실습

### 실행 명령어
```bash
pwd
ls
cd Desktop
mkdir ai-sw-workstation
cd ai-sw-workstation
touch README.md
mkdir practice
touch test.txt
cp test.txt copy.txt
mv copy.txt moved.txt
rm moved.txt
ls -la
chmod 644 test.txt
chmod 755 practice
ls -ld practice
````

### 확인 결과

* 작업 디렉터리 생성 성공
* 파일/폴더 생성, 복사, 이동, 삭제 가능 확인
* 권한 변경 명령어 정상 동작 확인

### 관련 로그 기록

```bash
dahan98199819@c4r9s6 ~ % pwd
/Users/dahan98199819
dahan98199819@c4r9s6 ~ % ls
Desktop		Downloads	Movies		OrbStack	Public
Documents	Library		Music		Pictures
dahan98199819@c4r9s6 ~ % cd Desktop
dahan98199819@c4r9s6 Desktop % mkdir ai-sw-workstation
dahan98199819@c4r9s6 Desktop % cd ai-sw-workstation
dahan98199819@c4r9s6 ai-sw-workstation % pwd
/Users/dahan98199819/Desktop/ai-sw-workstation
dahan98199819@c4r9s6 ai-sw-workstation % touch README.md
dahan98199819@c4r9s6 ai-sw-workstation % mkdir practice
dahan98199819@c4r9s6 ai-sw-workstation % touch test.txt
dahan98199819@c4r9s6 ai-sw-workstation % cp test.txt copy.txt
dahan98199819@c4r9s6 ai-sw-workstation % mv copy.txt moved.txt
dahan98199819@c4r9s6 ai-sw-workstation % rm moved.txt
dahan98199819@c4r9s6 ai-sw-workstation % ls -la
total 0
drwxr-xr-x  3 dahan98199819  dahan98199819   96  3 31 18:06 .
drwx------+ 5 dahan98199819  dahan98199819  160  3 31 18:05 ..
-rw-r--r--  1 dahan98199819  dahan98199819    0  3 31 18:06 README.md
dahan98199819@c4r9s6 ai-sw-workstation % chmod 644 test.txt
dahan98199819@c4r9s6 ai-sw-workstation % chmod 755 practice
dahan98199819@c4r9s6 ai-sw-workstation % ls -ld practice
drwxr-xr-x  2 dahan98199819  dahan98199819  64  3 31 18:14 practice
```

---

## 3-2. Docker 설치 및 동작 확인

### 실습 목적

Docker가 정상 설치되어 있는지 확인하고, 기본 테스트 컨테이너를 실행한다.

### 수행 내용

* Docker 버전 확인
* Docker 정보 확인
* `hello-world` 이미지 실행
* 이미지 목록 및 컨테이너 목록 확인

### 실행 명령어

```bash
docker --version
docker info
docker run hello-world
docker images
docker ps -a
```

### 확인 결과

* Docker 설치 정상 확인
* `hello-world` 이미지 다운로드 및 실행 완료
* `Hello from Docker!` 메시지 출력 확인

### 관련 로그 기록

```bash
dahan98199819@c4r9s6 ai-sw-workstation % docker --version
Docker version 28.5.2, build ecc6942

dahan98199819@c4r9s6 ai-sw-workstation % docker info
Client:
 Version:    28.5.2
 Context:    orbstack
 Debug Mode: false
 Plugins:
  buildx: Docker Buildx (Docker Inc.)
    Version:  v0.29.1
  compose: Docker Compose (Docker Inc.)
    Version:  v2.40.3

Server:
 Containers: 0
 Running: 0
 Paused: 0
 Stopped: 0
 Images: 0
 Server Version: 28.5.2

dahan98199819@c4r9s6 ai-sw-workstation % docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
4f55086f7dd0: Pull complete
Digest: sha256:452a468a4bf985040037cb6d5392410206e47db9bf5b7278d281f94d1c2d0931
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

dahan98199819@c4r9s6 ai-sw-workstation % docker images
REPOSITORY    TAG       IMAGE ID       CREATED      SIZE
hello-world   latest    e2ac70e7319a   7 days ago   10.1kB

dahan98199819@c4r9s6 ai-sw-workstation % docker ps -a
CONTAINER ID   IMAGE         COMMAND    CREATED          STATUS                      PORTS     NAMES
69e8465a90ec   hello-world   "/hello"   48 seconds ago   Exited (0) 48 seconds ago             romantic_hawking
```

---

## 3-3. Ubuntu 컨테이너 실행

### 실습 목적

Ubuntu 컨테이너를 실행하고 내부 쉘에 직접 진입하여 컨테이너 환경을 확인한다.

### 수행 내용

* Ubuntu 이미지 다운로드
* 컨테이너 내부 진입
* 내부 명령어 실행 후 종료

### 실행 명령어

```bash
docker run -it ubuntu bash
ls
echo hello
pwd
exit
docker ps -a
```

### 확인 결과

* Ubuntu 컨테이너 내부 진입 성공
* 컨테이너 내부에서 기본 명령어 실행 가능 확인
* 종료 후 컨테이너 상태 확인 완료

### 관련 로그 기록

```bash
dahan98199819@c4r9s6 ai-sw-workstation % docker run -it ubuntu bash
Unable to find image 'ubuntu:latest' locally
latest: Pulling from library/ubuntu
817807f3c64e: Pull complete
Digest: sha256:186072bba1b2f436cbb91ef2567abca677337cfc786c86e107d25b7072feef0c
Status: Downloaded newer image for ubuntu:latest

root@abe331f0f36d:/# ls
bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
root@abe331f0f36d:/# echo hello
hello
root@abe331f0f36d:/# pwd
/
root@abe331f0f36d:/# exit
exit

dahan98199819@c4r9s6 ai-sw-workstation % docker ps -a
CONTAINER ID   IMAGE         COMMAND    CREATED         STATUS                          PORTS     NAMES
abe331f0f36d   ubuntu        "bash"     2 minutes ago   Exited (0) About a minute ago             ecstatic_mccarthy
09aea4c99ff6   hello-world   "/hello"   3 minutes ago   Exited (0) 3 minutes ago                  friendly_brattain
69e8465a90ec   hello-world   "/hello"   4 minutes ago   Exited (0) 4 minutes ago                  romantic_hawking
```

---

## 3-4. NGINX 기반 HTML 페이지 실행

### 실습 목적

직접 작성한 HTML 파일을 NGINX 컨테이너에 포함시켜 웹 페이지가 정상적으로 출력되는지 확인한다.

### 수행 내용

* `web` 폴더 생성
* `index.html` 작성
* `Dockerfile` 작성
* NGINX 이미지 빌드 및 컨테이너 실행
* `curl`을 통해 페이지 확인

### index.html

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>AI-SW Workstation</title>
</head>
<body>
  <h1>AI/SW 개발 워크스테이션 구축 성공</h1>
  <p>Docker NGINX 컨테이너 실행 확인</p>
  <p>작성자: 최대한</p>
</body>
</html>
```

### Dockerfile

```Dockerfile
FROM nginx:latest
COPY index.html /usr/share/nginx/html/index.html
```

### 실행 명령어

```bash
docker build -t my-nginx .
docker run -d -p 8080:80 --name my-web my-nginx
docker ps
curl http://127.0.0.1:8080
```

### 확인 결과

* 작성한 HTML 페이지가 정상 출력됨
* NGINX 컨테이너 기반 웹 서버 구동 성공

### 관련 로그 기록

```bash
dahan98199819@c4r9s6 ~ % nano ~/Desktop/ai-sw-workstation/web/index.html
dahan98199819@c4r9s6 ~ % cat ~/Desktop/ai-sw-workstation/web/index.html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>AI-SW Workstation</title>
</head>
<body>
  <h1>AI/SW 개발 워크스테이션 구축 성공</h1>
  <p>Docker NGINX 컨테이너 실행 확인</p>
  <p>작성자: 최대한</p>
</body>
</html>

dahan98199819@c4r9s6 ~ % curl http://127.0.0.1:8080
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>AI-SW Workstation</title>
</head>
<body>
  <h1>AI/SW 개발 워크스테이션 구축 성공</h1>
  <p>Docker NGINX 컨테이너 실행 확인</p>
  <p>작성자: 최대한</p>
</body>
</html>
```

---

## 3-5. 바인드 마운트 실습

### 실습 목적

호스트의 웹 폴더를 컨테이너와 직접 연결하여, 파일 수정 시 실시간 반영되는지 확인한다.

### 수행 내용

* 호스트 `web` 폴더를 컨테이너 `/usr/share/nginx/html`에 연결
* HTML 수정 후 변경사항 반영 확인

### 실행 명령어

```bash
docker rm -f my-web-bind
docker run -d --name my-web-bind -p 8081:80 -v ~/Desktop/ai-sw-workstation/web:/usr/share/nginx/html nginx
docker ps
```

### 수정한 HTML

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>AI-SW Workstation</title>
</head>
<body>
  <h1>바인드 마운트 실시간 반영 성공</h1>
  <p>파일을 수정하면 컨테이너에 바로 반영됩니다.</p>
  <p>작성자: 최대한</p>
</body>
</html>
```

### 확인 결과

* 로컬 파일 수정 내용이 컨테이너 웹 페이지에 바로 반영됨
* 바인드 마운트의 실시간 반영 특성 확인

### 관련 로그 기록

```bash
dahan98199819@c4r9s6 ~ % docker rm -f my-web-bind
my-web-bind

dahan98199819@c4r9s6 ~ % docker run -d --name my-web-bind -p 8081:80 -v ~/Desktop/ai-sw-workstation/web:/usr/share/nginx/html nginx
a07f02f562f41ce291640b810e496059cafc56ef24b0f9a4e65f16f90084c700

dahan98199819@c4r9s6 ~ % docker ps
CONTAINER ID   IMAGE     COMMAND                   CREATED          STATUS          PORTS                                     NAMES
a07f02f562f4   nginx     "/docker-entrypoint.…"   25 seconds ago   Up 24 seconds   0.0.0.0:8081->80/tcp, [::]:8081->80/tcp   my-web-bind

dahan98199819@c4r9s6 ~ % cat > ~/Desktop/ai-sw-workstation/web/index.html <<'EOF'
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>AI-SW Workstation</title>
</head>
<body>
  <h1>바인드 마운트 실시간 반영 성공</h1>
  <p>파일을 수정하면 컨테이너에 바로 반영됩니다.</p>
  <p>작성자: 최대한</p>
</body>
</html>
EOF
```

---

## 3-6. Docker Volume 영속성 실습

### 실습 목적

Docker Volume을 사용하여 컨테이너를 삭제해도 데이터가 유지되는지 확인한다.

### 수행 내용

* Docker Volume 생성
* Volume 연결 컨테이너 실행
* 컨테이너 내부 HTML 작성
* 컨테이너 삭제 후 재생성하여 데이터 유지 확인

### 실행 명령어

```bash
docker volume create my-nginx-data
docker volume ls
docker run -d --name my-web-volume -p 8082:80 -v my-nginx-data:/usr/share/nginx/html nginx
docker exec -it my-web-volume sh -c 'cat > /usr/share/nginx/html/index.html << "EOF"
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Docker Volume Test</title>
</head>
<body>
  <h1>볼륨 영속성 성공</h1>
  <p>컨테이너를 삭제해도 이 페이지는 남습니다.</p>
  <p>작성자: 최대한</p>
</body>
</html>
EOF'
curl http://127.0.0.1:8082
docker rm -f my-web-volume
docker run -d --name my-web-volume2 -p 8082:80 -v my-nginx-data:/usr/share/nginx/html nginx
curl http://127.0.0.1:8082
```

### 확인 결과

* 컨테이너 삭제 후 다시 생성해도 동일한 HTML 페이지 유지
* Docker Volume의 영속성 확인 완료

### 관련 로그 기록

```bash
dahan98199819@c4r9s6 ~ % docker volume create my-nginx-data
my-nginx-data

dahan98199819@c4r9s6 ~ % docker volume ls
DRIVER    VOLUME NAME
local     my-nginx-data

dahan98199819@c4r9s6 ~ % docker run -d --name my-web-volume -p 8082:80 -v my-nginx-data:/usr/share/nginx/html nginx
358e97c04a9e471688343147863b6f16baa97985a2ccdcc15221603a3f5bb268

dahan98199819@c4r9s6 ~ % docker ps
CONTAINER ID   IMAGE     COMMAND                   CREATED          STATUS          PORTS                                     NAMES
358e97c04a9e   nginx     "/docker-entrypoint.…"   11 seconds ago   Up 11 seconds   0.0.0.0:8082->80/tcp, [::]:8082->80/tcp   my-web-volume

dahan98199819@c4r9s6 ~ % docker exec -it my-web-volume sh -c 'cat > /usr/share/nginx/html/index.html << "EOF"
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Docker Volume Test</title>
</head>
<body>
  <h1>볼륨 영속성 성공</h1>
  <p>컨테이너를 삭제해도 이 페이지는 남습니다.</p>
  <p>작성자: 최대한</p>
</body>
</html>
EOF'

dahan98199819@c4r9s6 ~ % curl http://127.0.0.1:8082
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Docker Volume Test</title>
</head>
<body>
  <h1>볼륨 영속성 성공</h1>
  <p>컨테이너를 삭제해도 이 페이지는 남습니다.</p>
  <p>작성자: 최대한</p>
</body>
</html>

dahan98199819@c4r9s6 ~ % docker rm -f my-web-volume
my-web-volume

dahan98199819@c4r9s6 ~ % docker run -d --name my-web-volume2 -p 8082:80 -v my-nginx-data:/usr/share/nginx/html nginx
e5a86b65b68c540674589508eef0d3d9b21473cbab032240ef7ae1e280b5ac98

dahan98199819@c4r9s6 ~ % curl http://127.0.0.1:8082
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Docker Volume Test</title>
</head>
<body>
  <h1>볼륨 영속성 성공</h1>
  <p>컨테이너를 삭제해도 이 페이지는 남습니다.</p>
  <p>작성자: 최대한</p>
</body>
</html>
```

---

## 3-7. Git 저장소 초기화 및 커밋

### 실습 목적

Git 사용자 정보를 설정하고 프로젝트를 버전 관리하기 위한 저장소를 초기화한다.

### 수행 내용

* Git 버전 확인
* 사용자 이름/이메일 설정
* 저장소 초기화
* 파일 추가 및 커밋
* 브랜치명을 `main`으로 변경

### 실행 명령어

```bash
git --version
git config --global user.name "최대한"
git config --global user.email "dahan9819@skuniv.ac.kr"
git config --global --list
cd ~/Desktop/ai-sw-workstation
git init
git status
git add .
git commit -m "Initial commit: AI-SW workstation setup"
git branch -m main
git status
git branch
git add README.md
git commit -m "Add README summary"
git status
```

### 확인 결과

* Git 사용자 정보 설정 완료
* 저장소 초기화 및 첫 커밋 완료
* `main` 브랜치로 변경 완료

### 관련 로그 기록

```bash
dahan98199819@c4r9s6 ~ % git --version
git version 2.53.0

dahan98199819@c4r9s6 ~ % git config --global user.name "최대한"
dahan98199819@c4r9s6 ~ % git config --global user.email "dahan9819@skuniv.ac.kr"
dahan98199819@c4r9s6 ~ % git config --global --list
user.name=최대한
user.email=dahan9819@skuniv.ac.kr

dahan98199819@c4r9s6 ~ % cd ~/Desktop/ai-sw-workstation
dahan98199819@c4r9s6 ai-sw-workstation % git init
Initialized empty Git repository in /Users/dahan98199819/Desktop/ai-sw-workstation/.git/

dahan98199819@c4r9s6 ai-sw-workstation % git status
현재 브랜치 master
아직 커밋이 없습니다

dahan98199819@c4r9s6 ai-sw-workstation % git add .
dahan98199819@c4r9s6 ai-sw-workstation % git commit -m "Initial commit: AI-SW workstation setup"
[master (root-commit) 4655712] Initial commit: AI-SW workstation setup

dahan98199819@c4r9s6 ai-sw-workstation % git branch -m main
dahan98199819@c4r9s6 ai-sw-workstation % git status
현재 브랜치 main
커밋할 사항 없음, 작업 폴더 깨끗함

dahan98199819@c4r9s6 ai-sw-workstation % git add README.md
dahan98199819@c4r9s6 ai-sw-workstation % git commit -m "Add README summary"
[main 2a2e885] Add README summary
```

---

# 4. 수행 중 어려웠던 점과 해결 과정

## 4-1. 터미널 명령어 오타

### 발생한 문제

* `pwn` 입력
* `ls-la` 입력
* `git config --globaluser.email` 입력

### 원인

터미널 명령어는 띄어쓰기와 옵션 위치가 정확해야 하므로 작은 오타도 오류를 발생시켰다.

### 해결 방법

오류 메시지를 확인하고 올바른 명령어 형식으로 다시 입력하였다.

---

## 4-2. HTML 작성 중 `DOCTYPE` 오류

### 발생한 문제

```bash
zsh: event not found: DOCTYPE
```

### 원인

zsh가 `!DOCTYPE`를 히스토리 확장으로 해석하였다.

### 해결 방법

* `nano index.html` 편집기 사용
* 또는 heredoc 문법을 정확히 사용하여 재작성

---

## 4-3. Docker Compose 포트 충돌

### 발생한 문제

```bash
Bind for 0.0.0.0:8081 failed: port is already allocated
```

### 원인

기존 바인드 마운트 실습용 컨테이너 `my-web-bind`가 이미 8081 포트를 사용 중이었다.

### 해결 방법

* Compose 포트를 다른 번호로 변경
* 이후 `.env` 파일을 사용해 `8084`로 분리하여 해결

---

# 5. 보너스 과제: Docker Compose

## 5-1. 단일 서비스 Compose 실행

### 실습 목적

Docker Compose를 이용하여 단일 NGINX 서비스를 실행한다.

### compose.yaml

```yaml
services:
  web:
    image: nginx:latest
    ports:
      - "8081:80"
```

### 실행 명령어

```bash
docker compose up -d
docker compose ps
```

### 결과 및 문제점

기존 8081 포트가 이미 사용 중이어서 실행 시 포트 충돌 오류가 발생하였다.

### 관련 로그 기록

```bash
dahan98199819@c4r9s6 bonus-compose % cat compose.yaml
services:
  web:
    image: nginx:latest
    ports:
      - "8081:80"

dahan98199819@c4r9s6 bonus-compose % docker compose up -d
[+] Running 1/2
 ✔ Network bonus-compose_default  Created
 ⠴ Container bonus-compose-web-1  Starting
Error response from daemon: failed to set up container networking: driver failed programming external connectivity on endpoint bonus-compose-web-1: Bind for 0.0.0.0:8081 failed: port is already allocated
```

---

## 5-2. 멀티 컨테이너 Compose 구성

### 실습 목적

`web`과 `helper` 두 개의 컨테이너를 동시에 실행하여 Compose 기반 멀티 컨테이너 구조를 확인한다.

### compose.yaml

```yaml
services:
  web:
    image: nginx:latest
    ports:
      - "${WEB_PORT}:80"

  helper:
    image: ubuntu:latest
    command: ["bash", "-c", "while true; do echo helper container is running; sleep 10; done"]
```

### .env

```env
WEB_PORT=8084
```

### 실행 명령어

```bash
docker compose down
docker compose up -d
docker compose ps
docker compose logs
```

### 확인 결과

* `web`, `helper` 두 컨테이너 모두 정상 실행
* `web` 서비스가 `8084` 포트로 정상 연결됨

### 관련 로그 기록

```bash
dahan98199819@c4r9s6 bonus-compose % cat > compose.yaml <<'EOF'
services:
  web:
    image: nginx:latest
    ports:
      - "${WEB_PORT}:80"

  helper:
    image: ubuntu:latest
    command: ["bash", "-c", "while true; do echo helper container is running; sleep 10; done"]
EOF

dahan98199819@c4r9s6 bonus-compose % cat > .env <<'EOF'
WEB_PORT=8084
EOF

dahan98199819@c4r9s6 bonus-compose % docker compose down
docker compose up -d
docker compose ps

[+] Running 3/3
 ✔ Container bonus-compose-web-1     Removed
 ✔ Container bonus-compose-helper-1  Removed
 ✔ Network bonus-compose_default     Removed

[+] Running 3/3
 ✔ Network bonus-compose_default     Created
 ✔ Container bonus-compose-helper-1  Started
 ✔ Container bonus-compose-web-1     Started

NAME                     IMAGE           COMMAND                   SERVICE   CREATED        STATUS                  PORTS
bonus-compose-helper-1   ubuntu:latest   "bash -c 'while true…"   helper    1 second ago   Up Less than a second
bonus-compose-web-1      nginx:latest    "/docker-entrypoint.…"   web       1 second ago   Up Less than a second   0.0.0.0:8084->80/tcp, [::]:8084->80/tcp
```

---

## 5-3. 컨테이너 간 네트워크 통신 확인

### 실습 목적

Compose 환경에서 서비스 이름으로 다른 컨테이너에 접근 가능한지 확인한다.

### 수행 내용

* `helper` 컨테이너에서 `curl` 설치
* `curl http://web` 실행

### 실행 명령어

```bash
docker compose exec helper bash
apt update && apt install -y curl
curl http://web
exit
```

### 확인 결과

* `helper` 컨테이너가 `web` 서비스를 이름으로 인식
* NGINX 기본 페이지 응답 확인
* Compose 내부 네트워크 정상 동작 확인

### 관련 로그 기록

```bash
Setting up curl (8.5.0-2ubuntu10.8) ...
Processing triggers for libc-bin (2.39-0ubuntu8.7) ...
Processing triggers for ca-certificates (20240203) ...
Updating certificates in /etc/ssl/certs...
0 added, 0 removed; done.
Running hooks in /etc/ca-certificates/update.d...
done.
root@fbfae37a555c:/# curl http://web
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, nginx is successfully installed and working.</p>
<p><em>Thank you for using nginx.</em></p>
</body>
</html>
root@fbfae37a555c:/# exit
exit
```

---

## 5-4. 브라우저 접속 확인

### 실습 목적

호스트 브라우저에서 Compose 웹 서버가 정상적으로 열리는지 확인한다.

### 접속 주소

```text
http://localhost:8084
```

### 확인 결과

* 브라우저에서 `Welcome to nginx!` 페이지가 정상 출력됨
* 이는 오류가 아니라 NGINX 공식 이미지가 정상 동작 중이라는 의미임

### 관련 로그 기록

```text
Welcome to nginx!

If you see this page, nginx is successfully installed and working.

Thank you for using nginx.
```

---

# 6. 최종 결과 정리

## 기본 과제 완료 항목

* 터미널 기본 명령어 실습 완료
* Docker 설치 및 동작 확인 완료
* `hello-world` 실행 완료
* Ubuntu 컨테이너 실행 완료
* NGINX 기반 HTML 페이지 실행 완료
* 바인드 마운트 실습 완료
* Docker Volume 영속성 실습 완료
* Git 저장소 초기화 및 커밋 완료

## 보너스 과제 완료 항목

* Docker Compose 단일 서비스 실행 완료
* 포트 충돌 문제 확인 및 해결 완료
* Docker Compose 멀티 컨테이너 실행 완료
* `helper -> web` 내부 네트워크 통신 확인 완료
* `.env` 환경변수를 통한 포트 설정 완료
* 브라우저에서 `localhost:8084` 접속 확인 완료

---

# 7. 이번 과제를 통해 배운 점

이번 실습을 통해 터미널 기본 사용법, Docker 이미지와 컨테이너의 개념, 포트 매핑, 바인드 마운트와 Volume의 차이, Git 버전 관리, Docker Compose 기반 멀티 컨테이너 구성까지 직접 확인할 수 있었다.
특히 오류를 직접 해결하는 과정에서 명령어 문법의 중요성, 포트 충돌 원인, 컨테이너 내부 네트워크 구조를 더 명확히 이해하게 되었다.

---

# 8. 작성자

최대한
