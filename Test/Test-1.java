// TestSemantico.java
public class TestSemantico {
    // 1. Campos de clase
    private String nombre;
    public int edad = 25;
    protected static final double PI = 3;
    
    // 2. Constructor con parámetros
    public TestSemantico(String nombre) {
        this.nombre = nombre; // Uso de 'this'
        
        // 3. Validación semántica (edad no negativa)
        if (this.edad < 0) {
            throw new IllegalArgumentException("Edad no puede ser negativa");
        }
    }
    
    // 4. Método con parámetros y retorno
    public String saludar(String prefijo) {
        // 5. Variable local
        String mensaje = prefijo + " " + this.nombre;
        
        // 6. Uso de campo no inicializado (debería dar warning)
        if (this.nombre == null) {
            System.out.println("Nombre no inicializado");
        }
        
        // 7. Retorno compatible
        return mensaje;
    }
    
    // 8. Sobrecarga de métodos
    public void saludar() {
        System.out.println("Hola anónimo");
    }
    
    // 9. Método estático
    public static int sumar(int a, int b) {
        return a + b;
    }
    
    // 10. Manejo de excepciones
    public void dividir(int a, int b) {
        try {
            // 11. Operación aritmética
            int resultado = a / b;
            System.out.println(resultado);
        } catch (ArithmeticException e) {
            System.err.println("División por cero");
        } finally {
            System.out.println("Operación completada");
        }
    }
    
    // 12. Clase anidada
    private class Anidada {
        private String dato;
        
        public Anidada(String dato) {
            this.dato = dato;
        }
    }
    
    // 13. Método con array
    public void procesarArray(String[] elementos) {
        // 14. Acceso a array
        String primero = elementos[0];
        
        // 15. Asignación incompatible (debería dar error)
        // int numero = primero;
        
        // 16. Iteración
        for (String elem : elementos) {
            System.out.println(elem.toUpperCase());
        }
    }
    
    public static void main(String[] args) {
        // 17. Creación de objeto
        TestSemantico test = new TestSemantico("Juan");
        
        // 18. Llamada a método
        String saludo = test.saludar("Estimado");
        System.out.println(saludo);
        
        // 19. Uso de método estático
        int total = TestSemantico.sumar(5, 3);
        System.out.println("Total: " + total);
        
        // 20. Uso de clase anidada
        Anidada anidada = test.new Anidada("Prueba");
        
        // 21. Array
        String[] nombres = {"Ana", "Carlos", "Diana"};
        test.procesarArray(nombres);
        
        // 22. División por cero (semánticamente válido, error en runtime)
        test.dividir(10, 0);
        
        // 23. Acceso a campo estático
        System.out.println("Valor de PI: " + PI);
    }
}
