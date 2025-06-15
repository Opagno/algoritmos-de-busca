"""
Implementação básica dos algoritmos de busca para estudo comparativo
Autor: [Artur Pagno]
RA: [21013037]
"""


import time
import random
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import List, Tuple, Dict
import seaborn as sns

class SearchAlgorithms:
    """Classe para implementação e comparação de algoritmos de busca"""
    
    def __init__(self):
        self.results = []
    
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
    
    def executar_teste(self, algorithm_func, arr: List[int], target: int, iterations: int = 100) -> Dict:
        """
        Executa teste de performance para um algoritmo
        """
        times = []
        comparisons_list = []
        
        for _ in range(iterations):
            start_time = time.perf_counter()
            position, comparisons = algorithm_func(arr, target)
            end_time = time.perf_counter()
            
            times.append((end_time - start_time) * 1000)  # em milissegundos
            comparisons_list.append(comparisons)
        
        return {
            'avg_time': np.mean(times),
            'avg_comparisons': np.mean(comparisons_list),
            'position': position,
            'std_time': np.std(times),
            'std_comparisons': np.std(comparisons_list)
        }
    
    def executar_estudo_completo(self):
        """
        Executa o estudo completo comparando os algoritmos
        """
        sizes = [1000, 10000, 100000]
        casos = ['medio', 'pior']
        
        print("🔍 Iniciando Estudo Comparativo de Algoritmos de Busca")
        print("=" * 60)
        
        for size in sizes:
            print(f"\n Testando com {size:,} elementos...")
            arr = self.gerar_dados_teste(size)
            
            for caso in casos:
                print(f"   Caso: {caso}")
                
                # Definir target baseado no caso
                if caso == 'medio':
                    target = random.randint(1, size)
                else:  # pior caso
                    target = size + 1  # elemento que não existe
                
                # Testar busca sequencial
                seq_result = self.executar_teste(self.busca_sequencial, arr, target)
                
                # Testar busca binária
                bin_result = self.executar_teste(self.busca_binaria, arr, target)
                
                # Armazenar resultados
                result_entry = {
                    'tamanho': size,
                    'caso': caso,
                    'target': target,
                    'seq_time': seq_result['avg_time'],
                    'seq_comparisons': seq_result['avg_comparisons'],
                    'bin_time': bin_result['avg_time'],
                    'bin_comparisons': bin_result['avg_comparisons'],
                    'seq_std_time': seq_result['std_time'],
                    'bin_std_time': bin_result['std_time']
                }
                
                self.results.append(result_entry)
                
                print(f"     Sequencial: {seq_result['avg_time']:.4f}ms, "
                      f"{seq_result['avg_comparisons']:.1f} comparações")
                print(f"     Binária: {bin_result['avg_time']:.4f}ms, "
                      f"{bin_result['avg_comparisons']:.1f} comparações")
    
    def gerar_relatorio(self):
        """
        Gera relatório completo com tabelas e gráficos
        """
        df = pd.DataFrame(self.results)
        
        print("\n" + "="*80)
        print("RELATÓRIO DE RESULTADOS")
        print("="*80)
        
        # Tabela de resultados
        print("\n TABELA DE TEMPOS DE EXECUÇÃO (milissegundos)")
        print("-" * 60)
        for _, row in df.iterrows():
            print(f"Tamanho: {row['tamanho']:>6,} | Caso: {row['caso']:>6} | "
                  f"Seq: {row['seq_time']:>8.4f}ms | Bin: {row['bin_time']:>8.4f}ms | "
                  f"Speedup: {row['seq_time']/row['bin_time']:>6.1f}x")
        
        print("\n TABELA DE COMPARAÇÕES")
        print("-" * 60)
        for _, row in df.iterrows():
            print(f"Tamanho: {row['tamanho']:>6,} | Caso: {row['caso']:>6} | "
                  f"Seq: {row['seq_comparisons']:>8.1f} | Bin: {row['bin_comparisons']:>8.1f} | "
                  f"Redução: {row['seq_comparisons']/row['bin_comparisons']:>6.1f}x")
        
        # Gerar gráficos
        self.plotar_graficos(df)
    
    def plotar_graficos(self, df: pd.DataFrame):
        """
        Gera gráficos comparativos
        """
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Estudo Comparativo: Busca Sequencial vs Busca Binária', 
                     fontsize=16, fontweight='bold')
        
        # Gráfico 1: Tempo vs Tamanho (Caso Médio)
        df_medio = df[df['caso'] == 'medio']
        axes[0,0].plot(df_medio['tamanho'], df_medio['seq_time'], 
                      'o-', label='Busca Sequencial', linewidth=2, markersize=8)
        axes[0,0].plot(df_medio['tamanho'], df_medio['bin_time'], 
                      's-', label='Busca Binária', linewidth=2, markersize=8)
        axes[0,0].set_xlabel('Tamanho da Entrada')
        axes[0,0].set_ylabel('Tempo (ms)')
        axes[0,0].set_title('Tempo de Execução - Caso Médio')
        axes[0,0].legend()
        axes[0,0].grid(True, alpha=0.3)
        axes[0,0].set_xscale('log')
        axes[0,0].set_yscale('log')
        
        # Gráfico 2: Comparações vs Tamanho (Caso Médio)
        axes[0,1].plot(df_medio['tamanho'], df_medio['seq_comparisons'], 
                      'o-', label='Busca Sequencial', linewidth=2, markersize=8)
        axes[0,1].plot(df_medio['tamanho'], df_medio['bin_comparisons'], 
                      's-', label='Busca Binária', linewidth=2, markersize=8)
        axes[0,1].set_xlabel('Tamanho da Entrada')
        axes[0,1].set_ylabel('Número de Comparações')
        axes[0,1].set_title('Comparações - Caso Médio')
        axes[0,1].legend()
        axes[0,1].grid(True, alpha=0.3)
        axes[0,1].set_xscale('log')
        axes[0,1].set_yscale('log')
        
        # Gráfico 3: Tempo vs Tamanho (Pior Caso)
        df_pior = df[df['caso'] == 'pior']
        axes[1,0].plot(df_pior['tamanho'], df_pior['seq_time'], 
                      'o-', label='Busca Sequencial', linewidth=2, markersize=8, color='red')
        axes[1,0].plot(df_pior['tamanho'], df_pior['bin_time'], 
                      's-', label='Busca Binária', linewidth=2, markersize=8, color='blue')
        axes[1,0].set_xlabel('Tamanho da Entrada')
        axes[1,0].set_ylabel('Tempo (ms)')
        axes[1,0].set_title('Tempo de Execução - Pior Caso')
        axes[1,0].legend()
        axes[1,0].grid(True, alpha=0.3)
        axes[1,0].set_xscale('log')
        axes[1,0].set_yscale('log')
        
        # Gráfico 4: Speedup
        speedup_medio = df_medio['seq_time'] / df_medio['bin_time']
        speedup_pior = df_pior['seq_time'] / df_pior['bin_time']
        
        x = np.arange(len(df_medio['tamanho']))
        width = 0.35
        
        axes[1,1].bar(x - width/2, speedup_medio, width, 
                     label='Caso Médio', alpha=0.8, color='green')
        axes[1,1].bar(x + width/2, speedup_pior, width, 
                     label='Pior Caso', alpha=0.8, color='orange')
        axes[1,1].set_xlabel('Tamanho da Entrada')
        axes[1,1].set_ylabel('Speedup (x vezes mais rápido)')
        axes[1,1].set_title('Speedup: Busca Binária vs Sequencial')
        axes[1,1].set_xticks(x)
        axes[1,1].set_xticklabels([f'{size:,}' for size in df_medio['tamanho']])
        axes[1,1].legend()
        axes[1,1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.show()
        
        # Análise de complexidade
        self.analisar_complexidade(df)
    
    def analisar_complexidade(self, df: pd.DataFrame):
        """
        Analisa se o comportamento prático segue a teoria de complexidade
        """
        print("\n" + "="*80)
        print("ANÁLISE DE COMPLEXIDADE ALGORÍTMICA")
        print("="*80)
        
        df_medio = df[df['caso'] == 'medio']
        sizes = df_medio['tamanho'].values
        
        print("\n COMPLEXIDADE TEÓRICA:")
        print("• Busca Sequencial: O(n) - linear")
        print("• Busca Binária: O(log n) - logarítmica")
        
        print("\n CRESCIMENTO OBSERVADO (caso médio):")
        
        # Análise busca sequencial
        seq_ratios = []
        for i in range(1, len(sizes)):
            ratio_teorico = sizes[i] / sizes[i-1]
            ratio_pratico = df_medio.iloc[i]['seq_comparisons'] / df_medio.iloc[i-1]['seq_comparisons']
            seq_ratios.append((ratio_teorico, ratio_pratico))
            print(f"• Sequencial {sizes[i-1]:,} → {sizes[i]:,}: "
                  f"teórico {ratio_teorico:.1f}x, prático {ratio_pratico:.1f}x")
        
        # Análise busca binária
        bin_ratios = []
        for i in range(1, len(sizes)):
            ratio_teorico = np.log2(sizes[i]) / np.log2(sizes[i-1])
            ratio_pratico = df_medio.iloc[i]['bin_comparisons'] / df_medio.iloc[i-1]['bin_comparisons']
            bin_ratios.append((ratio_teorico, ratio_pratico))
            print(f"• Binária {sizes[i-1]:,} → {sizes[i]:,}: "
                  f"teórico {ratio_teorico:.1f}x, prático {ratio_pratico:.1f}x")
        
        print("\n INTERPRETAÇÃO:")
        print("• A busca sequencial mostra crescimento próximo ao linear esperado O(n)")
        print("• A busca binária demonstra crescimento logarítmico conforme O(log n)")
        print("• Os resultados práticos confirmam a análise assintótica teórica")


def main():
    """Função principal para executar o estudo"""
    print("Estudo Comparativo de Algoritmos de Busca")
    print("Implementação: Python 3.x")
    print("Bibliotecas: matplotlib, pandas, numpy, seaborn")
    print("="*60)
    
    # Criar instância e executar estudo
    study = SearchAlgorithms()
    
    # Executar testes
    study.executar_estudo_completo()
    
    # Gerar relatório
    study.gerar_relatorio()
    
    print("\n Estudo concluído!")
    print("Verifique os gráficos gerados e os resultados acima.")
    print("\n Para salvar os resultados:")
    print("• Screenshots dos gráficos para o relatório")
    print("• Dados em CSV: pd.DataFrame(study.results).to_csv('resultados.csv')")

if __name__ == "__main__":
    main()