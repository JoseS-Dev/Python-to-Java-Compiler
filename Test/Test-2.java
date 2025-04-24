public class TestSemantico {
    // 1. Atributo privado
    private String nombre;
    
    
    
    // 3. Método público
    public String saludar(String saludo) {
        // 4. Variable local
        String mensaje = saludo + " " + nombre;
        
        // 5. Condicional
        if (nombre.equals("Juan")) {
            mensaje += " (especial)";
        } else {
            mensaje += " (normal)";
        }
        
        // 6. Bucle for
        for (int i = 0; i < 3; i++) {
            System.out.println(mensaje);
        }
        
        return mensaje; // Faltaba el return
    }
}