import logging
import multiprocessing
import time
from typing import Literal

logging.basicConfig(level=logging.INFO, format='%(message)s')


def get_number_factors(num: int) -> list:
    process = multiprocessing.current_process().name
    logging.info(f"Number {num} on process {process}")
    factors = []
    for i in range(1, num + 1):
        if num % i == 0:
            factors.append(i)
    return factors


class FactorLinear:
    def __init__(self, *numbers: int):
        self.numbers = numbers

    def factorize(self) -> list[list]:
        result = []
        for num in self.numbers:
            factor = get_number_factors(num)
            result.append(factor)
        return result

    def self_check(self):
        factors = self.factorize()
        expected_factors = [
            [1, 2, 4, 8, 16, 32, 64, 128],
            [1, 3, 5, 15, 17, 51, 85, 255],
            [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999],
            [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
             1521580, 2130212, 2662765, 5325530, 10651060],
            [1, 2, 4, 8, 157, 314, 628, 1256, 74047, 148094, 296188, 592376, 11625379, 23250758, 46501516, 93003032],
            [1, 2, 1993, 3986, 24979, 49958, 49783147, 99566294]
        ]

        for i, factor in enumerate(factors):
            assert factor == expected_factors[i], f"Factorization error for number {self.numbers[i]}."

        logging.info("Self-check passed. All factors are correct.")


class FactorParallel(FactorLinear):
    def factorize(self) -> list[list]:
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            result = pool.map(get_number_factors, self.numbers)
        return result


def run_factorization(numbers: int, mode: Literal["parallel", "linear"]):
    if mode == "linear":
        factor_class = FactorLinear
        logging.info("\nRunning in linear mode...\n")
    elif mode == "parallel":
        factor_class = FactorParallel
        logging.info("\nRunning in parallel mode...\n")
    else:
        logging.error("Invalid mode. Please specify 'linear' or 'parallel'.")
        return

    start_time = time.time()
    factor_instance = factor_class(*numbers)
    factor_instance.self_check()
    end_time = time.time()

    if mode == "parallel":
        cpu = multiprocessing.cpu_count()
        logging.info(
            f"{factor_instance.__class__.__name__} execution time: {end_time - start_time:.4f} seconds on {cpu} cpu's")
    else:
        logging.info(f"{factor_instance.__class__.__name__} execution time: {end_time - start_time:.4f} seconds")


if __name__ == "__main__":
    numbers = (128, 255, 99999, 10651060, 93003032, 99566294)
    run_factorization(numbers, "linear")
    run_factorization(numbers, "parallel")
