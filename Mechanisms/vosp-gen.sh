#!/bin/bash

# Проверяем, передано ли имя компонента
if [ -z "$1" ]; then
    echo "Ошибка: Укажите имя компонента."
    echo "Использование: ./vosp-gen.sh MyNewComponent"
    exit 1
fi

# Превращаем имя в чистый snake-case для названия файлов
# (Заменяет CamelCase и пробелы на дефисы в нижнем регистре)
COMPONENT_INPUT=$1
COMPONENT_NAME=$(echo "$COMPONENT_INPUT" | sed -r 's/([A-Z])/-\1/g' | sed 's/^-//' | sed 's/[ _]/-/.../g' | tr '[:upper:]' '[:lower:]' | sed 's/--/-/g')

# Создаем структуру 6 папок согласно struct.md
mkdir -p "$COMPONENT_INPUT/schemes"
mkdir -p "$COMPONENT_INPUT/prototypes"
mkdir -p "$COMPONENT_INPUT/intermodule"
mkdir -p "$COMPONENT_INPUT/content"
mkdir -p "$COMPONENT_INPUT/structs"
mkdir -p "$COMPONENT_INPUT/specs"

# Генерируем базовые заготовки файлов по правилам snake-case
touch "$COMPONENT_INPUT/schemes/architecture-map.svg"
touch "$COMPONENT_INPUT/schemes/logic-flow.pseudo"
touch "$COMPONENT_INPUT/schemes/test-matrix.md"

echo "/* Компонент: $COMPONENT_INPUT */" > "$COMPONENT_INPUT/prototypes/$COMPONENT_NAME.hpp"
echo "/* Реализация: $COMPONENT_INPUT */" > "$COMPONENT_INPUT/structs/$COMPONENT_NAME.cpp"

echo "✓ Структура для компонента '$COMPONENT_INPUT' успешно создана!"
echo "  Имена файлов зафиксированы в стиле snake-case: $COMPONENT_NAME.hpp / .cpp"
