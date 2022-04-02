sudo apt update -y
sudo apt upgrade -y
sudo apt install gunicorn python3-pip -y
pip3 install Flask flask-sqlalchemy flask_session simple-websocket
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080
sudo iptables -t nat -I OUTPUT -p tcp -d 127.0.0.1 --dport 80 -j REDIRECT --to-ports 8080
