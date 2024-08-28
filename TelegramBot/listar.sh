if [ -f peliculas.txt ]; then
    rm peliculas.txt
fi

if [ -f series.txt ]; then
    rm series.txt
fi

python listar.py

while [ ! -f peliculas.txt ] || [ ! -f series.txt ]; do
    sleep 1
done

mv peliculas.txt /volume1/Programacion/Coleccion/TelegramBot/
mv series.txt /volume1/Programacion/Coleccion/TelegramBot/

echo "Los archivos peliculas.txt y series.txt han sido creados."
