import time
import math

def clear(): #Czyszczenie okna terminala
    print("\x1B\x5B2J", end="")
    print("\x1B\x5BH", end="")

def int_input(): #Zabezpieczony input liczb by przy wprowadzeniu złego znaku nie psuło programu
    while True:
        x = input("-> ")
        try: int(x)
        except ValueError:
            print("To nie jest liczba!")
        else:
            y = int(x)
            return y    

# OPERACJE NA PLIKACH

def choose_file(n):
    if n == 0: # Zestaw treningowy
        return "train_data.data"
    elif n == 1: # Zestaw walidacyjny
        return "dev_data.data"
    elif n == 2: # Zestaw testowy
        return "test_data.data"
    elif n == 3: # Pełen zestaw danych | Plik, który do testów może być nadpisywany
        return "full_data.data"
    elif n == 4: # Pełen zestaw danych | Plik oryginalny, który nie będzie nadpisywany przez program
        return "house-votes-84.data"
    else:
        print('"n" powinno mieścić się w przedziale <0;2>')
        return 0

def read_file(file_name): #Wczytywanie danych z pliku
    file = open(file_name, "r")
    data1d = []
    data2d = []
    j=0
    for linia in file:
        linia = linia.strip("\n")
        linia = linia.split(",")
        for i in range(len(linia)):
            data1d.append(linia[i])
        data2d.append(data1d)
        data1d = [] 
        j += 1
    file.close()
    return data2d

def save_file(data, file_name):
    file = open(file_name, "w")
    for i in range(len(data)):
        for j in range(len(data[i])):
            file.write(data[i][j])
            file.write(",")
        file.write("\n")        
    file.close()

# OPERACJE NA ZAIMPORTOWANYCH ZBIORACH DANYCH

def make_train_dev_test(data, type): #Podział zbioru na train/dev/test
    data_lenght = len(data) - 1

    train = 0.6*data_lenght
    dev = 0.2*data_lenght
    test = 0.2*data_lenght

    if train != int(train) or dev != int(dev) or test != int(test):
        train = int(train)
        dev = int(dev)
        test = int(test)


    
    if type == 0: #ZESTAW TESTOWY
        train_data = []
        for i in range(train + 1):
            train_data.append(data[i])
        return train_data
    elif type == 1:
        dev_data = []
        for i in range(train + 1, train + dev + 1):
            dev_data.append(data[i]) 
        return dev_data
    elif type == 2:
        test_data = []
        for i in range(train + dev + 1, train + dev + test + 1):
            test_data.append(data[i]) 
        return test_data
    else:
        print('"Type" musi mieścić się w przedziale <0;2>')

def show_data(data): #Wyświetlenie danych zawartych w konkretnym zbiorze
    for i in range(len(data)):
        print(f"{i}." + data[i][0] + " " + data[i][1] + " " + data[i][2] + " " + data[i][3] + " " + data[i][4] + " " + data[i][5] + " " + data[i][6] + " " + data[i][7] + " " + data[i][8] + " " + data[i][9] + " " + data[i][10] + " " + data[i][11] + " " + data[i][12] + " " + data[i][13] + " " + data[i][14] + " " + data[i][15] + " " + data[i][16])

# ALGORYTM K - NAJBLIŻSZYCH SĄSIADÓW

def one_answer(data):
    politician_answers = []
    if data[0] == 'democrat':
        politician_answers.append(1) # 0 - republican, 1 - democrat
    elif data[0] == 'republican':
        politician_answers.append(0)
    for question_number in range(1, 17): # Y - 1,0 | N - 0,1 | ? - 0,0
        if data[question_number] == "y":
            politician_answers.append(1)
            politician_answers.append(0)
        elif data[question_number] == "n":
            politician_answers.append(0)
            politician_answers.append(1)
        elif data[question_number] == "?":
            politician_answers.append(0)
            politician_answers.append(0)
    return politician_answers  

def find_answers(data): #ILE RAZY KAŻDY POLITYK ODPOWIEDZIAŁ Y/N/?
    all_answers = []
    for i in range(len(data)):
        all_answers.append(one_answer(data[i]))
    return all_answers

def distance(points, unkown_politician):
    power = 0
    for i in range(1, len(points)):
        power +=math.pow((points[i] - unkown_politician[i]), 2)
    distance = math.sqrt(power)

    return distance

def find_neighbours(unknown_politician, answers, k):
    distances = []
    neighbours_check = []

    for i in range(len(answers)):
        distances.append(distance(answers[i], unknown_politician))
        neighbours_check.append(0) # TWORZENIE TABLICY ZER DO SPRAWDZANIA SĄSIADÓW
    for j in range(k):
        distance_number = 0
        for i in range(1, len(answers)):
            if distances[i] < distances[distance_number] and neighbours_check[i] == 0:
                distance_number = i
        neighbours_check[distance_number] = 1

    # for i in range(len(distances)):
    #     print(f"{i}. {distances[i]} | n_check = {neighbours_check[i]}")
    return neighbours_check

def show_answers(answers):
    print("[Y|N|0-R 1-D]")
    print(answers)

def knn(train_data, dev_data, k):
    all_answers = find_answers(train_data)
    prediction = []
    
    for i in range(len(dev_data)):
        D = 0
        R = 0
        neighbours_check = find_neighbours(one_answer(dev_data[i]), all_answers, k)
        for j in range(len(neighbours_check)):
            if neighbours_check[j] == 1:
                if all_answers[j][0] == 1:
                    D += 1
                elif all_answers[j][0] == 0:
                    R += 1
                else:
                    print("knn: error")
        
        #print(f"D = {D} R = {R}")
        if D>=R:
            prediction.append(1) # KNN - democrat
        else:
            prediction.append(0) # KNN - republican

    return prediction

# MACIERZ POMYŁEK

def show_and_compare(prediction, dev_data):
    for i in range(len(prediction)):
        if prediction[i] == 1:
            print(f"PREDICTED: democrat   | CORRECT: {dev_data[i][0]}")
        elif prediction[i] == 0:
            print(f"PREDICTED: republican | CORRECT: {dev_data[i][0]}")

def confusion_matrix(prediction, data, k):
    TP = 0
    FP = 0
    FN = 0
    TN = 0
    for i in range(len(prediction)):
        if prediction[i] == 1 and data[i][0] == "democrat":
            TP += 1 # prawdziwie dodatnia
        elif prediction[i] == 1 and data[i][0] == "republican":
            FP += 1 # fałszywie dodatnia
        elif prediction[i] == 0 and data[i][0] == "democrat":
            FN += 1 # fałszywie ujemna
        elif prediction[i] == 0 and data[i][0] == "republican":
            TN += 1 # prawdziwie ujemna

    TPR = TP/(TP+FN) # czułość
    TNR = TN/(FP+TN) # swoistość
    precision = TP/(TP+FP) # precyzja
    ACC = (TP+TN)/(TP+FN+FP+TN) # dokładność
    #ERR = (FP+TN)/(TP+FN+FP+TN) # poziom błędu

    print(f"K = {k}| Czułość TPR = {round(TPR, 4)}|Swoistość TNR = {round(TNR, 4)}|Precyzja = {round(precision*100, 0)}% | Dokładność ACC = {round(ACC*100, 0)}%")
    # print(f"Prawdziwie dodatnia TP = {TP} | Fałszywie dodatnia FP = {FP} | Fałszywie ujemna FN = {FN} | Prawdziwie ujemna TN = {TN}")

#MENU 

def menu_view(data, train_data, dev_data, test_data):
    clear()
    print("1 - Wyświetl cały zbiór danych")
    print("2 - Wyświetl zbiór treningowy")   
    print("3 - Wyświetl zbiór walidacyjny")
    print("4 - Wyświetl zbiór testowy")
    y = int_input()
    if y == 1: # WYŚWIETLENIE CAŁEGO ZBIORU
        clear()
        print("CAŁY ZBIÓR DANYCH")
        show_data(data)
        input("Nacisnij Enter by kontynuowac")
        clear()
    elif y == 2: # WYŚWIETLENIE ZBIORU TRENINGOWEGO
        clear()
        print("ZBIÓR TRENINGOWY")
        show_data(train_data)
        input("Nacisnij Enter by kontynuowac")
        clear()
    elif y == 3: # WYŚWIETLENIE ZBIORU WALIDACYJNEGO
        clear()
        print("ZBIÓR WALIDACYJNY")
        show_data(dev_data)
        input("Nacisnij Enter by kontynuowac")
        clear()
    elif y == 4: # WYŚWIETLENIE ZBIORU TESTOWEGO
        clear()
        print("ZBIÓR TESTOWY")
        show_data(test_data)
        input("Nacisnij Enter by kontynuowac")
        clear()
    else:
        clear()
        print("Nie ma takiej opcji!\n")
        input("Nacisnij Enter by kontynuowac")
        clear()

def menu_knn_choose(train_data, choosen_data):
    clear()
    while True:
        print("1 - Wprowadź k")
        print("2 - Zbadaj działanie algorytmu dla 'k' z przedziału")
        x = int_input()
        if x == 1:
            clear()
            print("Wprowadź k")
            k = int_input()
            prediction = knn(train_data, choosen_data, k)
            show_and_compare(prediction, choosen_data)
            confusion_matrix(prediction, choosen_data, k)
            break
        elif x == 2:
            clear()
            a = int_input()
            b = int_input()
            clear()
            for k in range(a, b+1):
                prediction = knn(train_data, choosen_data, k)
                confusion_matrix(prediction, choosen_data, k)                
            break
        else:
            print("Nie ma takiej opcji!\n")         
            break    

#MAIN

data = read_file(choose_file(4))
train_data = read_file(choose_file(0))
dev_data = read_file(choose_file(1))
test_data = read_file(choose_file(2))

while True: #Menu
    print("1 - Wyświetl dane")
    print("2 - Algorytm KNN")
    print("3 - Podział zbioru na train/dev/test")
    print("4 - Zapisz pliki z danymi\n")
    print("5 - Wyjdz z programu\n")
    x = int_input()

    if x == 1: # WYŚWIETLENIE DANYCH
        menu_view(data, train_data, dev_data, test_data)
    elif x == 2: # KNN
        clear()
        print("Wybierz zbiór")
        print("1 - Zbiór walidacyjny")
        print("2 - Zbiór testowy")
        y = int_input()
        clear()
        if y == 1:
            menu_knn_choose(train_data, dev_data)
        elif y == 2:
            menu_knn_choose(train_data, test_data)
        else:
             print("Nie ma takiej opcji!\n")       
        input("Nacisnij Enter by kontynuowac")
        clear()
    elif x == 3:
        clear()
        train_data = make_train_dev_test(data, 0)
        dev_data = make_train_dev_test(data, 1)
        test_data = make_train_dev_test(data, 2)
        print("Podzielono zbiór w proporcjach 60:20:20")
        input("Nacisnij Enter by kontynuowac")
        clear()
    elif x == 4:
        save_file(train_data, choose_file(0))
        save_file(dev_data, choose_file(1))
        save_file(test_data, choose_file(2))
        save_file(data, choose_file(3))
        print("Dane zostały zapisane")
        input("Nacisnij Enter by kontynuowac")
        clear()       
    elif x == 5: #ZAKOŃCZ PROGRAM
        break
    else:
        clear()
        print("Nie ma takiej opcji!\n")
        input("Nacisnij Enter by kontynuowac")
        clear()