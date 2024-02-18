from ezlab import main

print("IN __MAIN__")
if __name__ in {"__main__", "__mp_main__"}:
    print("HANDING TO MAIN.ENTER")
    main.enter()
