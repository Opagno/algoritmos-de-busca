"""
Implementação básica dos algoritmos de busca para estudo comparativo
Autor: [Artur Pagno]
RA: [21013037]
"""


from typing import List, Tuple

class SearchAlgorithms:
    """Classe para implementação de algoritmos de busca"""
    
    def busca_sequencial(self, arr: List[int], target: int) -> Tuple[int, int]:
        """
        Implementa busca sequencial
        Retorna: (posição encontrada ou -1, número de comparações)
        """
        comparisons = 0
        for i in range(len(arr)):
            comparisons += 1
            if arr[i] == target:
                return i, comparisons
        return -1, comparisons
    
    def busca_binaria(self, arr: List[int], target: int) -> Tuple[int, int]:
        """
        Implementa busca binária
        Retorna: (posição encontrada ou -1, número de comparações)
        """
        left, right = 0, len(arr) - 1
        comparisons = 0
        
        while left <= right:
            comparisons += 1
            mid = (left + right) // 2
            
            if arr[mid] == target:
                return mid, comparisons
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return -1, comparisons
    
    def gerar_dados_teste(self, size: int) -> List[int]:
        """Gera lista ordenada de tamanho especificado"""
        return list(range(1, size + 1))


# Teste simples para verificar funcionamento
if __name__ == "__main__":
    search = SearchAlgorithms()
    
    # Teste básico
    arr = search.gerar_dados_teste(10)
    print(f"Array de teste: {arr}")
    
    # Teste busca sequencial
    pos, comp = search.busca_sequencial(arr, 7)
    print(f"Busca sequencial - Elemento 7: posição {pos}, {comp} comparações")
    
    # Teste busca binária
    pos, comp = search.busca_binaria(arr, 7)
    print(f"Busca binária - Elemento 7: posição {pos}, {comp} comparações")
    
    # Teste elemento não encontrado
    pos, comp = search.busca_sequencial(arr, 15)
    print(f"Busca sequencial - Elemento 15: posição {pos}, {comp} comparações")
    
    pos, comp = search.busca_binaria(arr, 15)
    print(f"Busca binária - Elemento 15: posição {pos}, {comp} comparações")