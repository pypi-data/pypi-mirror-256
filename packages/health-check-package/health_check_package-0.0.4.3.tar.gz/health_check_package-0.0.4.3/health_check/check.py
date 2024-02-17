from datetime import datetime


def check_crons(all_tasks: dict, started_tasks: dict, completed_tasks: dict, started_tasks_array: dict):
    """
    This function will take 3 arguments
    all_tasks: all the cron jobs with their expected time of execution (dict)
    started_tasks: tasks which have been started (dict)
    completed_tasks: tasks which have ended (dict)
    started_task_array: list of task ids for tasks which have been started (dict array)
    And this function will return 4 arrays:
    successful: list of all cron jobs which were successfully executed
    error: list of all cron jobs which failed
    warning: list of all cron jobs which are still running or failed
    delayed: list of all cron jobs which got delayed from their expected execution time
    """
    successful = []
    error = []
    warning = []
    delayed = []
    for key, value in all_tasks.items():
        cron_name = key
        cron_time = value['cron_time']
        value.pop('cron_time', None)
        started_task_ids = started_tasks_array.get(cron_name)
        if started_task_ids is None:
            if not is_process_time_valid(cron_time, datetime.now()):
                error.append(value)
            continue
        for task_id in started_task_ids:
            if check_if_task_delayed(started_tasks.get(task_id), cron_time):
                delayed.append({**started_tasks.get(task_id), **value})
            if completed_tasks.get(task_id):
                successful.append({**started_tasks.get(task_id), **value})
            else:
                warning.append({**started_tasks.get(task_id), **value})
    return successful, error, warning, delayed


def is_process_time_valid(cron_time, time):
    time_minute = time.minute
    time_hour = time.hour
    combinations = get_all_time_combinations(cron_time.get('hour'), cron_time.get('minute'))
    for hour, minute in combinations:
        if time_hour >= hour:
            if time_minute >= minute:
                return False
    return True


def get_all_time_combinations(hours, minutes):
    combinations = []
    for hour in hours:
        for minute in minutes:
            combinations.append((hour, minute))
    return combinations


def check_if_task_delayed(started_task, cron_time):
    started_task_time = started_task['start_time'].time()
    started_task_time_hour = started_task_time.hour
    started_task_time_minute = started_task_time.minute
    hours = cron_time.get('hour')
    minutes = cron_time.get('minute')
    if not started_task_time_hour in hours or not started_task_time_minute in minutes:
        return True
    return False
