class AnalizadorSemantico:
    def __init__(self):
        self.tabla_simbolos = {
            'global': {
                'clases': {},
                'variables': {},
                'funciones': {},
                'packages': {},
                'imports': {}
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
    
    # Funcion para analizar el AST (Abstract Syntax Tree)
    def analizar(self, ast):
        if ast[0] != 'program':
            self.errors.append(f"Error: El AST no es un programa válido.")
            return

        if ast[1] is not None:
            self.analizar_package(ast[1])
        
        if ast[2] is not None:
            self.analizar_imports(ast[2])
        
        if ast[3] is not None:
            for clase in ast[3]:
                self.analizar_clase(clase)
        
        # Se hace un reporte de los resultados
        self.reporte_issues()
    
    # Funcion para analizar los paquetes o el paquete
    def analizar_package(self, package):
        if package[0] != 'package':
            self.add_errores(f'El nodo de paquetes no es valido')
            return
        package_name = self.get_qualified_id_name(package[1])
        if package_name in self.tabla_simbolos[self.current_scope]['packages']:
            self.add_errores(f'El paquete {package_name} ya existe')
        else:
            self.tabla_simbolos[self.current_scope]['packages'][package_name] = package_name
    
    # Funcion para analizar los imports
    def analizar_imports(self, imports):
        if imports[0] != 'import':
            self.add_errores(f'El nodo de imports no es valido')
            return
        import_name = self.get_qualified_id_name(imports[1])
        if import_name in self.tabla_simbolos[self.current_scope]['imports']:
            self.add_errores(f'El import {import_name} ya existe')
        else:
            self.tabla_simbolos[self.current_scope]['imports'][import_name] = import_name
    
    # Funcion para analizar las clases
    def analizar_clase(self, clase):
        if clase[0] != 'class':
            self.add_errores(f'El nodo de clase no es valido')
            return
        class_header = clase[1]
        class_body = clase[2]

        # Se obtiene la informacion de la clase
        modifiers = []
        class_name = None
        extends = None
        implements = []

        if len(class_header) == 5: # clase con modificadores
            modifiers = self.get_modifiers(class_header[1])
            class_name = class_header[2]
            extends = class_header[3][1] if class_header[3] else None
            implements = [imp[1] for imp in class_header[4][1]] if class_header[4] else []
        
        else: # clase sin modificadores
            class_name = class_header[1]
            extends = class_header[2][1] if class_header[2] else None
            implements = [imp[1] for imp in class_header[3][1]] if class_header[3] else []
        
        # Se verifica si la clase ya existe
        if class_name in self.tabla_simbolos[self.current_scope]['clases']:
            self.add_errores(f'La clase {class_name} ya existe')
            return

        # Se crea las entradas en la tabla de simbolos
        class_info = {
            'name': class_name,
            'modifiers': modifiers,
            'extends': extends,
            'implements': implements,
            'fields': {},
            'methods': {},
            'constructors': [],
        }
        self.tabla_simbolos['global']['clases'][class_name] = class_info
        self.current_class = class_name
        previous_scope = self.current_scope
        self.current_scope = class_name

        # Se analiza los miembros de la clase
        for member in class_body:
            if member[0] != 'member':
                self.add_errores(f'El nodo de miembro no es valido')
                continue
            member_type = member[1][0]
            if member_type == 'field':
                self.analizar_field(member[1])
            elif member_type == 'method':
                self.analizar_metodos(member[1])
            elif member_type == 'constructor':
                self.analizar_constructor(member[1])
            elif member_type == 'class':
                self.analizar_clase(member[1]) # Clase anidada
        
        self.current_scope = previous_scope
        self.current_class = None
    
    # Funcion que analiza los field o variables de la clase
    def analizar_field(self, field):
        modifiers = self.get_modifiers(field[1])
        field_type = self.get_type_name(field[2])
        variables = field[3]

        for var in variables:
            var_name = var[1]
            var_init = var[2]
            if var_name in self.tabla_simbolos['global']['clases'][self.current_class]['fields']:
                self.add_errores(f'La variable {var_name} ya existe en la clase {self.current_class}')
                continue

            # Se agrega a la tabla de simbolos
            field_info = {
                'name': var_name,
                'type': field_type,
                'modifiers': modifiers,
                'initialized': var_init is not None,
            }

            self.tabla_simbolos['global']['clases'][self.current_class]['fields'][var_name] = field_info
            # Una validacion para analizar la expresion de inicialización si existe
            if var_init is not None:
                self.analizar_expression(var_init, field_type)


