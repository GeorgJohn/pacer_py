import abc
from typing import Any

import pacer_py.user_interface as ui

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
        user_readings = {}
        user_readings['distance'] = ui.ask_user_for_distance()
        user_readings['duration'] = ui.ask_user_for_duration()
        return user_readings

    def execute(self, user_input: dict[str, Any]) -> dict[str, Any]:
        print(f"Start calculating pace")
        return dict()

    def user_response(self, result: dict[str, Any]) -> None:
        pass

class CalculateDuration(Job):
    def __str__(self) -> str:
        return "Start Duration Calculator"
    
    def user_request(self) -> dict[str, Any]:
        return dict()

    def execute(self, user_input: dict[str, Any]) -> dict[str, Any]:
        print(f"Start calculating duration")
        return dict()

    def user_response(self, result: dict[str, Any]) -> None:
        pass

class CalculateDistance(Job):
    def __str__(self) -> str:
        return "Start Distance Calculator"
    
    def user_request(self) -> dict[str, Any]:
        return dict()

    def execute(self, user_input: dict[str, Any]) -> dict[str, Any]:
        print(f"Start calculating distance")
        return dict()

    def user_response(self, result: dict[str, Any]) -> None:
        pass


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