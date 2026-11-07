import time
import csv
import matplotlib.pyplot as plt
import random
import sys

# Optimización para manejar enteros gigantescos en Python si es necesario
sys.set_int_max_str_digits(100000)

class ModularExponentiation:
    """Clase que agrupa las implementaciones de la exponenciación modular."""
    
    @staticmethod
    def naive_exponentiation(base: int, exponent: int, modulus: int) -> int:
        """
        Implementación Lineal Ingenua.
        Multiplica la base 'b' veces aplicando el módulo en cada paso.
        Complejidad Temporal: O(b)
        Complejidad Espacial: O(1)
        """
        if modulus == 1:
            return 0
        result = 1
        base = base % modulus
        for _ in range(exponent):
            result = (result * base) % modulus
        return result

    @staticmethod
    def cormen_recursive_squaring(base: int, exponent: int, modulus: int) -> int:
        """
        Complejidad Temporal: O(log b) operaciones aritméticas.
        Complejidad Espacial: O(log b) debido a la pila de recursión.
        """
        if exponent == 0:
            return 1
        
        if exponent % 2 == 0:
            half = ModularExponentiation.cormen_recursive_squaring(base, exponent // 2, modulus)
            return (half * half) % modulus
        else:
            prev = ModularExponentiation.cormen_recursive_squaring(base, exponent - 1, modulus)
            return (base * prev) % modulus

    @staticmethod
    def cormen_iterative_squaring(base: int, exponent: int, modulus: int) -> int:
        """
        Optimiza el espacio de la pila de recursión.
        Complejidad Temporal: O(log b)
        Complejidad Espacial: O(1)
        """
        if modulus == 1:
            return 0
        result = 1
        base = base % modulus
        while exponent > 0:
            # Si el bit actual es 1, acumular en el resultado
            if exponent % 2 == 1:
                result = (result * base) % modulus
            # Cuadrado repetido
            base = (base * base) % modulus
            exponent //= 2
        return result


class ExperimentalFramework:
    """Clase encargada de ejecutar las pruebas, tomar tiempos y generar gráficos."""
    
    def __init__(self):
        self.results = []

    def run_experiments(self, max_bit_length: int = 14, steps: int = 10):
        """
        Ejecuta experimentos comparativos incrementando el tamaño en bits del exponente.
        Se usa un límite bajo para el método ingenuo debido a su lentitud O(b).
        """
        print("Iniciando pruebas experimentales")
        self.results = []
        
        # Generar exponentes con tamaños de bits controlados para no congelar la PC con el método ingenuo
        # Pasos de tamaño: desde 2 hasta el límite indicado
        bit_sizes = [int(2 + (max_bit_length - 2) * i / (steps - 1)) for i in range(steps)]
        
        for idx, bits in enumerate(bit_sizes):
            # Asegurar bases estables fijas para una comparación justa
            base = 3
            modulus = 1000000007  # Un primo grande estándar
            exponent = (1 << bits) - 1 # Exponente lleno de unos en binario (peor caso)

            print(f"[{idx+1}/{steps}] Probando con exponente de {bits} bits (Valor: {exponent})...")

            # 1. Medir Método Ingenuo
            start_time = time.perf_counter()
            res_naive = ModularExponentiation.naive_exponentiation(base, exponent, modulus)
            end_time = time.perf_counter()
            t_naive = end_time - start_time

            # 2. Medir Método del Cormen (Recursivo)
            start_time = time.perf_counter()
            res_rec = ModularExponentiation.cormen_recursive_squaring(base, exponent, modulus)
            end_time = time.perf_counter()
            t_rec = end_time - start_time

            # 3. Medir Método del Cormen (Iterativo)
            start_time = time.perf_counter()
            res_iter = ModularExponentiation.cormen_iterative_squaring(base, exponent, modulus)
            end_time = time.perf_counter()
            t_iter = end_time - start_time

            # Validar Correctitud (15% de la rúbrica)
            assert res_naive == res_rec == res_iter, "¡Error! Los algoritmos difieren en resultados."

            self.results.append({
                'bits': bits,
                'exponent_value': exponent,
                't_naive': t_naive,
                't_recursive': t_rec,
                't_iterative': t_iter
            })
            
        self._save_to_csv()
        print("Experimentos finalizados con éxito. Datos guardados en 'resultados_experimento.csv'.")

    def _save_to_csv(self):
        with open('resultados_experimento.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Bits Exponente', 'Valor Exponente', 'Tiempo Ingenuo (s)', 'Tiempo Recursivo (s)', 'Tiempo Iterativo (s)'])
            for row in self.results:
                writer.writerow([row['bits'], row['exponent_value'], row['t_naive'], row['t_recursive'], row['t_iterative']])

    def generate_plots(self):
        """Genera y guarda la gráfica comparativa."""
        if not self.results:
            print("No hay datos para graficar. Ejecuta primero run_experiments().")
            return

        bits = [r['bits'] for r in self.results]
        t_naive = [r['t_naive'] for r in self.results]
        t_rec = [r['t_recursive'] for r in self.results]
        t_iter = [r['t_iterative'] for r in self.results]

        plt.figure(figsize=(10, 6))
        plt.plot(bits, t_naive, label='Ingenuo O(b) - Lineal', color='red', marker='o', linewidth=2)
        plt.plot(bits, t_rec, label='Cormen Recursivo O(log b)', color='blue', marker='s', linestyle='--')
        plt.plot(bits, t_iter, label='Cormen Iterativo O(log b)', color='green', marker='^', linestyle=':')

        plt.title('Comparativa de Rendimiento: Exponenciación Modular', fontsize=14, fontweight='bold')
        plt.xlabel('Tamaño del Exponente (en bits)', fontsize=12)
        plt.ylabel('Tiempo de Ejecución (segundos)', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend(fontsize=11)
        
        # Guardar la gráfica para el reporte
        plt.savefig('grafica_rendimiento.png', dpi=300, bbox_inches='tight')
        print("Gráfica generada y guardada como 'grafica_rendimiento.png'.")
        plt.show()


if __name__ == "__main__":
    # Demostración del ejemplo del libro página 933: "Powers of 3 modulo 7"
    print("--- Verificación con el Ejemplo del Libro (Pág. 933) ---")
    print("Potencias de 3 módulo 7:")
    for i in range(6):
        val = ModularExponentiation.cormen_iterative_squaring(3, i, 7)
        print(f"3^{i} mod 7 = {val}")
        
    print("\n--- Ejecución de la Suite Experimental ---")
    framework = ExperimentalFramework()
    # Se usan hasta 15 bits para el exponente para que el método ingenuo (2^15 iteraciones) no tarde demasiado.
    framework.run_experiments(max_bit_length=15, steps=8)
    framework.generate_plots()