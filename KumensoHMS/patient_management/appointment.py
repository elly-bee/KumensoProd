"""from datetime import datetime, timedelta
from .models import AppointmentDateTime,Appointments



def generate_time_blocks(appointment_date, start_time, end_time, interval_minutes=30):
    # Define the time interval
    interval = timedelta(minutes=interval_minutes)

    # Create available time blocks for the given date
    current_time = datetime.combine(appointment_date, start_time)
    while current_time < datetime.combine(appointment_date, end_time):
        end_of_block = current_time + interval
        AppointmentDateTime.objects.create(
            appointment_date=appointment_date,
            start_time=current_time.time(),
            end_time=end_of_block.time()
        )
        current_time = end_of_block
"""