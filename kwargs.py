def print_address(*args, **kwargs):
    for arg in args:
        print(arg, end=" ")
    print()

    print(type(kwargs))

    for key, values in kwargs.items():
        print(f"{key}:{values}")

    for key in kwargs.keys():
        print(key)

    print(f"{kwargs.get('street')}")
    print(f"{kwargs.get('city')}")
    print(f"{kwargs.get('state')}")


print_address("Ashish", "Raj", "Singh",
              street="#3451",
              city="hyderabad",
              state="telangana")
