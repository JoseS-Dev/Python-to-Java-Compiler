class AnalizadorSemantico:
    def __init__(self):
        self.tabla_simbolos = {
            'global': {
                'clases': {},
                'variables': {},
                'funciones': {}
            }
        }
        self.current_scope = 'global'
        self.current_class = None
        self.current_method = None
        self.errors = []
        self.Warning = []
        self.type_system = {
            'primitive': [ 'int', 'float', 'double', 'char', 'boolean', 'string', 'short', 'long', 'byte'],
            'compatible': {
                'int': ['long', 'short', 'byte'],
                'float': ['double'],
                'double': ['float'],
                'long': ['int', 'short', 'byte'],
                'short': ['byte']
            }
        }