from tkinter import *
import time
import random

#global var
stroke = []
alfabet = []
rules = dict()

def read_alf(a):
    b = list(a)
    for i in range(len(b)):
        if b[i].isupper() and (b[i] not in alfabet):
            alfabet.append(b[i])
    # print(alfabet)  # test
    return 0

def read_rules(a:str) -> str:
    '''
    Функция для чтения правил с файла по строчно
    '''
    # one_stroke = list(a)
    # left = ''
    # right = ''
    # n_right = ''
    # for_right = a.index('>')
    # for i in range(for_right):
    #     left += one_stroke[i]
    # rules[left]=[]

    # for j in range(one_stroke.count('|')+1):
    #     try:
    #         last_point = one_stroke.index('|',for_right+1,len(one_stroke))
    #     except:
    #         last_point = len(one_stroke)
    #     for i in range(for_right+1,last_point):
    #         n_right += one_stroke[i]
        
    #     for_right = last_point
    #     right = n_right
    #     n_right = ''
    #     rules[left].append(right)
    right = a[2:].split('|')
    rules[a[0]] = right

    # print(rules) #test
    return 0

def for_one_way(a): #подумать тут!!!
    result = ''
    all_result = []
    for i in rules[f'{a}']:
        result = i
        result.replace(rules[f'{a}'][i],rules[i] )
    all_result.append(result)
    
    #print(rules[f'{a}'])
    print(all_result)

    return 0

# def make_all_way(a):
#     for i in range(len(rules[f'{a}'])):
        
#         return rules[f'{a}'][i]
#     return 0

# def make_all_result():
#     all_result = []
#     while make_all_way() != 0:
#         all_result.append(make_all_way())
#     return 0

# Рабочий варик для буквенных
def makeSameResult():
    sameResult:str = list(rules.keys())[0]
    letter = 0
    while(sameResult.islower() != True):
        if (sameResult[letter].isupper()):
            sameResult = sameResult[:(letter)] + rules[sameResult[letter]][random.randint(0, len(rules[sameResult[letter]])-1)] + sameResult[letter+1:]
        else:
            letter += 1
        #print(sameResult)#test
    return sameResult


def mainProgramm():
    global stroke
    programm = open("programm.txt", "r")
    stroke = programm.read().splitlines()
    programm.close()
    for i in range(len(stroke)):
        read_alf(stroke[i])
        read_rules(stroke[i])
        # for_one_way('S')
    # print(stroke) #test
    return 0

if __name__ == '__main__':
    mainProgramm() #Можно убрать
    
    print('Алфавит:',*alfabet) #test
    print('Правила:',*stroke, sep="\n") #test
    print(rules)
    print(makeSameResult())

    # rWidth,rHeight = 400, 500
    # root = Tk()     # создаем корневой объект - окно
    # root.title("Приложение для ТЯП")     # устанавливаем заголовок окна
    # root.geometry(f"{rWidth}x{rHeight}")    # устанавливаем размеры окна
    
    # f1 = LabelFrame(root,text="Ваша программа",width=rWidth*0.9,height=rHeight*0.6) # root можно не указывать
    # f1.place(relx=0.5, rely=0, anchor=N)

    # button = Button(padx=50, pady=20)
    
    # button.place(relx=0.3, rely=0.7, anchor=N)

    # root.mainloop()

    # time.sleep(60)