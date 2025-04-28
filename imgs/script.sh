#!/bin/bash

LOTE=100
INDICE=101 # Começar do 101 porque você já adicionou os 100 primeiros manualmente

# Enquanto ainda houver arquivos
while true
do
    arquivos=$(ls | tail -n +$INDICE | head -n $LOTE)

    # Se não tiver mais arquivos, sair do loop
    if [ -z "$arquivos" ]; then
        echo "🏁 Todos os arquivos enviados!"
        break
    fi

    git add $arquivos
    git commit -m "Added 100 files"
    git push origin main

    INDICE=$((INDICE + LOTE))
done
