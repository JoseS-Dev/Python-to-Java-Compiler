from AnalizadorSintactico import parser, lexer
class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {
            'global': {
                'classes': {},
                'variables': {},
                'functions': {}
            }
        }
        self.current_scope = 'global'
        self.current_class = None
        self.current_method = None
        self.errors = []
        self.warnings = []
        self.type_system = {
            'primitive': ['int', 'float', 'double', 'char', 'boolean', 'short', 'long', 'string', 'byte'],
            'compatible': {
                'int': ['short', 'byte', 'long'],
                'float': ['double'],
                'double': ['float'],
                'long': ['int', 'short', 'byte'],
                'short': ['byte']
            }
        }
    
    def analyze(self, ast):
        if ast[0] != 'program':
            self.add_error("El AST no comienza con un programa válido")
            return
        
        # Analizar paquete si existe
        if ast[1] is not None:
            self.analyze_package(ast[1])
        
        # Analizar imports si existen
        if ast[2] is not None:
            self.analyze_imports(ast[2])
        
        # Analizar declaraciones de clase
        if ast[3] is not None:
            for class_decl in ast[3]:
                self.analyze_class(class_decl)
        
        # Reportar resultados
        self.report_issues()
    
    def analyze_package(self, package_node):
        if package_node[0] != 'package':
            self.add_error("Nodo de paquete inválido")
            return
        
        package_name = self.get_qualified_id_name(package_node[1])
        self.symbol_table['global']['package'] = package_name
    
    def analyze_imports(self, imports):
        for import_node in imports:
            if import_node[0] != 'import':
                self.add_error("Nodo de importación inválido")
                continue
            
            import_name = self.get_qualified_id_name(import_node[1])
            if import_name not in self.symbol_table['global']['imports']:
                self.symbol_table['global']['imports'].append(import_name)
    
    def analyze_class(self, class_node):
        if class_node[0] != 'class':
            self.add_error("Nodo de clase inválido")
            return
        
        class_header = class_node[1]
        class_body = class_node[2]
        
        # Obtener información de la clase
        modifiers = []
        class_name = None
        extends = None
        implements = []
        
        if len(class_header) == 5:  # Con modificadores
            modifiers = self.get_modifiers(class_header[1])
            class_name = class_header[2]
            extends = class_header[3][1] if class_header[3] else None
            implements = [imp[1] for imp in class_header[4][1]] if class_header[4] else []
        else:  # Sin modificadores
            class_name = class_header[1]
            extends = class_header[2][1] if class_header[2] else None
            implements = [imp[1] for imp in class_header[3][1]] if class_header[3] else []
        
        # Verificar si la clase ya existe
        if class_name in self.symbol_table['global']['classes']:
            self.add_error(f"Clase '{class_name}' ya está definida")
            return
        
        # Crear entrada en la tabla de símbolos
        class_info = {
            'name': class_name,
            'modifiers': modifiers,
            'extends': extends,
            'implements': implements,
            'fields': {},
            'methods': {},
            'constructors': []
        }
        
        self.symbol_table['global']['classes'][class_name] = class_info
        self.current_class = class_name
        previous_scope = self.current_scope
        self.current_scope = class_name
        
        # Analizar miembros de la clase
        for member in class_body:
            if member[0] != 'member':
                continue
            
            member_type = member[1][0]
            if member_type == 'field':
                self.analyze_field(member[1])
            elif member_type == 'method':
                self.analyze_method(member[1])
            elif member_type == 'constructor':
                self.analyze_constructor(member[1])
            elif member_type == 'class':
                self.analyze_class(member[1])  # Clase anidada
        
        self.current_scope = previous_scope
        self.current_class = None
    
    def analyze_field(self, field_node):
        modifiers = self.get_modifiers(field_node[1])
        field_type = self.get_type_name(field_node[2])
        variables = field_node[3]
        
        for var in variables:
            var_name = var[1]
            var_init = var[2]
            
            # Verificar si el campo ya existe
            if var_name in self.symbol_table['global']['classes'][self.current_class]['fields']:
                self.add_error(f"Campo '{var_name}' ya está definido en la clase '{self.current_class}'")
                continue
            
            # Agregar a la tabla de símbolos
            field_info = {
                'name': var_name,
                'type': field_type,
                'modifiers': modifiers,
                'initialized': var_init is not None
            }
            
            self.symbol_table['global']['classes'][self.current_class]['fields'][var_name] = field_info
            
            # Analizar expresión de inicialización si existe
            if var_init is not None:
                self.analyze_expression(var_init, field_type)
    
    def analyze_method(self, method_node):
        method_header = method_node[1]
        method_body = method_node[2]
        
        modifiers = self.get_modifiers(method_header[1])
        return_type = 'void' if method_header[2] == 'void' else self.get_type_name(method_header[2])
        method_name = method_header[3]
        params = method_header[4]
        
        # Verificar si el método ya existe
        if method_name in self.symbol_table['global']['classes'][self.current_class]['methods']:
            # Verificar sobrecarga
            existing_methods = self.symbol_table['global']['classes'][self.current_class]['methods'][method_name]
            for existing in existing_methods:
                if self.compare_parameters(existing['params'], params):
                    self.add_error(f"Método '{method_name}' con los mismos parámetros ya está definido en la clase '{self.current_class}'")
                    return
        
        # Crear entrada en la tabla de símbolos
        method_info = {
            'name': method_name,
            'return_type': return_type,
            'modifiers': modifiers,
            'params': [],
            'variables': {}
        }
        
        # Analizar parámetros
        param_types = []
        for param in params:
            param_type = self.get_type_name(param[1])
            param_name = param[2]
            param_info = {
                'name': param_name,
                'type': param_type
            }
            method_info['params'].append(param_info)
            param_types.append(param_type)
        
        # Agregar método a la tabla de símbolos
        if method_name not in self.symbol_table['global']['classes'][self.current_class]['methods']:
            self.symbol_table['global']['classes'][self.current_class]['methods'][method_name] = []
        
        self.symbol_table['global']['classes'][self.current_class]['methods'][method_name].append(method_info)
        
        # Analizar cuerpo del método
        previous_method = self.current_method
        self.current_method = method_name
        previous_scope = self.current_scope
        self.current_scope = f"{self.current_class}.{method_name}"
        
        self.analyze_block(method_body, return_type)
        
        self.current_scope = previous_scope
        self.current_method = previous_method
    
    def analyze_constructor(self, constructor_node):
        modifiers = self.get_modifiers(constructor_node[1])
        constructor_name = constructor_node[2]
        params = constructor_node[3]
        body = constructor_node[4]
        
        # Verificar que el nombre coincida con la clase
        if constructor_name != self.current_class:
            self.add_error(f"El constructor '{constructor_name}' no coincide con el nombre de la clase '{self.current_class}'")
            return
        
        # Verificar si el constructor ya existe
        existing_constructors = self.symbol_table['global']['classes'][self.current_class]['constructors']
        for existing in existing_constructors:
            if self.compare_parameters(existing['params'], params):
                self.add_error(f"Constructor con los mismos parámetros ya está definido en la clase '{self.current_class}'")
                return
        
        # Crear entrada en la tabla de símbolos
        constructor_info = {
            'name': constructor_name,
            'modifiers': modifiers,
            'params': []
        }
        
        # Analizar parámetros
        for param in params:
            param_type = self.get_type_name(param[1])
            param_name = param[2]
            param_info = {
                'name': param_name,
                'type': param_type
            }
            constructor_info['params'].append(param_info)
        
        self.symbol_table['global']['classes'][self.current_class]['constructors'].append(constructor_info)
        
        # Analizar cuerpo del constructor
        previous_scope = self.current_scope
        self.current_scope = f"{self.current_class}.{constructor_name}"
        
        self.analyze_block(body, None)
        
        self.current_scope = previous_scope
    
    def analyze_block(self, block_node, expected_return_type):
        if block_node[0] != 'block':
            self.add_error("Nodo de bloque inválido")
            return
        
        statements = block_node[1]
        
        for stmt in statements:
            self.analyze_statement(stmt, expected_return_type)
    
    def analyze_statement(self, stmt_node, expected_return_type):
        if stmt_node[0] != 'statement':
            return
        
        stmt_type = stmt_node[1][0]
        
        if stmt_type == 'block':
            self.analyze_block(stmt_node[1][1], expected_return_type)
        elif stmt_type == 'if':
            self.analyze_if(stmt_node[1], expected_return_type)
        elif stmt_type == 'if-else':
            self.analyze_if_else(stmt_node[1], expected_return_type)
        elif stmt_type == 'while':
            self.analyze_while(stmt_node[1], expected_return_type)
        elif stmt_type == 'do-while':
            self.analyze_do_while(stmt_node[1], expected_return_type)
        elif stmt_type == 'for':
            self.analyze_for(stmt_node[1], expected_return_type)
        elif stmt_type == 'switch':
            self.analyze_switch(stmt_node[1], expected_return_type)
        elif stmt_type == 'return':
            self.analyze_return(stmt_node[1], expected_return_type)
        elif stmt_type == 'break':
            self.analyze_break(stmt_node[1])
        elif stmt_type == 'continue':
            self.analyze_continue(stmt_node[1])
        elif stmt_type == 'throw':
            self.analyze_throw(stmt_node[1])
        elif stmt_type == 'try-catch':
            self.analyze_try_catch(stmt_node[1], expected_return_type)
        elif stmt_type == 'try-catch-finally':
            self.analyze_try_catch_finally(stmt_node[1], expected_return_type)
        elif stmt_type == 'expr-statement':
            self.analyze_expression(stmt_node[1][1], None)
        elif stmt_type == 'local_var':
            self.analyze_local_var(stmt_node[1])
    
    def analyze_if(self, if_node, expected_return_type):
        condition = if_node[1]
        then_stmt = if_node[2]
        
        # Verificar que la condición sea booleana
        cond_type = self.analyze_expression(condition, None)
        if cond_type != 'boolean':
            self.add_error(f"La condición del if debe ser booleana, no '{cond_type}'")
        
        self.analyze_statement(then_stmt, expected_return_type)
    
    def analyze_if_else(self, if_else_node, expected_return_type):
        condition = if_else_node[1]
        then_stmt = if_else_node[2]
        else_stmt = if_else_node[3]
        
        # Verificar que la condición sea booleana
        cond_type = self.analyze_expression(condition, None)
        if cond_type != 'boolean':
            self.add_error(f"La condición del if-else debe ser booleana, no '{cond_type}'")
        
        self.analyze_statement(then_stmt, expected_return_type)
        self.analyze_statement(else_stmt, expected_return_type)
    
    def analyze_while(self, while_node, expected_return_type):
        condition = while_node[1]
        body = while_node[2]
        
        # Verificar que la condición sea booleana
        cond_type = self.analyze_expression(condition, None)
        if cond_type != 'boolean':
            self.add_error(f"La condición del while debe ser booleana, no '{cond_type}'")
        
        self.analyze_statement(body, expected_return_type)
    
    def analyze_do_while(self, do_while_node, expected_return_type):
        body = do_while_node[1]
        condition = do_while_node[2]
        
        self.analyze_statement(body, expected_return_type)
        
        # Verificar que la condición sea booleana
        cond_type = self.analyze_expression(condition, None)
        if cond_type != 'boolean':
            self.add_error(f"La condición del do-while debe ser booleana, no '{cond_type}'")
    
    def analyze_for(self, for_node, expected_return_type):
        init = for_node[1]
        condition = for_node[2]
        update = for_node[3]
        body = for_node[4]
        
        # Analizar inicialización
        if init[0] == 'for_init':
            if init[1][0] == 'local_var':
                self.analyze_local_var(init[1])
            else:  # expression_list
                for expr in init[1][1]:
                    self.analyze_expression(expr, None)
        
        # Verificar que la condición sea booleana o vacía
        if condition is not None:
            cond_type = self.analyze_expression(condition, None)
            if cond_type != 'boolean':
                self.add_error(f"La condición del for debe ser booleana, no '{cond_type}'")
        
        # Analizar actualización
        if update[0] == 'for_update':
            for expr in update[1][1]:
                self.analyze_expression(expr, None)
        
        # Analizar cuerpo
        self.analyze_statement(body, expected_return_type)
    
    def analyze_switch(self, switch_node, expected_return_type):
        expr = switch_node[1]
        cases = switch_node[2]
        
        # Analizar expresión del switch
        expr_type = self.analyze_expression(expr, None)
        if expr_type not in ['int', 'char', 'short', 'byte', 'string', 'enum']:
            self.add_error(f"La expresión del switch debe ser de tipo entero, char o string, no '{expr_type}'")
        
        # Analizar casos
        for case in cases:
            if case[0] == 'case':
                case_expr = case[1]
                stmts = case[2]
                
                case_type = self.analyze_expression(case_expr, None)
                if not self.are_types_compatible(expr_type, case_type):
                    self.add_error(f"Tipo de caso '{case_type}' no compatible con tipo de switch '{expr_type}'")
                
                for stmt in stmts:
                    self.analyze_statement(stmt, expected_return_type)
            else:  # default
                stmts = case[1]
                for stmt in stmts:
                    self.analyze_statement(stmt, expected_return_type)
    
    def analyze_return(self, return_node, expected_return_type):
        if len(return_node) == 2:  # return con expresión
            expr = return_node[1]
            return_type = self.analyze_expression(expr, None)
            
            if expected_return_type == 'void':
                self.add_error("No se puede retornar un valor en un método void")
            elif not self.are_types_compatible(expected_return_type, return_type):
                self.add_error(f"Tipo de retorno '{return_type}' no compatible con el tipo esperado '{expected_return_type}'")
        else:  # return sin expresión
            if expected_return_type != 'void':
                self.add_error(f"Se esperaba retornar un valor de tipo '{expected_return_type}'")
    
    def analyze_break(self, break_node):
        # Verificación de break en contexto válido (implementar lógica según necesidad)
        pass
    
    def analyze_continue(self, continue_node):
        # Verificación de continue en contexto válido (implementar lógica según necesidad)
        pass
    
    def analyze_throw(self, throw_node):
        expr = throw_node[1]
        expr_type = self.analyze_expression(expr, None)
        
        if expr_type != 'Throwable' and not self.is_subclass(expr_type, 'Throwable'):
            self.add_error(f"Solo se pueden lanzar excepciones, no '{expr_type}'")
    
    def analyze_try_catch(self, try_catch_node, expected_return_type):
        try_block = try_catch_node[1]
        catches = try_catch_node[2]
        
        self.analyze_block(try_block, expected_return_type)
        
        for catch in catches:
            param = catch[1]
            catch_block = catch[2]
            
            param_type = param[1]
            param_name = param[2]
            
            # Verificar que el tipo sea Throwable
            if param_type != 'Throwable' and not self.is_subclass(param_type, 'Throwable'):
                self.add_error(f"El tipo de catch debe ser Throwable, no '{param_type}'")
            
            # Analizar bloque catch
            previous_scope = self.current_scope
            self.current_scope = f"{previous_scope}.catch({param_type} {param_name})"
            
            self.analyze_block(catch_block, expected_return_type)
            
            self.current_scope = previous_scope
    
    def analyze_try_catch_finally(self, try_catch_finally_node, expected_return_type):
        try_block = try_catch_finally_node[1]
        catches = try_catch_finally_node[2]
        finally_block = try_catch_finally_node[3]
        
        self.analyze_block(try_block, expected_return_type)
        
        for catch in catches:
            param = catch[1]
            catch_block = catch[2]
            
            param_type = param[1]
            param_name = param[2]
            
            # Analizar bloque catch
            previous_scope = self.current_scope
            self.current_scope = f"{previous_scope}.catch({param_type} {param_name})"
            
            self.analyze_block(catch_block, expected_return_type)
            
            self.current_scope = previous_scope
        
        self.analyze_block(finally_block, expected_return_type)
    
    def analyze_local_var(self, local_var_node):
        var_type = self.get_type_name(local_var_node[1])
        variables = local_var_node[2]
        
        for var in variables:
            var_name = var[1]
            var_init = var[2]
            
            # Verificar si la variable ya existe en el ámbito actual
            if self.is_variable_defined(var_name):
                self.add_error(f"Variable '{var_name}' ya está definida en este ámbito")
                continue
            
            # Agregar a la tabla de símbolos
            var_info = {
                'name': var_name,
                'type': var_type,
                'initialized': var_init is not None
            }
            
            # Determinar dónde guardar la variable
            if self.current_method:
                method_info = self.get_current_method_info()
                method_info['variables'][var_name] = var_info
            elif self.current_class:
                class_info = self.symbol_table['global']['classes'][self.current_class]
                class_info['fields'][var_name] = var_info
            else:
                self.symbol_table['global']['variables'][var_name] = var_info
            
            # Analizar expresión de inicialización si existe
            if var_init is not None:
                init_type = self.analyze_expression(var_init, None)
                if not self.are_types_compatible(var_type, init_type):
                    self.add_error(f"No se puede asignar '{init_type}' a variable de tipo '{var_type}'")
    
    def analyze_expression(self, expr_node, expected_type):
        if not isinstance(expr_node, tuple):
            return 'unknown'
        
        expr_type = expr_node[0]
        
        if expr_type == 'assign':
            return self.analyze_assignment(expr_node, expected_type)
        elif expr_type == 'binary':
            return self.analyze_binary_operation(expr_node, expected_type)
        elif expr_type == 'unary':
            return self.analyze_unary_operation(expr_node, expected_type)
        elif expr_type == 'ternary':
            return self.analyze_ternary_operation(expr_node, expected_type)
        elif expr_type == 'postfix':
            return self.analyze_postfix_operation(expr_node, expected_type)
        elif expr_type == 'array_access':
            return self.analyze_array_access(expr_node, expected_type)
        elif expr_type == 'member_access':
            return self.analyze_member_access(expr_node, expected_type)
        elif expr_type == 'method_call':
            return self.analyze_method_call(expr_node, expected_type)
        elif expr_type == 'new':
            return self.analyze_new_expression(expr_node, expected_type)
        elif expr_type == 'primary':
            return self.analyze_primary(expr_node[1], expected_type)
        elif expr_type == 'literal':
            return self.analyze_literal(expr_node[1], expected_type)
        elif expr_type == 'id':
            return self.analyze_identifier(expr_node[1], expected_type)
        elif expr_type == 'qualified':
            return self.analyze_qualified_id(expr_node, expected_type)
        else:
            self.add_error(f"Expresión de tipo desconocido: {expr_type}")
            return 'unknown'
    
    def analyze_assignment(self, assign_node, expected_type):
        var_name = assign_node[1]
        op = assign_node[2][1]  # operador de asignación
        expr = assign_node[3]
        
        # Obtener información de la variable
        var_info = self.get_variable_info(var_name)
        if not var_info:
            self.add_error(f"Variable '{var_name}' no está definida")
            return 'unknown'
        
        # Analizar expresión del lado derecho
        expr_type = self.analyze_expression(expr, var_info['type'])
        
        # Verificar compatibilidad de tipos
        if not self.are_types_compatible(var_info['type'], expr_type):
            self.add_error(f"No se puede asignar '{expr_type}' a variable de tipo '{var_info['type']}'")
        
        # Verificar operadores de asignación compuestos
        if op != '=':
            # Para operadores como +=, -=, etc., verificar que el tipo soporte la operación
            if not self.supports_operation(var_info['type'], op[:-1]):
                self.add_error(f"Operador '{op}' no soportado para tipo '{var_info['type']}'")
        
        return var_info['type']
    
    def analyze_binary_operation(self, binary_node, expected_type):
        operator = binary_node[1]
        left = binary_node[2]
        right = binary_node[3]
        
        left_type = self.analyze_expression(left, None)
        right_type = self.analyze_expression(right, None)
        
        # Verificar compatibilidad de tipos
        if not self.are_types_compatible(left_type, right_type):
            self.add_error(f"Tipos incompatibles en operación binaria: '{left_type}' y '{right_type}'")
            return 'unknown'
        
        # Determinar tipo de retorno basado en el operador
        if operator in ['+', '-', '*', '/', '%', '<<', '>>', '&', '|', '^']:
            # Operadores aritméticos y de bits
            if left_type in ['int', 'short', 'byte', 'long', 'char']:
                return self.get_numeric_result_type(left_type, right_type)
            else:
                self.add_error(f"Operador '{operator}' no soportado para tipo '{left_type}'")
                return 'unknown'
        elif operator in ['&&', '||']:
            # Operadores lógicos
            if left_type == 'boolean':
                return 'boolean'
            else:
                self.add_error(f"Operador '{operator}' requiere operandos booleanos, no '{left_type}'")
                return 'boolean'
        elif operator in ['==', '!=', '<', '>', '<=', '>=']:
            # Operadores de comparación
            return 'boolean'
        else:
            self.add_error(f"Operador binario desconocido: '{operator}'")
            return 'unknown'
    
    def analyze_unary_operation(self, unary_node, expected_type):
        operator = unary_node[1]
        expr = unary_node[2]
        
        expr_type = self.analyze_expression(expr, None)
        
        if operator in ['++', '--']:
            if expr_type not in ['int', 'short', 'byte', 'long', 'char', 'float', 'double']:
                self.add_error(f"Operador '{operator}' no soportado para tipo '{expr_type}'")
            return expr_type
        elif operator in ['+', '-']:
            if expr_type not in ['int', 'short', 'byte', 'long', 'char', 'float', 'double']:
                self.add_error(f"Operador '{operator}' no soportado para tipo '{expr_type}'")
            return expr_type
        elif operator == '!':
            if expr_type != 'boolean':
                self.add_error(f"Operador '!' requiere operando booleano, no '{expr_type}'")
            return 'boolean'
        elif operator == '~':
            if expr_type not in ['int', 'short', 'byte', 'long', 'char']:
                self.add_error(f"Operador '~' no soportado para tipo '{expr_type}'")
            return expr_type
        else:
            self.add_error(f"Operador unario desconocido: '{operator}'")
            return 'unknown'
    
    def analyze_ternary_operation(self, ternary_node, expected_type):
        condition = ternary_node[1]
        true_expr = ternary_node[2]
        false_expr = ternary_node[3]
        
        cond_type = self.analyze_expression(condition, None)
        if cond_type != 'boolean':
            self.add_error(f"La condición en operador ternario debe ser booleana, no '{cond_type}'")
        
        true_type = self.analyze_expression(true_expr, expected_type)
        false_type = self.analyze_expression(false_expr, expected_type)
        
        if not self.are_types_compatible(true_type, false_type):
            self.add_error(f"Tipos incompatibles en operador ternario: '{true_type}' y '{false_type}'")
            return 'unknown'
        
        return true_type
    
    def analyze_postfix_operation(self, postfix_node, expected_type):
        expr = postfix_node[1]
        operator = postfix_node[2]
        
        expr_type = self.analyze_expression(expr, None)
        
        if operator in ['++', '--']:
            if expr_type not in ['int', 'short', 'byte', 'long', 'char', 'float', 'double']:
                self.add_error(f"Operador '{operator}' no soportado para tipo '{expr_type}'")
        
        return expr_type
    
    def analyze_array_access(self, array_access_node, expected_type):
        array_expr = array_access_node[1]
        index_expr = array_access_node[2]
        
        array_type = self.analyze_expression(array_expr, None)
        index_type = self.analyze_expression(index_expr, None)
        
        if not array_type.endswith('[]'):
            self.add_error(f"Intento de acceso a array en variable no-array de tipo '{array_type}'")
            return 'unknown'
        
        if index_type != 'int':
            self.add_error(f"Índice de array debe ser int, no '{index_type}'")
        
        return array_type[:-2]  # Eliminar los [] para obtener el tipo base
    
    def analyze_member_access(self, member_access_node, expected_type):
        object_expr = member_access_node[1]
        member = member_access_node[2]
        
        object_type = self.analyze_expression(object_expr, None)
        
        if member[0] == 'member':
            member_name = member[1]
            
            # Buscar el miembro en la clase del objeto
            if object_type in self.symbol_table['global']['classes']:
                class_info = self.symbol_table['global']['classes'][object_type]
                
                # Buscar campo
                if member_name in class_info['fields']:
                    return class_info['fields'][member_name]['type']
                
                # Buscar método (simplificado)
                if member_name in class_info['methods']:
                    # Para simplificar, asumimos que el tipo de retorno es el del primer método encontrado
                    return class_info['methods'][member_name][0]['return_type']
            
            self.add_error(f"Miembro '{member_name}' no encontrado en tipo '{object_type}'")
            return 'unknown'
        
        elif member[0] == 'new_member':
            return self.analyze_new_expression(member, expected_type)
        
        else:
            self.add_error(f"Tipo de acceso a miembro desconocido: {member[0]}")
            return 'unknown'
    
    def analyze_method_call(self, method_call_node, expected_type):
        method_name = method_call_node[1]
        args = method_call_node[2][1] if method_call_node[2] else []
        
        # Buscar el método en la clase actual
        if self.current_class and method_name in self.symbol_table['global']['classes'][self.current_class]['methods']:
            methods = self.symbol_table['global']['classes'][self.current_class]['methods'][method_name]
            
            # Buscar método con parámetros compatibles (simplificado)
            for method in methods:
                if len(method['params']) == len(args):
                    match = True
                    for param, arg in zip(method['params'], args):
                        arg_type = self.analyze_expression(arg, None)
                        if not self.are_types_compatible(param['type'], arg_type):
                            match = False
                            break
                    
                    if match:
                        return method['return_type']
            
            self.add_error(f"No se encontró método '{method_name}' con parámetros compatibles")
            return 'unknown'
        
        # Si no está en la clase actual, verificar si es un método estático de otra clase
        elif method_name in ['this', 'super']:
            # Manejo especial para this y super
            return self.current_class if method_name == 'this' else self.get_super_class()
        
        else:
            self.add_error(f"Método '{method_name}' no definido")
            return 'unknown'
    
    def analyze_new_expression(self, new_node, expected_type):
        creator = new_node[1]
        
        if creator[0] == 'creator':
            created_type = creator[1][1] if isinstance(creator[1], tuple) else creator[1]  # Manejar qualified_id
            args = creator[2][1] if creator[2] else []
            
            # Verificar que el tipo exista
            if created_type not in self.symbol_table['global']['classes'] and created_type not in self.type_system['primitive']:
                self.add_error(f"Tipo '{created_type}' no definido")
                return 'unknown'
            
            # Verificar constructor (simplificado)
            if created_type in self.symbol_table['global']['classes']:
                class_info = self.symbol_table['global']['classes'][created_type]
                
                # Buscar constructor con parámetros compatibles
                for constructor in class_info['constructors']:
                    if len(constructor['params']) == len(args):
                        match = True
                        for param, arg in zip(constructor['params'], args):
                            arg_type = self.analyze_expression(arg, None)
                            if not self.are_types_compatible(param['type'], arg_type):
                                match = False
                                break
                        
                        if match:
                            return created_type
                
                self.add_error(f"No se encontró constructor compatible para '{created_type}'")
            
            return created_type
        else:
            self.add_error("Expresión 'new' inválida")
            return 'unknown'
    
    def analyze_primary(self, primary_node, expected_type):
        if isinstance(primary_node, tuple):
            if primary_node[0] == 'literal':
                return self.analyze_literal(primary_node[1], expected_type)
            elif primary_node[0] == 'id':
                return self.analyze_identifier(primary_node[1], expected_type)
            elif primary_node[0] == 'qualified':
                return self.analyze_qualified_id(primary_node, expected_type)
            else:
                return self.analyze_expression(primary_node, expected_type)
        else:
            # Puede ser un literal simple como número o string
            return self.analyze_literal(primary_node, expected_type)
    
    def analyze_literal(self, literal, expected_type):
        if isinstance(literal, str):
            if literal.startswith('"') and literal.endswith('"'):
                return 'string'
            elif literal.startswith("'") and literal.endswith("'"):
                return 'char'
            elif literal in ['true', 'false']:
                return 'boolean'
            elif literal == 'null':
                return 'null'
        elif isinstance(literal, int):
            return 'int'
        elif isinstance(literal, float):
            return 'float'
        
        return 'unknown'
    
    def analyze_identifier(self, identifier, expected_type):
        var_info = self.get_variable_info(identifier)
        if not var_info:
            self.add_error(f"Variable '{identifier}' no definida")
            return 'unknown'
        
        return var_info['type']
    
    def analyze_qualified_id(self, qualified_node, expected_type):
        if len(qualified_node) == 3:  # qualified_id : ID PUNTO ID
            left = qualified_node[1]
            right = qualified_node[2]
            
            # Buscar el tipo del lado izquierdo
            left_type = None
            if left in self.symbol_table['global']['classes']:
                left_type = left
            else:
                var_info = self.get_variable_info(left)
                if var_info:
                    left_type = var_info['type']
            
            if not left_type:
                self.add_error(f"Identificador '{left}' no definido")
                return 'unknown'
            
            # Buscar el miembro en el tipo
            if left_type in self.symbol_table['global']['classes']:
                class_info = self.symbol_table['global']['classes'][left_type]
                
                # Buscar campo
                if right in class_info['fields']:
                    return class_info['fields'][right]['type']
                
                # Buscar método (simplificado)
                if right in class_info['methods']:
                    return class_info['methods'][right][0]['return_type']
            
            self.add_error(f"Miembro '{right}' no encontrado en tipo '{left_type}'")
            return 'unknown'
        else:  # qualified_id : ID
            return self.analyze_identifier(qualified_node[1], expected_type)
    
    # Funciones auxiliares
    def get_modifiers(self, modifiers_node):
        if not modifiers_node:
            return []
        return [mod[1] for mod in modifiers_node[1]] if isinstance(modifiers_node, tuple) else []
    
    def get_type_name(self, type_node):
        if not type_node:
            return 'void'
        
        if type_node[0] == 'type':
            inner_type = type_node[1]
            if inner_type[0] == 'primitive':
                return inner_type[1].lower()
            elif inner_type[0] == 'reference':
                return self.get_qualified_id_name(inner_type[1])
        elif type_node[0] == 'array_type':
            base_type = self.get_type_name(type_node[1])
            return f"{base_type}[]"
        
        return 'unknown'
    
    def get_qualified_id_name(self, qualified_node):
        if qualified_node[0] == 'qualified':
            return f"{qualified_node[1]}.{qualified_node[2]}"
        elif qualified_node[0] == 'id':
            return qualified_node[1]
        else:
            return 'unknown'
    
    def compare_parameters(self, params1, params2):
        if len(params1) != len(params2):
            return False
        
        for p1, p2 in zip(params1, params2):
            type1 = p1['type'] if isinstance(p1, dict) else self.get_type_name(p2[1])
            type2 = self.get_type_name(p2[1])
            
            if type1 != type2:
                return False
        
        return True
    
    def are_types_compatible(self, target_type, source_type):
        if target_type == source_type:
            return True
        
        # Compatibilidad numérica
        if target_type in self.type_system['compatible'] and source_type in self.type_system['compatible'][target_type]:
            return True
        
        # Null puede asignarse a cualquier tipo de referencia
        if source_type == 'null' and target_type not in self.type_system['primitive']:
            return True
        
        # Verificar herencia (simplificado)
        if target_type in self.symbol_table['global']['classes'] and source_type in self.symbol_table['global']['classes']:
            current = source_type
            while current:
                if current == target_type:
                    return True
                
                class_info = self.symbol_table['global']['classes'][current]
                current = class_info['extends']
        
        return False
    
    def supports_operation(self, type_name, operator):
        if operator in ['+', '-', '*', '/', '%']:
            return type_name in ['int', 'short', 'byte', 'long', 'char', 'float', 'double']
        elif operator in ['&', '|', '^', '<<', '>>']:
            return type_name in ['int', 'short', 'byte', 'long', 'char']
        else:
            return False
    
    def get_numeric_result_type(self, type1, type2):
        types = [type1, type2]
        
        if 'double' in types:
            return 'double'
        elif 'float' in types:
            return 'float'
        elif 'long' in types:
            return 'long'
        else:
            return 'int'
    
    def is_variable_defined(self, var_name):
        # Buscar en el ámbito actual (método)
        if self.current_method:
            method_info = self.get_current_method_info()
            if var_name in method_info['variables']:
                return True
        
        # Buscar en la clase actual (campos)
        if self.current_class:
            class_info = self.symbol_table['global']['classes'][self.current_class]
            if var_name in class_info['fields']:
                return True
        
        # Buscar en ámbito global
        if var_name in self.symbol_table['global']['variables']:
            return True
        
        return False
    
    def get_variable_info(self, var_name):
        # Buscar en el ámbito actual (método)
        if self.current_method:
            method_info = self.get_current_method_info()
            if var_name in method_info['variables']:
                return method_info['variables'][var_name]
            
            # Buscar en parámetros del método
            for param in method_info['params']:
                if param['name'] == var_name:
                    return param
        
        # Buscar en la clase actual (campos)
        if self.current_class:
            class_info = self.symbol_table['global']['classes'][self.current_class]
            if var_name in class_info['fields']:
                return class_info['fields'][var_name]
        
        # Buscar en ámbito global
        if var_name in self.symbol_table['global']['variables']:
            return self.symbol_table['global']['variables'][var_name]
        
        return None
    
    def get_current_method_info(self):
        if not self.current_method or not self.current_class:
            return None
        
        methods = self.symbol_table['global']['classes'][self.current_class]['methods'].get(self.current_method, [])
        # Para simplificar, devolvemos el primer método (no manejamos sobrecarga correctamente aquí)
        return methods[0] if methods else None
    
    def get_super_class(self):
        if not self.current_class:
            return None
        
        class_info = self.symbol_table['global']['classes'][self.current_class]
        return class_info['extends']
    
    def is_subclass(self, child_class, parent_class):
        current = child_class
        while current:
            if current == parent_class:
                return True
            
            if current not in self.symbol_table['global']['classes']:
                return False
            
            class_info = self.symbol_table['global']['classes'][current]
            current = class_info['extends']
        
        return False
    
    def add_error(self, message):
        self.errors.append(f"Error semántico: {message}")
    
    def add_warning(self, message):
        self.warnings.append(f"Advertencia: {message}")
    
    def report_issues(self):
        
        
        for error in self.errors:
            print(error)
        
        for warning in self.warnings:
            print(warning)
        
        print(f"\nTotal: {len(self.errors)} errores, {len(self.warnings)} advertencias.")

# Uso del analizador semántico
if __name__ == '__main__':
    filename = 'Test/Test-3.java'
    try:
        with open(filename, 'r') as f:
            java_code = f.read()
        
        # Primero parsear el código
        ast = parser.parse(java_code, lexer=lexer, debug=False)
        
        # Luego analizar semánticamente
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
    except FileNotFoundError:
        print(f"Error: Archivo no encontrado - {filename}")
    except Exception as e:
        print(f"Error durante el análisis: {str(e)}")


