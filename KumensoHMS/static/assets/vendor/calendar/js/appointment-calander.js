$(function () {
    /* initialize the calendar */
    var date = new Date();
    var d = date.getDate();
    var m = date.getMonth();
    var y = date.getFullYear();

    // Fetch appointments from the server
    $.ajax({
        url: 'patientcalander', // Replace this with the actual URL to fetch appointments
        type: 'GET',
        success: function (data) {
            var events = [];
            // Loop through each appointment and add it to the events array
            data.forEach(function (appointment) {
                var start = new Date(appointment.start_time.replace(' ', 'T'));
                var end = new Date(appointment.end_time.replace(' ', 'T'));
                events.push({
                    title: appointment.appointment_reason,
                    start: start,
                    end: end,
                });
            });

            // Initialize FullCalendar with events array
            $('#calendar').fullCalendar({
                header: {
                    left: 'prev, next',
                    center: 'title',
                    right: 'today, month, agendaWeek, agendaDay'
                },
                events: events, // Set the events array
                editable: true,
                eventLimit: true,
                droppable: true,
                drop: function (date, allDay) {
                    // Same as before
                    var originalEventObject = $(this).data('eventObject');
                    var copiedEventObject = $.extend({}, originalEventObject);
                    copiedEventObject.start = date;
                    copiedEventObject.allDay = allDay;
                    $('#calendar').fullCalendar('renderEvent', copiedEventObject, true);
                    if ($('#drop-remove').is(':checked')) {
                        $(this).remove();
                    }
                }
            });
        },
        error: function (error) {
            console.error("Error fetching appointments:", error);
        }
    });
});
