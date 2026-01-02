import abc
from typing import Any

from rich import print

import pacer_py.user_interface as ui
import pacer_py.math as ppm


class Job(abc.ABC):
    
    """Abstract base class for different jobs."""
    @abc.abstractmethod
    def user_request(self) -> dict[str, Any]:
        raise NotImplementedError("Subclasses must implement this method.")
    
    @abc.abstractmethod
    def execute(self, user_input: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError("Subclasses must implement this method.")

    def user_response(self, result: dict[str, Any]) -> None:
        raise NotImplementedError("Subclasses must implement this method.")

    
class CalculatePace(Job):
    def __str__(self) -> str:
        return "Start Pace Calculator"

    def user_request(self) -> dict[str, Any]:
        user_readings: dict[str, int | float] = {}
        try:
            user_readings['distance'] = ui.ask_user_for_distance()
            user_readings['duration'] = ui.ask_user_for_duration()
        except ValueError as e:
            print(f"Error: {e}")
            return {}
        return user_readings

    def execute(self, user_input: dict[str, Any]) -> dict[str, Any]:
        distance_m = user_input.get('distance')
        duration_sec = user_input.get('duration')
        if distance_m is None or duration_sec is None:
            raise ValueError("Missing distance or duration in user input.")
        pace_min_per_km = ppm.pace_from_duration_and_distance(duration_sec, distance_m, 'min/km')
        return {'pace_min_per_km': pace_min_per_km}

    def user_response(self, result: dict[str, Any]) -> None:
        pace_reading = result.get('pace_min_per_km')
        if pace_reading is None or not isinstance(pace_reading, (float)):
            raise ValueError("Missing pace in result.")
        
        pace_split = ppm.duration_to_hh_mm_ss(pace_reading, 'min')
        print(f"Pace: {pace_split[1]:02d}:{pace_split[2]:02d} min/km")

class CalculateDuration(Job):
    def __str__(self) -> str:
        return "Start Duration Calculator"
    
    def user_request(self) -> dict[str, Any]:
        user_readings: dict[str, int | float] = {}
        try:
            user_readings['pace'] = ui.ask_user_for_pace()
            user_readings['distance'] = ui.ask_user_for_distance()
        except ValueError as e:
            print(f"Error: {e}")
            return {}
        return user_readings

    def execute(self, user_input: dict[str, Any]) -> dict[str, Any]:
        pace_sec_per_m = user_input.get('pace')
        distance_m = user_input.get('distance')
        if pace_sec_per_m is None or distance_m is None:
            raise ValueError("Missing pace or distance in user input.")
        duration_sec = ppm.duration_from_pace_and_distance(pace_sec_per_m, distance_m)
        return {'duration': duration_sec}

    def user_response(self, result: dict[str, Any]) -> None:
        duration_reading = result.get('duration')
        if duration_reading is None or not isinstance(duration_reading, (int, float)):
            raise ValueError("Missing duration in result.")
        
        if duration_reading < 180:
            print(f"Duration: {duration_reading:.2f} sec")
        else:
            duration_split = ppm.duration_to_hh_mm_ss(duration_reading, 'sec')
            print(f"Duration: {duration_split[0]:02d}:{duration_split[1]:02d}:{duration_split[2]:02d} hh:mm:ss")

class CalculateDistance(Job):
    def __str__(self) -> str:
        return "Start Distance Calculator"
    
    def user_request(self) -> dict[str, Any]:
        user_readings: dict[str, int | float] = {}
        try:
            user_readings['pace'] = ui.ask_user_for_pace()
            user_readings['duration'] = ui.ask_user_for_duration()
        except ValueError as e:
            print(f"Error: {e}")
            return {}
        return user_readings

    def execute(self, user_input: dict[str, Any]) -> dict[str, Any]:
        pace_sec_per_m = user_input.get('pace')
        duration_sec = user_input.get('duration')
        if pace_sec_per_m is None or duration_sec is None:
            raise ValueError("Missing pace or duration in user input.")
        distance_m = ppm.distance_from_pace_and_duration(pace_sec_per_m, duration_sec, 'm')
        return {'distance_m': distance_m}

    def user_response(self, result: dict[str, Any]) -> None:
        distance_reading = result.get('distance_m')
        if distance_reading is None or not isinstance(distance_reading, (int, float)):
            raise ValueError("Missing distance in result.")
        
        if distance_reading >= 1000.0:
            distance_km = distance_reading / 1000.0
            print(f"Distance: {distance_km:.2f} km")
        else:
            print(f"Distance: {distance_reading:.2f} m")


class ExitApplication(Job):
    def __str__(self) -> str:
        return "Exit Application"
    
    def user_request(self) -> dict[str, Any]:
        return dict()

    def execute(self, user_input: dict[str, Any]) -> dict[str, Any]:
        return dict()

    def user_response(self, result: dict[str, Any]) -> None:
        print("Exiting the application. Goodbye!")



class JobFactory:

    def __init__(self) -> None:
        self.jobs: dict[int, Job] = {}

    def register_job(self, job: Job) -> None:
        n = len(self.jobs) + 1
        self.jobs[n] = job

    def register_default_job(self, job: Job) -> None:
        self.default_job = job
    
    def ask_user(self) -> Job:
        opt = {key: str(value) for key, value in self.jobs.items()}
        job_id = ui.ask_user_for_option(opt)
        return self.jobs.get(job_id, self.default_job)


job_factory = JobFactory()
job_factory.register_job(CalculatePace())
job_factory.register_job(CalculateDuration())
job_factory.register_job(CalculateDistance())
job_factory.register_job(ExitApplication())
job_factory.register_default_job(ExitApplication())