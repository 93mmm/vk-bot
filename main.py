import tests
import bot

def main():
    tests.test()
    current_session = bot.Bot()
    current_session.test_write() 


if __name__ == "__main__":
    main()
