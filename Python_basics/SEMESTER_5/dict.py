# Creating a dictionary
my_dict = {
    "name": "Mushtaq",
    "age": 38,
    "location": "Jammu & Kashmir"
}

# Accessing a value
print(my_dict["name"])  # Output: Mushtaq

# Adding a new key-value pair
my_dict["occupation"] = "Developer"

# Modifying a value
my_dict["age"] = 26

# Removing a key-value pair
del my_dict["location"]

# Printing the updated dictionary
print(my_dict)  # Output: {'name': 'Mushtaq', 'age': 26, 'occupation': 'Developer'}
# Example of a nested dictionary
users = {
    "user1": {
        "name": "Mushtaq",
        "age": 25,
        "location": "Lar"
    },
    "user2": {
        "name": "Ali",
        "age": 30,
        "location": "Srinagar"
    }
}

# Accessing nested values
print(users["user1"]["location"])  # Output: Lar
print(users)



# Example: Squaring numbers
squares = {x: x**2 for x in range(1, 6)}
print(squares)  # Output: {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
cubes={x:x**3 for x in range(0,4)}
print("the dict values of cubes:\n",cubes)

# merging dictionaries
dict1 = {"a": 1, "b": 2}
dict2 = {"b": 3, "c": 4}
merged_dict = dict1 | dict2
print(merged_dict)  # Output: {'a': 1, 'b': 3, 'c': 4}
#Dictionary Views (, , ):These methods return "views" of the dictionary data, which are dynamic and reflect changes in the dictionary.
my_dict = {"name": "Mushtaq", "age": 25}
keys_view = my_dict.keys()
values_view = my_dict.values()
print(keys_view)    # Output: dict_keys(['name', 'age'])
print(values_view)  # Output: dict_values(['Mushtaq', 25])
#Using  for Key-Value Operations:The  method lets you work with both keys and values simultaneously in a loop.
my_dict = {"name": "Mushtaq", "age": 25, "location": "Lar"}
for key, value in my_dict.items():
    print(f"{key}: {value}")
# default dictionary
from collections import defaultdict
# Example: Counting occurrences
counter = defaultdict(int)
words = ["apple", "banana", "apple", "cherry", "banana"]
for word in words:
    counter[word] += 1
print(counter)  # Output: {'apple': 2, 'banana': 2, 'cherry': 1}

# Example: Filtering values greater than 20
my_dict = {"a": 10, "b": 30, "c": 50}
filtered_dict = {key: value for key, value in my_dict.items() if value > 20}

print(filtered_dict)
# Output: {'b': 30, 'c': 50}
