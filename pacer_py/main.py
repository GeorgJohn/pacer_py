""" Main entry point for the pacer_py application."""
from pacer_py.jobs import job_factory


def main() -> None:
    
    job = job_factory.ask_user()

    user_inputs = job.user_request()
    user_results = job.execute(user_inputs)
    job.user_response(user_results)
