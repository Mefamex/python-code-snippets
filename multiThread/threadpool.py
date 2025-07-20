#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
===========================================================
                    THREAD POOL
===========================================================

Description:
    Python'da verimli paralel görev yürütümü için profesyonel thread pool (iş parçacığı havuzu) 
    implementasyonu. Bu modül, çoklu iş parçacığı ile görevlerin aynı anda çalıştırılmasını 
    sağlar ve thread-safe bir şekilde görev yönetimi sunar.

Author:
    Mefamex (info@mefamex.com) (https://mefamex.com)

Features: 
    - Verimli paralel görev yürütümü
    - Dinamik thread havuzu yönetimi
    - Thread-safe görev ekleme ve sonuç toplama
    - Esnek sonuç yönetimi (saklama veya anında yazdırma)
    - Performans ölçümü ve süre hesaplama
    - Basit ve sezgisel API

Modules:
    - threading: Thread yönetimi ve senkronizasyon
    - queue: Thread-safe görev kuyruğu
    - time: Performans ölçümü ve zamanlama
    - random: Test amaçlı rastgele sayı üretimi

Classes:
    - POOL: Ana thread pool sınıfı, görev yönetimi ve paralel çalıştırma için

Functions:
    - __init__(max_threads, logFuture, ResultwhenDone): Thread pool'u başlatır
    - submit(func, *args, **kwargs): Yeni görev ekler
    - join(): Tüm görevlerin tamamlanmasını bekler ve sonuçları döner
    - _worker(): Thread worker fonksiyonu (dahili)

Usage:
    1. POOL nesnesi oluşturun (max_threads, logFuture, ResultwhenDone parametreleri ile)
    2. submit() metodu ile görevleri ekleyin
    3. join() metodu ile tüm görevlerin tamamlanmasını bekleyin
    4. Sonuçları, geçen süreyi ve toplam işlem süresini alın

Requirements:
    - Python 3.6 veya üstü
    - Dependencies:
        - threading (built-in)
        - queue (built-in)
        - time (built-in)
        - random (built-in)

Installation:
    1. Tek dosya olarak kullanım:
        - Bu dosyayı projenize kopyalayın
        - Python -> from threadpool import POOL

Documentation: 
    - Detaylı kullanım örnekleri: `README.md`
    - API dokümantasyonu: Kod içi docstring'ler

License:
    MIT Lisansı (https://opensource.org/licenses/MIT)

Changelog:
    - 1.0.0 (2024-09-08): İlk sürüm
    - 1.1.0 (2025-07-20): Dokümantasyon iyileştirmeleri ve usage example güncellenmesi

Contributors: None

Contact:
    - Email: info@mefamex.com
    - Website: https://mefamex.com
    - GitHub: https://github.com/Mefamex/Python_Code_Snippets

Additional Information:
    Bu modül, I/O yoğun işlemler için uygundur. CPU yoğun işlemler için multiprocessing 
    modülü tercih edilebilir. Thread havuzu, bellek kullanımını optimize ederken 
    aynı anda çalışan görev sayısını kontrol eder.

Notes:
    - Bu modül I/O yoğun işlemler için optimize edilmiştir
    - Çok fazla thread kullanmak sistem performansını olumsuz etkileyebilir
    - Thread-safe tasarım sayesinde güvenli görev yönetimi sağlar
    - Performans metrikleri otomatik olarak hesaplanır

Disclaimer and Legal Notice:
    Bu yazılım, herhangi bir garanti olmaksızın "olduğu gibi" sağlanmaktadır.
    Yazar, bu yazılımın kullanımı sonucunda oluşabilecek zararlardan sorumlu değildir.
    Kullanıcılar, yazılımı kendi sorumlulukları altında kullanmalıdır.
    
    MIT Lisansı kapsamında açık kaynak olarak dağıtılır ve kullanıcılar lisans 
    koşullarına uymakla yükümlüdür. Yazılımın değiştirilmesi, dağıtılması veya 
    kullanılması lisans koşullarına uygun olmalıdır.
===========================================================
"""

__version__ = "1.1.0"
__author__ = "Mefamex"
__email__ = "info@mefamex.com"
__license__ = "MIT"
__status__ = "STABLE"

__project_name__ = "thread-pool"
__url__ = "https://mefamex.com"
__url_github__ = "https://github.com/Mefamex/Python_Code_Snippets"
__copyright__ = "Copyright (c) 2025 Mefamex"
__description__ = "Python için verimli thread pool implementasyonu - paralel görev yürütümü"
__date__ = "2024-09-08"
__date_modify__ = "2025-07-20"
__python_version__ = ">=3.6" 
__dependencies__ = {
    "threading": "built-in",
    "queue": "built-in",
    "time": "built-in",
    "random": "built-in"
}
#===============================================================================



#============================ IMPORTS =========================================
import threading
from queue import Queue
from time import time, sleep
from random import randint
#==============================================================================

#============================ CLASS POOL ======================================
class POOL:
    """
    A thread pool for efficient parallel task execution.
    Args:
        max_threads (int, optional): Maximum number of threads in the pool. Defaults to 10.
        logFuture (bool, optional): Whether to store task results in a list. Defaults to True.
        ResultwhenDone (bool, optional): Whether to print task results immediately after completion. Defaults to False.
    """
    def __init__(self, max_threads:int=10, logFuture:bool=True, ResultwhenDone:bool=False):
        self.ResultwhenDone, self.logFuture =ResultwhenDone, logFuture
        self.task_queue, self.lock = Queue(), threading.Lock()
        self.futures , self.max_threads= [], max_threads
        self.start_time,self.task_times = time(), []


    def _worker(self):
        """Worker function executed by each thread in the pool."""
        while True:
            func, args, kwargs = self.task_queue.get()
            task_start_time = time()
            try:
                result = func(*args, **kwargs)
                self.task_times.append( time() - task_start_time)
                if self.logFuture: self.futures.append(result)
                if self.ResultwhenDone: print(result)
            finally:self.task_queue.task_done()


    def submit(self, func, *args, **kwargs) -> None:
        """Submits a new task for execution.
        Args:
            func: The function to be executed.
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.
        """
        if not self.start_time:self.start_time = time()
        self.task_queue.put((func, args, kwargs))
        with self.lock:
            if self.task_queue.qsize() > 0 and threading.active_count() < self.max_threads:
                threading.Thread(target=self._worker).start()

    def join(self, verbose: bool = True) -> tuple[list, float, float]:
        """Waits for all tasks to complete and returns results.

        Returns:
            tuple: A tuple containing the list of task results, elapsed time, and total time.
        """
        self.task_queue.join()
        elapsed_time = time() - self.start_time
        total_time = sum( [q for q in self.task_times ])
        if verbose: print(f"Toplam geçen süre: {elapsed_time:.2f} saniye\n kurtarılan :{total_time-elapsed_time:.2f}")
        return self.futures,elapsed_time,total_time
#===============================================================================


#============================ USAGE EXAMPLE ====================================
"""
POOL modülünün temel kullanımı aşağıdaki gibidir:


from threadpool import POOL
from time import sleep

def kare_al(x):
    sleep(1)  # Simülasyon için gecikme
    return x * x

if __name__ == "__main__":
    pool = POOL(max_threads=5, logFuture=True, ResultwhenDone=True)
    for i in range(10):
        pool.submit(kare_al, i)
    sonuc_listesi, gecen_sure, toplam_is_suresi = pool.join()
    print("Sonuçlar:", sonuc_listesi)
    print(f"Toplam geçen süre: {gecen_sure:.2f} sn, Toplam iş süresi: {toplam_is_suresi:.2f} sn")


# Kısa açıklama:
# - POOL nesnesi oluşturulur.
# - submit ile görevler eklenir.
# - join ile tüm görevlerin bitmesi beklenir ve sonuçlar alınır.
# - logFuture=True ile sonuçlar kaydedilir, ResultwhenDone=True ile her görev bittiğinde ekrana yazılır.
"""
#===============================================================================

