import string
import re
temp = '565598||cdndm5|98|40|com|101|manhua1032|http|69|32f0e8371cda88218d6784d723ada4eb|key|161|type|cid|39948|png|jpg|16_2974|13_5230|15_1310|12_1045|14_1108|17_6663|22_6925|21_7725|20_4023|18_1924|19_1395|3_5691|4_8115|5_9961|newImgs|1_2570|2_2038|9_3918|10_2330|11_1351|6_2201|7_2626|8_3098|23_3063|39_8140|40_5433|38_6370|36_4345|37_1897|41_2644|45_8007|30_4913|44_9775|42_2712|43_8882|35_7467|27_8007|28_4477|26_9840|24_8761|25_4377|29_2102|33_7794|34_3493|32_9759|var|31_2662'
temp_array = temp.split('|')
print(temp_array)
old = "8://7-6-9-c-3.2.5/4/f/0/t.g?e=0&b=a&d=1"
def UrlAnalysis(temp_array, old):
    capital_dict = dict.fromkeys(string.ascii_uppercase, 0)
    capital_list = [chr(i) for i in range(65,91)]
    i = 36
    for temp in capital_list:
        capital_dict[temp] = i
        i = i + 1

    lowercase_letters_dict = dict.fromkeys(string.ascii_lowercase, 0)
    lowercase_letters_list = [chr(i) for i in range(97,123)]
    i = 10
    for temp in lowercase_letters_list:
        lowercase_letters_dict[temp] = i
        i = i + 1

    num_list = [str(i) for i in range(10,91)]
    num_dict = dict.fromkeys(num_list, 0)
    i = 62
    for temp in num_list:
        num_dict[temp] = i
        i = i + 1

    for ce in lowercase_letters_list:
        try:
            old = re.sub(r'(?<=\W)%s(?=\W)'%(ce),temp_array[lowercase_letters_dict[ce]],old)#位置匹配
        except :
            break
    for ce in capital_list:
        try:
            old = re.sub(r'(?<=\W)%s(?=\W)'%(ce),temp_array[capital_dict[ce]],old)#位置匹配
        except:
            break
    for ce in num_list:
        try:
            old = re.sub(r'(?<=\W)%s(?=\W)'%(ce),temp_array[num_dict[ce]],old)
        except:
            break
    for num in range(0,10):
        try:
            old = re.sub(r'(?<=\W)%s(?=\W)'%(num),temp_array[num],old)
        except:
            break
    old = "http" + old[1:]
    print(old)
    return old
def main():
    UrlAnalysis(temp_array, old)

if __name__ == '__main__':
    main()