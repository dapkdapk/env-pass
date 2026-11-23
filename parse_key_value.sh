#!/bin/bash

# Mehrzeiliger String mit Schlüssel-Wert-Paaren (getrennt durch ':')
config_data="name:Max
age:30
city:Berlin
country:Germany
job:Engineer"

echo "Originaler String:"
echo "$config_data"
echo ""

# Methode 1: Iteration über die Zeilen und Extraktion von Schlüssel und Wert
echo "Methode 1 - Direkte Zuweisung zu Variablen:"
while IFS=':' read -r key value; do
    # Entferne mögliche Leerzeichen am Anfang/Ende
    key=$(echo "$key" | xargs)
    value=$(echo "$value" | xargs)
    
    # Weise den Wert entsprechenden Variablen zu
    case "$key" in
        "name")
            user_name="$value"
            echo "Variable user_name wurde auf '$user_name' gesetzt"
            ;;
        "age")
            user_age="$value"
            echo "Variable user_age wurde auf '$user_age' gesetzt"
            ;;
        "city")
            user_city="$value"
            echo "Variable user_city wurde auf '$user_city' gesetzt"
            ;;
        "country")
            user_country="$value"
            echo "Variable user_country wurde auf '$user_country' gesetzt"
            ;;
        "job")
            user_job="$value"
            echo "Variable user_job wurde auf '$user_job' gesetzt"
            ;;
    esac
done <<< "$config_data"

echo ""
echo "Zugriff auf die neu zugewiesenen Variablen:"
echo "Name: $user_name"
echo "Alter: $user_age"
echo "Stadt: $user_city"
echo "Land: $user_country"
echo "Beruf: $user_job"

echo ""
echo "----------------------------------------"
echo ""

# Methode 2: Dynamische Erstellung von Variablen
echo "Methode 2 - Dynamische Erstellung von Variablen:"
while IFS=':' read -r key value; do
    # Entferne mögliche Leerzeichen am Anfang/Ende
    key=$(echo "$key" | xargs)
    value=$(echo "$value" | xargs)
    
    # Erstelle dynamisch benannte Variablen
    declare "$key"="$value"
    echo "Variable $key wurde auf '${!key}' gesetzt"
done <<< "$config_data"

echo ""
echo "Zugriff auf die dynamisch erstellten Variablen:"
echo "Name: $name"
echo "Alter: $age"
echo "Stadt: $city"
echo "Land: $country"
echo "Beruf: $job"