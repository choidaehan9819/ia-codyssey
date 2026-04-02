````md
# AI-SW 개발 워크스테이션 구축 과제

## 1. 과제 개요
이번 과제에서는 macOS 환경에서 터미널 기본 명령어를 익히고, Docker를 활용하여 컨테이너 실행 및 웹 서버 구동을 실습하였다.  
또한 바인드 마운트와 Docker Volume을 비교하며 데이터 반영 방식과 영속성 차이를 확인했고, 마지막으로 Git 저장소를 초기화하여 작업 내용을 관리하였다.  
보너스 과제에서는 Docker Compose를 이용해 멀티 컨테이너 환경을 구성하고, 컨테이너 간 네트워크 통신과 환경변수 기반 포트 설정까지 확인하였다.

---

## 2. 수행 환경
- OS: macOS
- Docker Engine: 28.5.2
- Docker Compose: v2.40.3
- Git: 2.53.0
- Docker Context: orbstack

---

## 3. 기본 과제 수행 내용

### 3-1. 터미널 기본 명령어 실습
프로젝트 폴더를 생성하고, 파일과 디렉터리를 다루는 기본 명령어를 실습하였다.

#### 사용한 명령어
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

#### 배운 점

* `pwd`: 현재 위치 확인
* `ls`, `ls -la`: 파일 및 디렉터리 목록 확인
* `mkdir`, `touch`: 폴더와 파일 생성
* `cp`, `mv`, `rm`: 복사, 이동, 삭제
* `chmod`: 파일 및 디렉터리 권한 변경

---

### 3-2. Docker 설치 및 동작 확인

Docker가 정상적으로 설치되어 있는지 확인하였다.

```bash
docker --version
docker info
```

그 후 가장 기본적인 테스트용 컨테이너인 `hello-world`를 실행하였다.

```bash
docker run hello-world
docker images
docker ps -a
```

#### 확인 결과

* Docker 이미지가 정상적으로 다운로드됨
* 컨테이너가 생성되고 실행됨
* `Hello from Docker!` 메시지를 통해 Docker 엔진이 정상 동작함을 확인함

---

### 3-3. Ubuntu 컨테이너 실행

Ubuntu 이미지를 실행하여 컨테이너 내부에 직접 들어가 보았다.

```bash
docker run -it ubuntu bash
```

컨테이너 내부에서 다음 명령어를 실행하였다.

```bash
ls
echo hello
pwd
exit
```

#### 배운 점

* `-it` 옵션을 이용하면 컨테이너 내부 쉘에 직접 들어갈 수 있음
* 컨테이너는 독립된 실행 환경이라는 것을 확인함

---

### 3-4. NGINX 기반 HTML 페이지 실행

`web` 폴더를 만들고 `index.html`, `Dockerfile`을 작성하였다.

#### index.html

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

#### Dockerfile

```Dockerfile
FROM nginx:latest
COPY index.html /usr/share/nginx/html/index.html
```

#### 이미지 빌드 및 컨테이너 실행

```bash
docker build -t my-nginx .
docker run -d -p 8080:80 --name my-web my-nginx
docker ps
curl http://127.0.0.1:8080
```

#### 확인 결과

* `localhost:8080` 또는 `curl`로 접속 시 직접 작성한 HTML 페이지가 출력됨
* Docker 이미지 빌드와 컨테이너 기반 웹 서버 실행 과정을 확인함

---

### 3-5. 바인드 마운트 실습

호스트의 `web` 폴더를 컨테이너 내부의 HTML 경로와 연결하여 바인드 마운트를 실습하였다.

```bash
docker rm -f my-web-bind
docker run -d --name my-web-bind -p 8081:80 -v ~/Desktop/ai-sw-workstation/web:/usr/share/nginx/html nginx
docker ps
```

그 후 `index.html`을 수정하여 다음 내용을 넣었다.

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

#### 확인 결과

* 호스트의 HTML 파일을 수정하자 컨테이너 웹 페이지에 바로 반영됨
* 바인드 마운트는 로컬 폴더와 컨테이너 폴더를 직접 연결하는 방식임을 이해함

---

### 3-6. Docker Volume 영속성 실습

Docker Volume을 생성하고, 컨테이너에 연결하여 영속성을 확인하였다.

#### Volume 생성

```bash
docker volume create my-nginx-data
docker volume ls
```

#### Volume 연결 컨테이너 실행

```bash
docker run -d --name my-web-volume -p 8082:80 -v my-nginx-data:/usr/share/nginx/html nginx
docker ps
```

#### 컨테이너 내부에 HTML 작성

```bash
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
```

#### 실행 확인

```bash
curl http://127.0.0.1:8082
```

#### 컨테이너 삭제 후 재실행

```bash
docker rm -f my-web-volume
docker run -d --name my-web-volume2 -p 8082:80 -v my-nginx-data:/usr/share/nginx/html nginx
curl http://127.0.0.1:8082
```

#### 확인 결과

* 컨테이너를 삭제하고 다시 만들어도 같은 HTML 페이지가 유지됨
* Docker Volume은 컨테이너 외부에 데이터를 저장하여 영속성을 보장함

---

### 3-7. Git 저장소 초기화 및 커밋

Git을 설치 확인하고 사용자 정보를 등록한 뒤 저장소를 초기화하였다.

```bash
git --version
git config --global user.name "최대한"
git config --global user.email "dahan9819@skuniv.ac.kr"
git config --global --list
```

#### 저장소 초기화 및 커밋

```bash
cd ~/Desktop/ai-sw-workstation
git init
git status
git add .
git commit -m "Initial commit: AI-SW workstation setup"
git branch -m main
git status
git branch
```

#### README 추가 후 커밋

```bash
git add README.md
git commit -m "Add README summary"
git status
```

#### 배운 점

* Git으로 프로젝트 이력을 관리할 수 있음
* `init`, `add`, `commit`, `branch -m` 의 기본 흐름을 익힘

---

## 4. 수행 중 어려웠던 점과 해결 과정

### 4-1. 터미널 명령어 오타

실습 중 다음과 같은 오타가 있었다.

* `pwn` → `pwd`
* `ls-la` → `ls -la`
* `git config --globaluser.email ...` → `git config --global user.email ...`

#### 느낀 점

터미널은 띄어쓰기와 옵션 순서가 매우 중요하다는 점을 알게 되었다.

---

### 4-2. HTML 작성 중 `DOCTYPE` 오류

처음 `cat > index.html <<EOF` 방식으로 HTML을 입력할 때 아래와 같은 오류가 발생하였다.

```bash
zsh: event not found: DOCTYPE
```

#### 원인

* zsh가 `!DOCTYPE`를 특수 문자로 해석했기 때문

#### 해결 방법

* `nano index.html`로 직접 수정
* 또는 heredoc 문법을 정확히 사용하여 다시 작성

---

### 4-3. Docker Compose 포트 충돌

보너스 과제에서 처음 `8081:80`으로 설정했지만 다음 오류가 발생하였다.

```bash
Bind for 0.0.0.0:8081 failed: port is already allocated
```

#### 원인

* 기존 `my-web-bind` 컨테이너가 이미 8081 포트를 사용 중이었음

#### 해결 방법

* Compose 포트를 다른 번호로 변경
* 이후 `.env` 파일을 사용해 8084 포트로 분리

#### 배운 점

* 같은 호스트 포트는 동시에 하나의 컨테이너만 사용할 수 있음

---

## 5. 보너스 과제: Docker Compose

### 5-1. 단일 서비스 실행

`bonus-compose` 폴더를 만든 뒤 `compose.yaml` 파일을 작성하였다.

```yaml
services:
  web:
    image: nginx:latest
    ports:
      - "8083:80"
```

#### 실행 명령

```bash
docker compose up -d
docker compose ps
docker compose down
```

#### 확인 결과

* Compose를 이용해 단일 웹 서비스를 실행할 수 있음을 확인함

---

### 5-2. 멀티 컨테이너 구성

다음으로 `web`과 `helper` 두 개의 서비스를 구성하였다.

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

`.env` 파일은 다음과 같이 작성하였다.

```env
WEB_PORT=8084
```

#### 실행 명령

```bash
docker compose down
docker compose up -d
docker compose ps
docker compose logs
```

---

### 5-3. 컨테이너 간 네트워크 확인

`helper` 컨테이너 안에서 `curl`을 설치한 뒤 `web` 서비스에 접근하였다.

```bash
docker compose exec helper bash
apt update && apt install -y curl
curl http://web
exit
```

#### 확인 결과

* `Welcome to nginx!` 페이지가 정상적으로 출력됨
* 이는 `helper` 컨테이너가 `web` 컨테이너를 서비스 이름으로 찾았다는 뜻임
* 즉, Docker Compose 내부 네트워크가 정상 동작함을 확인함

---

### 5-4. 브라우저 접속 확인

브라우저에서 아래 주소로 접속하였다.

```bash
http://localhost:8084
```

#### 확인 결과

* `Welcome to nginx!` 기본 페이지가 출력됨
* 이는 오류가 아니라 nginx 공식 이미지가 정상 실행되고 있다는 의미임
* 포트 매핑과 Compose 설정이 올바르게 적용되었음을 확인함

---

## 6. 최종 결과 정리

### 기본 과제 완료 항목

* 터미널 기본 명령어 실습
* Docker 설치 및 실행 확인
* `hello-world` 실행
* Ubuntu 컨테이너 실행
* NGINX 기반 HTML 페이지 실행
* 바인드 마운트 실습
* Docker Volume 영속성 실습
* Git 저장소 초기화 및 커밋

### 보너스 과제 완료 항목

* Docker Compose 단일 서비스 실행
* Docker Compose 멀티 컨테이너 실행
* `helper -> web` 내부 네트워크 통신 확인
* `docker compose up -d`, `ps`, `logs`, `down` 명령 사용
* `.env` 환경변수로 포트 변경
* `localhost:8084` 접속 확인

---

## 7. 이번 과제를 통해 배운 점

이번 실습을 통해 터미널 기본 사용법부터 Docker 컨테이너 실행, 웹 서버 구동, 바인드 마운트와 Volume의 차이, Git 버전 관리, Docker Compose를 이용한 멀티 컨테이너 구성까지 직접 경험할 수 있었다.
특히 오류를 직접 해결하는 과정에서 명령어 문법, 포트 충돌 원인, 컨테이너 내부 네트워크 구조를 더 잘 이해하게 되었다.

---

## 8. 작성자

최대한

```
```
