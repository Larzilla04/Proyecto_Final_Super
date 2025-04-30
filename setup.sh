#!/bin/bash
echo "Actualizando sistema..."
sudo apt update && sudo apt upgrade -y

echo "Instalando paquetes esenciales..."
sudo apt install -y git vim docker.io python3 python3-pip

echo "Agregando usuario al grupo docker..."
sudo usermod -aG docker $USER
echo "Listo. Reinicia sesión o ejecuta 'newgrp docker'"

echo "Instalando dependencias de Python..."
pip3 install -r requirements.txt
