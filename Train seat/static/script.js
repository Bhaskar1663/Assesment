document.getElementById('booking-form').addEventListener('submit', async function (event) {
    event.preventDefault();
    
    const numSeats = parseInt(document.getElementById('num-seats').value);
    const resultDiv = document.getElementById('booking-result');

    if (numSeats < 1 || numSeats > 7) {
        resultDiv.textContent = 'Please enter a valid number of seats (1-7).';
        return;
    }

    try {
        const response = await fetch('/book', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ num_seats: numSeats }),
        });

        const result = await response.json();

        if (response.ok) {
            resultDiv.textContent = `Seats booked successfully: ${result.booked_seats.join(', ')}`;
            location.reload();
        } else {
            resultDiv.textContent = result.error;
        }
    } catch (error) {
        resultDiv.textContent = 'An error occurred. Please try again.';
    }
});
