public class Test2 {
    public static void main(String args) {
        final int value1 = 1;
        int value2 = 2;
        int value3 = 3;
        int value4 = 4;
        int value5 = 5;
        String myPhrase;
        boolean myBoolean = false;
        float myFloat;

        if (false) {
            return;
        }
        value2++;
        while (value3 < 10) {
            value2++;
        }
        int newValue;
        for (newValue = 2; newValue < 4; newValue++) {
            newValue++;
        }
        int sum = value1 + value2 + value3 + value4 + value5;
        System.out.println(sum);
    }
}