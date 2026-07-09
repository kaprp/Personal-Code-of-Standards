#!/usr/bin/env python3
import os
import sys

# Расширения файлов, которые подлежат обязательной проверке
TARGET_EXTENSIONS = {
    '.hpp', '.cpp', '.h', '.cc',  # C++
    '.java',                       # Java
    '.py'                          # Python
}

# Суффиксы, которые исключаются из проверки (чтобы не проверять сами тесты и примеры)
EXCLUDE_SUFFIXES = {'.test', '.example'}

def collect_project_files():
    """Собирает карту всех файлов в проекте для быстрого глобального поиска"""
    all_files = set()
    for root, _, files in os.walk('.'):
        # Пропускаем скрытые папки (например, .git, .idea, __pycache__)
        if any(part.startswith('.') for part in root.split(os.sep)):
            continue
        for file in files:
            # Сохраняем имя файла в нижнем регистре для корректного поиска
            all_files.add(file.lower())
    return all_files

def check_vosp_rules():
    has_errors = False
    
    # 1. Строим карту всех существующих файлов в репозитории
    project_files_pool = collect_project_files()
    
    # 2. Проверяем каждый исходный файл на наличие глобальных дубликатов
    for root, _, files in os.walk('.'):
        if any(part.startswith('.') for part in root.split(os.sep)):
            continue
            
        for file in files:
            name, ext = os.path.splitext(file)
            ext_lower = ext.lower()
            
            # Проверяем только целевые языки программирования
            if ext_lower not in TARGET_EXTENSIONS:
                continue
                
            # Проверяем, не является ли файл сам по себе тестом или примером
            sub_name, sub_ext = os.path.splitext(name.lower())
            if sub_ext in EXCLUDE_SUFFIXES:
                continue
                
            # Формируем целевые имена файлов для поиска в проекте
            expected_test_file = f"{name.lower()}.test{ext_lower}"
            expected_example_file = f"{name.lower()}.example{ext_lower}"
            
            # Ищем файлы примеров и тестов по всему пулу файлов проекта
            if expected_test_file not in project_files_pool:
                print(f"❌ Ошибка VOSP: Для файла '{os.path.join(root, file)}' в проекте отсутствует файл тестов '{expected_test_file}'")
                has_errors = True
                
            if expected_example_file not in project_files_pool:
                print(f"❌ Ошибка VOSP: Для файла '{os.path.join(root, file)}' в проекте отсутствует файл примеров '{expected_example_file}'")
                has_errors = True

    if has_errors:
        print("\n🛑 Валидация провалена: найдены файлы без обязательных тестов или примеров в структуре проекта.")
        sys.exit(1)
    else:
        print("✅ Валидация успешна: все исходные файлы укомплектованы тестами и примерами в репозитории!")
        sys.exit(0)

if __name__ == '__main__':
    check_vosp_rules()
