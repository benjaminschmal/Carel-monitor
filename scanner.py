from database import init_database

from core.scanner import Scanner


if __name__ == "__main__":

    init_database()

    Scanner().run()