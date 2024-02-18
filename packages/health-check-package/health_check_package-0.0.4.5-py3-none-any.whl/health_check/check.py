from datetime import datetime


def check_crons(all_tasks: dict, started_tasks: dict, started_tasks_array: dict, completed_tasks: dict,
                completed_tasks_arr: dict):
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
        completed_task_ids = completed_tasks_arr.get(cron_name)
        started_tasks_ids = started_tasks_array.get(cron_name)
        if not completed_task_ids:
            if not started_tasks_ids:
                if not is_task_scheduled_later(cron_time, datetime.now()):
                    error.append(value)
                else:
                    continue
            else:
                for task_id in started_tasks_ids:
                    warning.append({**started_tasks.get(task_id), **value})
        else:
            for task_id in completed_task_ids:
                task_obj = completed_tasks.get(task_id)
                if check_if_task_delayed(task_obj, cron_time):
                    delayed.append({**task_obj, **value})
                successful.append({**task_obj, **value})
    return successful, error, warning, delayed


def is_task_scheduled_later(cron_time, time):
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
    if started_task_time_hour not in hours or started_task_time_minute not in minutes:
        return True
    return False
