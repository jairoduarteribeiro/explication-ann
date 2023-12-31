import logging


def create_metrics(dataset_name):
    return {
        'dataset_name': dataset_name,
        'accumulated_time_with_box': 0,
        'accumulated_time_without_box': 0,
        'accumulated_box_time': 0,
        'irrelevant_by_box': 0,
        'irrelevant_by_solver': 0,
        'continuous_vars': 0,
        'binary_vars': 0,
        'constraints': 0
    }


def prepare_metrics(metrics, number_executions, len_x):
    number_explications = number_executions * len_x
    irrelevant_by_box = metrics['irrelevant_by_box'] / number_explications
    irrelevant_by_solver = metrics['irrelevant_by_solver'] / number_explications
    total = irrelevant_by_box + irrelevant_by_solver
    return {
        'avg_time_with_box': metrics['accumulated_time_with_box'] / number_explications,
        'avg_time_without_box': metrics['accumulated_time_without_box'] / number_explications,
        'avg_time_box': metrics['accumulated_box_time'] / number_explications,
        'irrelevant_by_box': irrelevant_by_box,
        'irrelevant_by_solver': irrelevant_by_solver,
        'percentage_irrelevant_by_box': irrelevant_by_box / total,
        'percentage_irrelevant_by_solver': irrelevant_by_solver / total
    }


def log_metrics(metrics):
    avg_time_with_box = metrics['avg_time_with_box']
    avg_time_without_box = metrics['avg_time_without_box']
    logging.info('--------------------------------------------------------------------------------')
    logging.info('METRICS PER EXPLICATION:'
                 f'\n- Average time without box: {avg_time_without_box:.4f} seconds'
                 f'\n- Average time with box: {avg_time_with_box:.4f} seconds'
                 '\nBOX METRICS:'
                 f'\n- Average time spent on box: {metrics["avg_time_box"]:.4f} seconds'
                 f'\n- Average features irrelevant by box: {metrics["irrelevant_by_box"]:.4f} '
                 f'({metrics["percentage_irrelevant_by_box"] * 100:.2f}%)'
                 f'\n- Average features irrelevant by solver: {metrics["irrelevant_by_solver"]:.4f} '
                 f'({metrics["percentage_irrelevant_by_solver"] * 100:.2f}%)')
    result, diff = ('better', avg_time_without_box - avg_time_with_box) if avg_time_with_box < avg_time_without_box \
        else ('worse', avg_time_with_box - avg_time_without_box)
    logging.info(f'FINAL RESULT:\n- Running with box was {result} than without box {diff:.4f} seconds')
