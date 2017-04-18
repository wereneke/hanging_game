import random
import time
import datetime


def opening_csv_file(filecsv="countries_and_capitals.txt"):

    '''convert csv file to list of couples country | capital'''

    Countryfile = open(filecsv)                     # OTWIERANIE PLIKU
    text_country_capital = Countryfile.read()                            # CZYTANIE PLIKU
    list_of_couples = text_country_capital.split('\n')            # ZAMIENIANIE PLIKU W LISTE
    return list_of_couples


def random_couple(lista, r):

    '''input: list of couples made by opening_csv_file, random integer
       output: list of strings [country, city]
    '''

    couple = list_of_couples[r]                              # WYBOR PARY
    country = ''
    city = ''
    for i in range(len(couple)):
        if couple[i:i+3] == ' | ':                           # STWORZENIE ZMIENNYCH
            country = couple[:i]
            city = couple[i+3:]
    return [country, city]


def play_information(life_points, used_letters, part_answer):

    '''prints actual informations about life-points, used letters, and visual form of guessing stage'''

    print('you have ', life_points, " lives \n",)
    print('You already used ', used_letters, end='\n')
    print(part_answer, end='\n \n')


def win_screen(counter, country, city_to_guess):

    '''win communicate, saving win-information to score.txt file as append'''

    print("Correct! that was %s capital of %s. It took you %s steps and %s sec"
          % (city_to_guess, country, counter, round(TIME)))
    name = input("enter your name")
    date = str(datetime.datetime.now().strftime("%d.%m.20%y %H:%M"))  # STRASZNIE HYTRE ZAPODANIE ROKU
    score_list = [name, date, str(counter), city_to_guess]
    score_text = ' | '.join(score_list) + '\n'
    scoreFile = open('score.txt', 'a')
    scoreFile.write(score_text)


def end_game_screens(life_points, part_answer, city_to_guess, counter, country):

    '''end screens, asking if we want to play again, returns variable conditioning loop of game-body'''

    if life_points != 0 and part_answer == city_to_guess:                                        # ekrany pozegnalne
        win_screen(counter, country, city_to_guess)

    else:
        print('You die! That was ', city_to_guess, 'the capital of', country)

    play = input('Would you like to play again? (y/n)')       # czy gramy dalej
    return play


def letter_checkout(part_answer, city_to_guess, num_of_letters, answer):

    '''checks answer and update and return visual form of guessing stage in string'''

    list_part_answer = list(part_answer)
    list_city_to_guess = list(city_to_guess)
    for i in range(num_of_letters):
        if answer == list_city_to_guess[i]:
            list_part_answer[i] = answer
    part_answer = ''.join(list_part_answer)
    return part_answer


# tworze liste panstw | miast do losowania
list_of_couples = opening_csv_file()
# ekran powitalny
print("""Welcome to the hanging game, try to guess one of
 the european capitals, or die!""", end='\n')
# zmienna warunku rozgrywki
play = 'y'
# rozgrywka
while play == 'y':
    # rozpoczecie mierzenia czasu, ustalenie poziomu zmiennych, losowanie pary panstwo | miasto 
    start = time.time()
    counter = 0
    life_points = 5
    used_letters = []
    r = random.randint(0, len(list_of_couples)-1)
    couple = random_couple(list_of_couples, r)
    country = couple[0]
    city = couple[1]
    # ujednolicenie zmiennych zeby byly czytelne dla funkcji programu
    city_to_guess = city.upper()
    num_of_letters = len(city_to_guess)
    part_answer = num_of_letters * '_'
    # funkcjonalnosc deweloperska
    print(city)
    # etap zgadywania
    while life_points > 0 and part_answer != city_to_guess:
        # podpowiedz przy ostatnim zyciu
        if life_points == 1:
            print('The capital of', country, end='\n')
        # wyswietlanie informacji o stanie rozgrywki
        play_information(life_points, used_letters, part_answer)
        # pytanie o odpowiedz
        answer = input('What is your guess?')
        answer = answer.upper()
        # przetwarza odpowiedz
        if answer in used_letters:
            print('You already used that one! \n')
        else:
            if answer not in city_to_guess:
                used_letters = used_letters + [answer]
            # funkcjonalnosc deweloperska
            print(answer)
            # sprawdzenie poprawnosci przy zgadywaniu calego slowa
            if len(answer) > 1:                                     
                if answer == city_to_guess:
                    part_answer = answer       
                    counter += 1
                    break
                else:
                    print('''It is'nt that one! \n''')
                    life_points -= 2
                    counter += 1
            # zabezpieczenie przed pusta odpowiedzia
            elif len(answer) == 0:
                print('Try again \n')
            else:
                # zla litera
                if answer not in city_to_guess:
                    life_points -= 1
                    counter += 1
                # dobra litera
                else:                                                
                    counter += 1
                    part_answer = letter_checkout(part_answer, city_to_guess, num_of_letters, answer)

    end = time.time()
    TIME = end - start
    # aktualizuje zmienna warunku rozgrywki
    play = end_game_screens(life_points, part_answer, city_to_guess, counter, country)
