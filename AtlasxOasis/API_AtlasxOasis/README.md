se connecter au vpn terminal:
sudo openconnect sslvpn.univ-lyon1.fr &


se connecter au serveur:
ssh -i clé_perso.pem p2109987@192.168.75.76

dans un .env:
DATABASE_URL=postgresql://user:password@localhost:5432/ma_db
