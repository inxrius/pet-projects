import sys
from mistralai import Mistral

def read_file(filename: str) -> str:
    """Читает содержимое файла и возвращает строку без лишних пробелов по краям."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден.")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при чтении файла '{filename}': {e}")
        sys.exit(1)

def main():
    # Пути к файлам (при необходимости измените)
    api_key_file = "api_key.txt"
    prompt_file = "prompt.txt"
    output_file = "response.txt"

    # 1. Читаем API-ключ
    api_key = read_file(api_key_file)
    if not api_key:
        print("Ошибка: файл с API-ключом пуст.")
        sys.exit(1)

    # 2. Читаем промпт
    prompt = read_file(prompt_file)
    if not prompt:
        print("Ошибка: файл с промптом пуст.")
        sys.exit(1)

    # 3. Инициализируем клиент Mistral
    client = Mistral(api_key=api_key)

    # Модель (можно заменить, например, на "open-mistral-nemo" для бесплатного тарифа)
    model = "mistral-small-latest"

    messages = [
        {"role": "user", "content": prompt}
    ]

    try:
        # Отправляем запрос
        response = client.chat.complete(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )

        # Извлекаем текст ответа
        answer = response.choices[0].message.content

        # 3. Записываем ответ в файл
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(answer)

        print(f"Ответ успешно записан в файл '{output_file}'.")

    except Exception as e:
        print(f"Произошла ошибка при обращении к API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
