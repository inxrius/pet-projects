import sys
import ollama

def read_file(filename: str) -> str:
    """Читает содержимое файла и возвращает строку."""
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
    # Пути к файлам
    prompt_file = "prompt.txt"
    output_file = "response.txt"

    # Читаем промпт
    prompt = read_file(prompt_file)
    if not prompt:
        print("Ошибка: файл с промптом пуст.")
        sys.exit(1)

    # Модель, которую используем (замените при необходимости)
    model = "mistral"  # или "mistral-small:24b-instruct-2503"

    # Сообщения для модели
    messages = [
        {"role": "user", "content": prompt}
    ]

    try:
        # Отправляем запрос в Ollama
        response = ollama.chat(
            model=model,
            messages=messages,
            options={
                "temperature": 0.7,
                "num_predict": 1000  # аналог max_tokens
            }
        )

        # Извлекаем ответ
        answer = response["message"]["content"]

        # Записываем ответ в файл
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(answer)

        print(f"Ответ успешно записан в файл '{output_file}'.")

    except Exception as e:
        print(f"Произошла ошибка при обращении к Ollama: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()