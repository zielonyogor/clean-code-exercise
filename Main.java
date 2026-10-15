import java.nio.file.*;
import java.util.*;

public class Main {
    public interface Everything {
        void send(String x);
        void save(String x) throws Exception;
        void refund(double x);
    }
    public static class Thing implements Everything {
        public void send(String x) { System.out.println("EMAIL " + x); }
        public void save(String x) throws Exception {
            Files.writeString(Path.of("orders.txt"), x + "\n", StandardOpenOption.CREATE, StandardOpenOption.APPEND);
        }
        public void refund(double x) { throw new UnsupportedOperationException("Not supported"); }
    }
    static String mode = "production";
    static int counter = 0;
    static double total = 0;
    static Map<String, String> cache = new HashMap<>();
    static String[] futureCurrencies = {"EUR", "USD", "BTC", "POINTS"};

    static String doIt(String s, int action, boolean verbose, boolean send, boolean save, int unused) {
        try {
            if (action == 2) {
                String x = "REPORT|" + counter + "|" + String.format(Locale.ROOT, "%.2f", total);
                if (verbose) System.out.println(x);
                return x;
            }
            if (action != 1) return "UNKNOWN";
            String[] a = s.split("\\|", -1);
            String n = a[0], e = a[1], t = a[2];
            String[] b = a[3].split(",");
            double z = 0;
            String detail = "";
            for (String q : b) {
                String[] c = q.split(":");
                double p;
                if (c[0].equals("BOOK")) p = 40;
                else if (c[0].equals("PEN")) p = 5;
                else if (c[0].equals("BAG")) p = 80;
                else p = 0;
                z += p * Integer.parseInt(c[1]);
                detail += c[0] + "x" + c[1] + ";";
            }
            if (t.equals("VIP")) z *= 0.9;
            else if (t.equals("STUDENT")) z *= 0.95;
            if (a[4].equals("SAVE10")) z *= 0.9;
            if (z < 100) z += 12;
            z *= 1.23;
            String x = "ORDER|" + n + "|" + detail + "|" + String.format(Locale.ROOT, "%.2f", z);
            counter++;
            total += z;
            cache.put(e, x);
            Thing obj = new Thing();
            if (save) obj.save(x);
            if (send) obj.send(e + "|" + x);
            if (verbose) System.out.println(x);
            return x;
        } catch (Exception ex) { return "ERROR"; }
    }
    public static void main(String[] args) {
        doIt("Alice|alice@example.test|VIP|BOOK:2,PEN:3|SAVE10", 1, true, true, true, 999);
        doIt("Bob|bob@example.test|REGULAR|BAG:2|NONE", 1, true, true, true, 999);
        doIt("", 2, true, false, false, 999);
    }
}
