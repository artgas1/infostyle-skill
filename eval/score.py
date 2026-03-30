#!/usr/bin/env python3
"""
Mechanical eval scorer for /infostyle skill.
Analogous to Karpathy's train.py — outputs a single number.

Usage:
    python eval/score.py eval/outputs/        # Score all output files
    python eval/score.py eval/outputs/case1.md # Score single file

Each output file should contain the skill's response for a test case.
File naming: case{N}.md (matches test case number from test-cases.md)

Output: single number 0-100 (percentage of passed criteria)
"""

import sys
import re
from pathlib import Path

# Стоп-слова для механической проверки (критерий 1)
STOP_WORDS = [
    "очень", "максимально", "уникальный", "уникальная", "уникальное",
    "качественный", "качественная", "качественное", "качественных",
    "инновационный", "инновационная", "инновационное",
    "передовой", "передовая", "передовые", "передовых",
    "высококвалифицированный", "высококвалифицированных",
    "данный", "данная", "данное", "данного",
    "является", "являются", "являясь",
    "осуществлять", "осуществляет", "осуществляем", "осуществление",
    "индивидуальный подход", "команда профессионалов",
    "широкий ассортимент", "динамично развивающ",
    "высокий уровень сервиса", "выгодные условия",
    "комплексные решения", "лидирующий поставщик",
    "клиентоориентированный", "оптимальное соотношение",
]

# Ключевые сущности по кейсам (критерий 6 — смысл сохранён)
CASE_ENTITIES = {
    1: ["презентац", "образовательн", "мебел", "решени"],  # corporate description
    2: ["отправ", "заявк"],  # UI button
    3: ["ошибк", "загруз", "попроб"],  # error message
    4: ["презентац", "слайд"],  # landing hero
    5: ["функц", "работ", "предложен"],  # email
    6: ["оформ", "заказ", "цен", "преподавател"],  # feedback form
    7: ["проект"],  # empty state
    8: ["удали", "проект"],  # confirmation modal
    9: ["готов", "презентац", "скача", "работ", "результат"],  # push notification
    10: ["ответственност", "сервис", "пользовател"],  # legal text
}


def check_criterion_1(text: str) -> bool:
    """Стоп-слова убраны?"""
    text_lower = text.lower()
    for word in STOP_WORDS:
        if word.lower() in text_lower:
            return False
    return True


def check_criterion_2(text: str, original_word_count: int, case_num: int) -> bool:
    """Пустоты заполнены? Результат не короче 60% оригинала.
    Исключение: UI кнопки (case 2), пуш (case 9) — краткость цель."""
    if case_num in (2, 9):
        return True  # auto-pass for brevity-focused types

    # Считаем слова в секции "Отредактированный текст"
    edited = extract_edited_text(text)
    if not edited:
        return False

    edited_words = len(edited.split())
    min_words = int(original_word_count * 0.6)
    return edited_words >= min_words


def check_criterion_3(text: str, case_num: int) -> bool:
    """Есть конкретика? Хотя бы одна цифра или единица измерения."""
    if case_num == 10:
        # Юридический текст — цифры в мета-ноте тоже считаются
        pass
    edited = extract_edited_text(text)
    if not edited:
        edited = text
    return bool(re.search(r'\d', edited))


def check_criterion_4(text: str) -> bool:
    """Контекст определён? Есть блок с типом текста."""
    return bool(
        re.search(r'[Тт]ип[:\s]', text) or
        re.search(r'[Аа]удитория[:\s]', text) or
        re.search(r'[Кк]онтекст', text)
    )


def check_criterion_5(text: str) -> bool:
    """Формат вывода соблюдён? Все обязательные блоки."""
    has_score_before = bool(re.search(r'[Яя]сность[:\s]*\d', text))
    has_edited = bool(
        re.search(r'[Оо]тредактированный текст', text) or
        re.search(r'[Пп]осле', text)
    )
    has_changes = bool(
        re.search(r'[Чч]то изменилось', text) or
        re.search(r'[Ии]зменени', text) or
        re.search(r'[Пп]очему', text)
    )
    return has_score_before and has_edited and has_changes


def check_criterion_6(text: str, case_num: int) -> bool:
    """Смысл сохранён? Ключевые сущности оригинала в результате."""
    entities = CASE_ENTITIES.get(case_num, [])
    if not entities:
        return True

    text_lower = text.lower()
    found = sum(1 for e in entities if e.lower() in text_lower)
    # Хотя бы половина ключевых сущностей должна присутствовать
    return found >= len(entities) / 2


def check_criterion_7(text: str, case_num: int) -> bool:
    """Юридический текст не тронут? (только для кейса 10)"""
    if case_num != 10:
        return True  # auto-pass for non-legal cases

    # Должен быть отказ/предупреждение ИЛИ минимальные изменения
    has_warning = bool(
        re.search(r'юрист', text.lower()) or
        re.search(r'юридич', text.lower()) or
        re.search(r'не применя', text.lower()) or
        re.search(r'не рекоменд', text.lower()) or
        re.search(r'правки не применены', text.lower()) or
        re.search(r'точность', text.lower())
    )
    return has_warning


def extract_edited_text(text: str) -> str:
    """Извлечь секцию 'Отредактированный текст' из вывода."""
    # Ищем блок между "Отредактированный текст" и следующим ##
    match = re.search(
        r'##\s*[Оо]тредактированный текст\s*\n(.*?)(?=\n##|\Z)',
        text, re.DOTALL
    )
    if match:
        return match.group(1).strip()

    # Альтернативный формат — блок "После"
    match = re.search(
        r'[Пп]осле[:\s]*\n```?\n?(.*?)```?',
        text, re.DOTALL
    )
    if match:
        return match.group(1).strip()

    return ""


# Количество слов в оригинальных текстах (из test-cases.md)
ORIGINAL_WORD_COUNTS = {
    1: 22,  # corporate description
    2: 8,   # UI button
    3: 18,  # error message
    4: 21,  # landing hero
    5: 30,  # email
    6: 25,  # feedback form
    7: 5,   # empty state
    8: 16,  # confirmation modal
    9: 17,  # push notification
    10: 20, # legal text
}


def score_file(filepath: Path) -> dict:
    """Score a single output file. Returns dict of criterion -> pass/fail."""
    text = filepath.read_text(encoding='utf-8')

    # Extract case number from filename
    match = re.search(r'case(\d+)', filepath.name)
    if not match:
        return {}
    case_num = int(match.group(1))

    original_words = ORIGINAL_WORD_COUNTS.get(case_num, 15)

    results = {
        'case': case_num,
        'c1_stop_words': check_criterion_1(text),
        'c2_no_gaps': check_criterion_2(text, original_words, case_num),
        'c3_specifics': check_criterion_3(text, case_num),
        'c4_context': check_criterion_4(text),
        'c5_format': check_criterion_5(text),
        'c6_meaning': check_criterion_6(text, case_num),
        'c7_legal': check_criterion_7(text, case_num),
    }
    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python eval/score.py <output_dir_or_file>")
        sys.exit(1)

    path = Path(sys.argv[1])

    if path.is_file():
        files = [path]
    elif path.is_dir():
        files = sorted(path.glob("case*.md"))
    else:
        print(f"Error: {path} not found")
        sys.exit(1)

    if not files:
        print("Error: no case*.md files found")
        sys.exit(1)

    total_passed = 0
    total_checks = 0

    for f in files:
        results = score_file(f)
        if not results:
            continue

        case_num = results['case']
        criteria = {k: v for k, v in results.items() if k.startswith('c')}
        passed = sum(1 for k, v in criteria.items() if k != 'case' and v)
        total = sum(1 for k in criteria if k != 'case')

        total_passed += passed
        total_checks += total

        fails = [k for k, v in criteria.items() if k != 'case' and not v]
        status = "PASS" if not fails else f"FAIL({','.join(fails)})"
        print(f"  case{case_num}: {passed}/{total} {status}")

    if total_checks == 0:
        print("0")
        sys.exit(0)

    score = round(total_passed / total_checks * 100, 1)
    print(f"\nScore: {score}")


if __name__ == "__main__":
    main()
