sudo groupadd  --system webapps
sudo useradd --system --gid webapps --shell /bin/bash  --home /webapps
cp -r petnet root@146.227.67:/webapp 