# 冒泡排序 
def bubble_sort(arr):
    n = len(arr)
    # 外层循环控制需要比较的轮数
    for i in range(n-1):
        # 内层循环控制每轮比较的次数
        for j in range(n-1-i):
            # 如果前一个数大于后一个数,则交换位置
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# 测试代码
if __name__ == "__main__":
    test_list = [64, 34, 25, 12, 22, 11, 90]
    print("排序前的列表:", test_list)
    sorted_list = bubble_sort(test_list)
    print("排序后的列表:", sorted_list)

