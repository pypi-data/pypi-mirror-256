from collect.coll import computing
from cli_tutor.cli import main


if __name__ == '__main__':
    main()
    info = computing.cache_info()
    print(info)