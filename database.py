class SimpleDB(object):
    def __init__(self):
         # database implemented as a dictionary
         self.data = {}
         # Cache to keep track of commands in transaction
         self.cache = []


    def dispatch(self, line):
        """ dispatch to different methods depending on the user command """
        commands = line.split()

        if commands[0].upper() == 'SET':
            key = commands[1]
            val = int(commands[2])
            return self.set(key, val)

        elif commands[0].upper() == 'GET':
            key = commands[1]
            return self.get(key)

        elif commands[0].upper() == 'UNSET':
            key = commands[1]
            return self.unset(key)

        elif commands[0].upper() == 'NUMEQUALTO':
            val = int(commands[1])
            return self.num_equal_to(val)

        elif commands[0].upper() == 'BEGIN':
            return self._begin()

        elif commands[0].upper() == 'COMMIT':
            return self._commit()

        elif commands[0].upper() == 'ROLLBACK':
            return self._rollback()

        elif commands[0].upper() == 'END':
            return self._end()

        else:
            return "Invalid Command!"

    def set(self, key, value, rollback=False):
        """ Set the variable name to the <value>  """
        if not rollback:
            if len(self.cache):
                self.cache[-1].append(['SET', key, value, self.get(key)])

        self.data[key] = value

    def get(self, key):
        """ Print out the value of the variable name or NULL if that variable not set. """
        return self.data.get(key, "NULL")

    def unset(self, key, rollback=False):
        """ Unset the variable name, making it like it was never set. """
        if not rollback:
            if len(self.cache):
                self.cache[-1].append(['UNSET', key, self.get(key)])

        if key in self.data.keys():
            del self.data[key]
        else:
            raise KeyError("Name key is not in the data")

    def num_equal_to(self, value):
        """ Print out the number of variables that are currently set to value. If no variables equal that value, print 0. """
        return self.data.values().count(value)

    def _begin(self):
        """ Open a new transaction block. Transaction blocks can be nested; a BEGIN can be issued inside of an existing block. """
        self.cache.append([])

    def _rollback(self):
        """ Undo all of the commands issued in the most recent transaction block, and close the block.
        Print nothing if successful, or print NO TRANSACTION if no transaction is in progress """
        if self.cache:
            last_command = self.cache.pop()
            for arg in last_command:
                if arg[0].upper() == 'SET':
                    if arg[-1] == 'NULL':
                        key = arg[1]
                        self.unset(key, True)
                    else:
                        key = arg[1]
                        val = int(arg[-1])
                        self.set(key, val, True)

                elif arg[0].upper() == 'UNSET':
                    key = arg[1]
                    val = int(arg[2])
                    self.set(key, val, True)
        else:
            return  "NO TRANSACTION"

    def _commit(self):
        """ Close all open transaction blocks, permanently applying the changes made in them.
        Print nothing if successful, or print NO TRANSACTION if no transaction is in progress. """
        self.cache = []

    def _end(self):
        return 'END'
