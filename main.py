# pt = "без труда не вытащишь и рыбку из пруда"
pt = "Васе надо придумать строку в 32."
def prepare():
    print(f'Получаем на вход полезную нагрузку в виде строки для шифрования:\n {pt}\n')

    l = []
    for i in pt:
        l.append(ord(i))
    print(f'Получаю значения Юникод каждого символа:\n {l}\n')

    l_ = []
    for i in l:
        l_.append(bin(i)[2:])
    print(f'Потом значения Юникод перевожу в биты:\n {l_}\n')
    l__ = ''
    for i in l_:
        l__ += i
    print(
        f'Далее блоки с бинарными значениями объединяю в строку для последующего разбиения на блоки по 64 бита:\n {l__}\n')
    list_of_bit = l__
    return list_of_bit


list_of_bit = prepare()


def check(list_of_bit):
    if len(list_of_bit) % 64 != 0:
        print('Обнаружено что поток бит не делится без остатка на 64')
        print('Начинается заполнение')
        count_zeros = (64 - len(list_of_bit) % 64)
        print(f'С левой части потока будет добавлено {count_zeros} бит/битов')
        amended_input = (64 - len(list_of_bit) % 64) * '0' + list_of_bit
        input_in_parts = [amended_input[x:x + 64] for x in range(0, len(amended_input), 64)]
        print(f'Блоки после заполнения:\n{input_in_parts}')
        return input_in_parts
    else:
        print('Заполнения блоков не требуется')
        amended_input = (64 - len(list_of_bit) % 64) * '0' + list_of_bit
        input_in_parts = [amended_input[x:x + 64] for x in range(0, len(amended_input), 64)]
        return input_in_parts

input_in_parts = check(list_of_bit)

initial_perm = [58, 50, 42, 34, 26, 18, 10, 2,
                60, 52, 44, 36, 28, 20, 12, 4,
                62, 54, 46, 38, 30, 22, 14, 6,
                64, 56, 48, 40, 32, 24, 16, 8,
                57, 49, 41, 33, 25, 17, 9, 1,
                59, 51, 43, 35, 27, 19, 11, 3,
                61, 53, 45, 37, 29, 21, 13, 5,
                63, 55, 47, 39, 31, 23, 15, 7]


def permute(b_or_k, arr, n):
    permutation = ""
    for i in range(0, n):
        permutation = permutation + b_or_k[arr[i] - 1]
    return permutation


count_i_block = 0
for i in input_in_parts:
    count_i_block += 1

list_of_CT = []
# rkb_ = []
while count_i_block != 0:
    for i in range(0,count_i_block):

        t = permute(input_in_parts[i], initial_perm, 64)
        print(f'\nБлок сообщения {i+1}\n{input_in_parts[i]}')
        print(f'Начальная перестановка для блока сообщения \n{t}\n')


        # циклический сдвиг влево
        def shift_left(k, nth_shifts):
            s = ""
            for i in range(nth_shifts):
                for j in range(1, len(k)):
                    s = s + k[j]
                s = s + k[0]
                k = s
                s = ""
            return k


        key = "0100001010101001010100011001101000011000101000001110100001101001"

        # генерация ключа, сначала перестановка

        keyp = [57, 49, 41, 33, 25, 17, 9,
                1, 58, 50, 42, 34, 26, 18,
                10, 2, 59, 51, 43, 35, 27,
                19, 11, 3, 60, 52, 44, 36,
                63, 55, 47, 39, 31, 23, 15,
                7, 62, 54, 46, 38, 30, 22,
                14, 6, 61, 53, 45, 37, 29,
                21, 13, 5, 28, 20, 12, 4]

        # получение 56 битного ключа из 64 используя таблицу четности keyp
        key = permute(key, keyp, 56)

        # таблица смещений у ключа относительно каждого раунда, я буду делать 1 раунд
        shift_table = [1, 1, 2, 2,
                       2, 2, 2, 2,
                       1, 2, 2, 2,
                       2, 2, 2, 1]

        # таблица сжатия ключа с 56 до 48 бит
        key_comp = [14, 17, 11, 24, 1, 5,
                    3, 28, 15, 6, 21, 10,
                    23, 19, 12, 4, 26, 8,
                    16, 7, 27, 20, 13, 2,
                    41, 52, 31, 37, 47, 55,
                    30, 40, 51, 45, 33, 48,
                    44, 49, 39, 56, 34, 53,
                    46, 42, 50, 36, 29, 32]

        # Разделение
        left = key[0:28]
        right = key[28:56]
        rkb = [] # rkb для RoundKeys в двоичном формате

        for i in range(0, 1): # 16 для 16 ранудов
            # применение сдвига
            left = shift_left(left, shift_table[i])
            right = shift_left(right, shift_table[i])

            # объединение левой и правой части ключа
            combine_str = left + right

            # сжатия ключа с 56 бит до 48 бит
            round_key = permute(combine_str, key_comp, 48)

            rkb.append(round_key)
            # rkb_.append(round_key)

        print(f'Сгенерированный ключ 48 битный \n{rkb[0]}\n')

        # фнукция расширения ключа
        exp_d = [32, 1, 2, 3, 4, 5, 4, 5,
                 6, 7, 8, 9, 8, 9, 10, 11,
                 12, 13, 12, 13, 14, 15, 16, 17,
                 16, 17, 18, 19, 20, 21, 20, 21,
                 22, 23, 24, 25, 24, 25, 26, 27,
                 28, 29, 28, 29, 30, 31, 32, 1]

        # S-box
        sbox = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
                 [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
                 [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
                 [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

                [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
                 [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
                 [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
                 [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

                [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
                 [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
                 [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
                 [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

                [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
                 [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
                 [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
                 [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

                [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
                 [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
                 [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
                 [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

                [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
                 [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
                 [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
                 [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

                [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
                 [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
                 [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
                 [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

                [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
                 [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
                 [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
                 [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

        # Перестановка P
        per = [16, 7, 20, 21,
               29, 12, 28, 17,
               1, 15, 23, 26,
               5, 18, 31, 10,
               2, 8, 24, 14,
               32, 27, 3, 9,
               19, 13, 30, 6,
               22, 11, 4, 25]

        # Конечная перестановка, является обратной к первоначальной перестановке
        final_perm = [40, 8, 48, 16, 56, 24, 64, 32,
                      39, 7, 47, 15, 55, 23, 63, 31,
                      38, 6, 46, 14, 54, 22, 62, 30,
                      37, 5, 45, 13, 53, 21, 61, 29,
                      36, 4, 44, 12, 52, 20, 60, 28,
                      35, 3, 43, 11, 51, 19, 59, 27,
                      34, 2, 42, 10, 50, 18, 58, 26,
                      33, 1, 41, 9, 49, 17, 57, 25]


        def xor(a, b):
            ans = ""
            for i in range(len(a)):
                if a[i] == b[i]:
                    ans = ans + "0"
                else:
                    ans = ans + "1"
            return ans


        def encrypt(t, rkb):
            # Разбитие текста


            left = t[0:32]
            right = t[32:64]

            for i in range(0, 1): # 16 если 16 раундов
                print("Идет раунд ", i + 1, " ")
                print(f'Разбитие текста на 2 части по 32бита')
                print(f'Левая часть: {left}')
                print(f'Правая часть: {right}\n')
                #  Таблица расширения D-box: преобразует 32 бита в 48
                print(f'Алгорим функции f')
                right_expanded = permute(right, exp_d, 48)
                print(f'Расширение правой части R: {right_expanded}')
                # XOR RoundKey[i] и right_expanded
                xor_x = xor(right_expanded, rkb[i])
                print(f'XOR правой части после расширения с ключом: {xor_x}\n')
                # S-boxex: подстановка значения из таблицы s-box путем вычисления строки и столбца
                sbox_str = ""
                for j in range(0,8):
                    row = int(xor_x[j * 6] + xor_x[j * 6 + 5], 2)
                    col = int(xor_x[j * 6 + 1] + xor_x[j * 6 + 2] + xor_x[j * 6 + 3] + xor_x[j * 6 + 4], 2)
                    val = sbox[j][row][col]
                    sbox_str = sbox_str + bin(val)[2:].zfill(4)
                #после S боксов перестановка P
                sbox_str = permute(sbox_str, per, 32)
                print(f'После перестановки битов: {sbox_str}')
                # функиця f
                result = xor(left, sbox_str)
                print(f'Результат функции f: {result}\n ')
                left = result

                # Swapper
                if (i != 1): #15 если 16 раундов
                    left, right = right, left



                print('Левая половина равна правой половине пердыдущего вектора'," ",'Правая это XOR L и f(R,k)')
                print(f'L = {left}',"                     ", f'R = {right}')

            # Объединяю левую и правую часть
            combine = left + right
            print(f'Объединение левой и правой части: {combine}')
            # окончательная перестановка битов для получения зашифрованного текста
            cipher_text = permute(combine, final_perm, 64)
            print(f'Конечная перестановка: {cipher_text}')
            return cipher_text


        count_i_block -= 1
        cipher_text = encrypt(t, rkb)


        list_of_CT.append(cipher_text)


cipher_res = ""
print(f'\nШифрованные блоки текста:\n{list_of_CT}\n')
for i in list_of_CT:
    cipher_res += i
print("Объединение шифр блоков в строку:", cipher_res)


