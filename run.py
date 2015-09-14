#! /usr/bin/env python
import sys
import database


def run():
        while True:
            try:
                result = process(raw_input().strip())
                if result == None:
                    continue
                if result == 'END':
                    break
                print result
            except EOFError:
                sys.exit()
            except KeyboardInterrupt:
                sys.exit()

def process(line):
    return db.dispatch(line)


if __name__ == '__main__':
    # init the database
    db = database.SimpleDB()
    run()
