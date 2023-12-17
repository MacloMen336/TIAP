import re
import random

# Чтение грамматики из файла
with open("grammar.txt", "r") as file:
    grammar_text = file.read()

# Разбиение текста грамматики на правила
rules = grammar_text.split("\n")

# Создание словаря для хранения правил грамматики
grammar_dict = {}
# Обработка каждого правила и добавление его в словарь
for rule in rules:
    if "->" in rule:
        left, right = rule.split("->")
        right = right.split("|")
        grammar_dict[left.strip()] = [r.strip().split() for r in right]

# Определение, является ли грамматика регулярной
def is_regular(grammar_dict):
    for left, right in grammar_dict.items():
        for rule in right:
            # Проверяем, что каждый символ в правой части правила является либо терминалом, либо нетерминалом
            for symbol in rule:
                if not re.match(r'^[A-Za-z0-9]+$', symbol):
                    return False
            # Проверяем, что в правой части правила нет двух последовательных нетерминалов
            for i in range(len(rule) - 1):
                if re.match(r'^[A-Z]+$', rule[i]) and re.match(r'^[A-Z]+$', rule[i+1]):
                    return False
    return True

def generate_words(grammar_dict, start_symbol):
    # Список для хранения порождаемых слов
    words = []
    # Начальное слово - стартовый символ
    current_word = start_symbol

    # Пока есть нетерминальные символы в слове
    while re.findall(r'[A-Z]', current_word):
        # Ищем первый нетерминальный символ
        nonterminal = re.search(r'[A-Z]', current_word).group()
        # Если его правило существует в грамматике
        if nonterminal in grammar_dict:
            # Выбираем случайное правило из возможных
            rule = random.choice(grammar_dict[nonterminal])
            # Создаем новое слово, заменяя первое вхождение нетерминала на правую часть выбранного правила
            new_word = current_word.replace(nonterminal, " ".join(rule), 1)
            # Добавляем новое слово в список
            words.append(new_word + f' ({nonterminal} => {" ".join(rule)})')
            # Обновляем текущее слово на новое
            current_word = new_word
        else:
            # Если правила для нетерминала не существует, заменяем его на случайный терминал
            terminals = [symbol for symbol in current_word if re.match(r'^[A-Za-z0-9]+$', symbol)]
            random_terminal = random.choice(terminals)
            current_word = current_word.replace(nonterminal, random_terminal, 1)
            # Добавляем текущее слово в список
            words.append(current_word + f' ({nonterminal} => {random_terminal})')

    # Выводим все порожденные слова
    for word in words:
        print("{}".format(word))

# Функция построения конечного автомата
def build_automaton(grammar_dict):
    # Инициализируем пустой словарь для хранения конечного автомата
    automaton = {}
    # Перебираем каждое правило грамматики
    for left, right in grammar_dict.items():
        for rule in right:
            # Если правило состоит из одного символа, добавляем его в автомат
            if len(rule) == 1:
                if left not in automaton:
                    automaton[left] = {}
                automaton[left][rule[0]] = [left]
            # Если правило состоит из двух символов, добавляем переход в автомат
            else:
                if left not in automaton:
                    automaton[left] = {}
                if rule[0] not in automaton[left]:
                    automaton[left][rule[0]] = []
                automaton[left][rule[0]].append(rule[1])
        # Выводим полученный конечный автомат
    print("Конечный автомат:")
    for state, transitions in automaton.items():
          print(f"{state} -> {transitions}")
        # Возвращаем полученный конечный автомат
    return automaton

def check_word(word, grammar_dict):
    current_states = ['S']
    path = {state: [] for state in grammar_dict} # словарь для хранения пути
    for symbol in word:
        next_states = []
        for state in current_states:
            if state not in grammar_dict:
                continue
            if symbol not in grammar_dict[state]:
                continue
            next_states += grammar_dict[state][symbol]
            for next_state in grammar_dict[state][symbol]: # добавляем путь к следующему состоянию
                path[next_state].append((state, symbol))
        if not next_states:
            print(f"Слово '{word}' не принадлежит грамматике")
            return
        current_states = next_states
    for state in current_states:
        if state in grammar_dict['EPSILON']:
            print(f"Слово '{word}' принадлежит грамматике")
            # сворачиваем слово от конца до начала по пути
            result = [state]
            for prev_state, symbol in reversed(path[state]):
                result.insert(0, prev_state)
                result.insert(0, symbol)
            print(" ".join([f"{result[i]} -> {result[i+1]};" for i in range(0, len(result)-1, 2)]))
            return
    print(f"Слово '{word}' не принадлежит грамматике")

generate_words(grammar_dict,'S')

if is_regular(grammar_dict):
    print("Грамматика является регулярной.")

    start_symbol = 'S'
    end_symbols = ['A', 'B', 'C']
    grammar_dict['EPSILON'] = end_symbols

    automaton = build_automaton(grammar_dict)
    word = input("Введите слово для проверки: ")
    check_word(word, automaton)
else:
    print("Грамматика не является регулярной.")