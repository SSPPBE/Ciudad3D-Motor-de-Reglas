#Install
sudo yum update -y
sudo yum groupinstall 'Development Tools' -y
sudo yum install sqlite-devel.x86_64 -y
sudo yum install git -y
sudo yum install python39 -y
sudo yum install libpq-devel -y
sudo yum install python39-devel.x86_64 -y

mkdir -p ~/third/src/
cd ~/third/src
git clone https://github.com/mapbox/tippecanoe.git
cd ~/third/src/tippecanoe
make -j
make install
