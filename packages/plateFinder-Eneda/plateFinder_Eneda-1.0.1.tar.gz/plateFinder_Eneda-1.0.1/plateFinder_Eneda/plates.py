from plateFinder_Eneda.utlis import get_data_from_excel


def find_plate():
    user_key = input("Please enter your key: ")
    data = get_data_from_excel()
    result = data.get(user_key, None)

    if result is not None:
        print(f'The owner of the car is: {result} ,Thank You')
    else:
        print('Owner NOT Found!!!')

