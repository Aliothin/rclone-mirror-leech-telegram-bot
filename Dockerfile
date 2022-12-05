FROM maverick9099/mh:heroku

WORKDIR /usr/src/app
SHELL ["/bin/bash", "-c"]
RUN chmod 777 /usr/src/app

RUN apt-get -y update && DEBIAN_FRONTEND="noninteractive" \
    apt-get install -y python3 python3-pip p7zip-full \
    p7zip-rar ffmpeg locales curl wget git unzip libmagic-dev libcrypto++-dev libssl-dev \ 
    libc-ares-dev libcurl4-openssl-dev libsqlite3-dev libsodium-dev libfreeimage-dev libpq-dev libffi-dev  \
    && locale-gen en_US.UTF-8 && \ 
    curl https://rclone.org/install.sh | bash 
    
RUN apt -qq update --fix-missing && \
    apt -qq install -y \
    mediainfo    

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get upgrade -y

CMD ["bash","start.sh"]
