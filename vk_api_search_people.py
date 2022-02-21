import requests
import os
import json
from auth_data import VKTOKEN
import time


def VK_get_members(group_name):
    new_url = f"https://api.vk.com/method/groups.getMembers?group_id={group_name}&count=1000&access_token={VKTOKEN}&v=5.131 "
    req = requests.get(new_url)
    src = req.json()
    list_count = src["response"]["count"]
    povtor = round(list_count / 1000) + 2

    for parsing in range(povtor):
        members = src["response"]["items"]
        new_offset = parsing * 1000
        new_url = f"https://api.vk.com/method/groups.getMembers?group_id={group_name}&count=1000&offset={new_offset}&access_token={VKTOKEN}&v=5.131 "
        time.sleep(0.3)
        req = requests.get(new_url)
        src = req.json()
        if os.path.exists(f"{group_name}") and new_offset == 0:
            break
        if os.path.exists(f"{group_name}"):
            if new_offset > list_count:
                print(f"Выполнено {list_count}/{list_count} ")
            else:
                print(f"Выполнено {new_offset}/{list_count} ")
        else:
            os.mkdir(group_name)

        # Создание файла json
        with open(f"{group_name}/{group_name}_{new_offset}.json", "w", encoding="utf-8") as file:
            json.dump(src, file, indent=4, ensure_ascii=False)

        with open(f"{group_name}/exist_members_{group_name}.txt", "a") as file:
            for item in members:
                file.write(str(item) + "\n")


def comparison(list_group_id):
    group_name = list_group_id[0]
    first_list = []
    vk_id_all = []
    vk_id_all_str = ''

    file = open(f"{group_name}/exist_members_{group_name}.txt", "r")
    # Заполнение 1 списка для сравнения
    for line in file:
        first_list.append(line)
    # Заполнение последующих списков для сравнения
    for i in range(len(list_group_id) - 1):
        group_name = list_group_id[i + 1]

        file = open(f"{group_name}/exist_members_{group_name}.txt", "r")
        second_list = []
        for line in file:
            second_list.append(line)

        first_list = list(
            set(first_list) & set(second_list))  # Сравнение 1 списка с последующими и сохранение совпадений в 1 список
    if len(first_list) == 0:
        print('Пересечения отсутсвуют.')
    else:
        for lines in range(len(first_list)):  # Вывод id пользователей входящие во все вышеперечисленные списки
            vk_id_all_str += f"{first_list[lines]}" + ","
            vk_id_all_str = vk_id_all_str.replace("\n", "")
            vk_id = f"[{lines + 1}] vk.com/id{first_list[lines]}"
            vk_id = vk_id.replace("\n", "")
            vk_id_all.append(vk_id)
        if input("Впишите '1' чтобы вывести ссылки с именами: ") == '1':
            url_for_name = f"https://api.vk.com/method/users.get?user_ids={vk_id_all_str}&access_token={VKTOKEN}&v=5.131 "
            get_name(url_for_name, vk_id_all)
        else:
            for i in range(len(vk_id_all)):
                print(vk_id_all[i])


def get_name(url_for_name, vk_id_all):
    full_inference = ""
    list_index = -1
    req = requests.get(url_for_name)
    src = req.json()
    json_response_userName = src["response"]
    for name in json_response_userName:
        try:
            if "first_name" in name:
                f_name = name["first_name"]
                l_name = name["last_name"]
                list_index += 1
                full_inference += vk_id_all[list_index] + " " + str(f_name) + " " + str(l_name) + "\n"
        except Exception:
            print("Что-то пошло не так :(((")
    print(full_inference)


def main():
    num_groups = int(input("Введите количество вводимых групп: "))
    list_group_id = []
    for number_groups in range(num_groups):
        group_name = input(
            f"Введите название {number_groups + 1} группы: ")
        group_name = group_name.replace("public", "")
        list_group_id.append(group_name)
        VK_get_members(group_name)
    if len(list_group_id) >= 2:
        comparison(list_group_id)


if __name__ == '__main__':
    main()
