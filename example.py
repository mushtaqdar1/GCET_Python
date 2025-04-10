list1=[1,'hi', 30.5]
list2=[55,77]
list3=list2.copy()
print("The elements from list2", list2)
print("List 3:Copied elements from list2", list3)
list3.pop(0)#popping an element
print("List 3:poped elements from list3",list3)
list2.extend(list1)
list1.append(68)
#list3.clear()
print("List 2:extended elements from list3",list2)
