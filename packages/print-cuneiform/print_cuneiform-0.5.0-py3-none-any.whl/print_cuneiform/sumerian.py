__ash__ = {0: '', 1: u'\U00012038 ', 2: u'\U00012400 ', 3: u'\U00012401  ', 4: u'\U00012402  ', 5: u'\U00012403  ',
            6: u'\U00012404  ', 7: u'\U00012405  ', 8: u'\U00012406  ', 9: u'\U00012407   '}
__u__ = {0: '', 1: u'\U0001230B', 2: u'\U0001230B\U0001230B', 3: u'\U0001230B\U0001230B\U0001230B', 4: u'\U0001240F ',
          5: u'\U00012410 '}
__gesh__ = {0: '', 1: u'\U00012415', 2: u'\U00012416 ', 3: u'\U00012417  ', 4: u'\U00012418 ', 5: u'\U00012419  ',
             6: u'\U0001241A  ', 7: u'\U0001241B  ', 8: u'\U0001241C  ', 9: u'\U0001241D  '}
__geshu__ = {0: '', 1: u'\U0001241E ', 2: u'\U0001241F ', 3: u'\U00012420  ', 4: u'\U00012421 ', 5: u'\U00012422  '}
__shar__ = {0: '', 1: u'\U0001212D ', 2: u'\U00012423   ', 3: u'\U00012424     ', 4: u'\U00012426   ',
             5: u'\U00012427     ', 6: u'\U00012428     ', 7: u'\U00012429      ', 8: u'\U0001242A      ',
             9: u'\U0001242B        '}
__sharu__ = {0: '', 1: u'\U0001242C ', 2: u'\U0001242D   ', 3: u'\U0001242E     ', 4: u'\U00012430   ',
              5: u'\U00012431    '}

__lal__ = u'\U000121F2 '

def int_to_sumerian(input_value, ash=True):
    test_value = int(input_value)
    out_string = ""
    if test_value < 0:
        out_string = out_string + __lal__
        test_value = abs(test_value)


    if test_value > 36000 * 5:
        return "Number to large"

    if test_value >= 36000:
        number_of_numeral = test_value // 36000
        test_value = test_value % 36000
        out_string = out_string + __sharu__[number_of_numeral]

    if test_value >= 3600:
        number_of_numeral = test_value // 3600
        test_value = test_value % 3600
        out_string = out_string + __shar__[number_of_numeral]

    if test_value >= 600:
        number_of_numeral = test_value // 600
        test_value = test_value % 600
        out_string = out_string + __geshu__[number_of_numeral]

    if test_value >= 60:
        number_of_numeral = test_value // 60
        test_value = test_value % 60
        out_string = out_string + __gesh__[number_of_numeral]

    if test_value > 0:
        tens_digit = test_value // 10
        ones_digit = test_value % 10
        out_string = out_string + __u__[tens_digit]
        if ash:
            out_string = out_string + __ash__[ones_digit]
        else:
            out_string = out_string + __gesh__[ones_digit]

    return out_string

def main_cli():
    import sys
    input_value = int(sys.argv[1])
    string_value = int_to_sumerian(input_value,ash=True)
    print(string_value)

def main_cli_cla():
    import sys
    input_value = int(sys.argv[1])
    string_value = int_to_sumerian(input_value,ash=False)
    print(string_value)

if __name__ == "__main__":
    main_cli()
