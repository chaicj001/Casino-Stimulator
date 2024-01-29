<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.2.1/socket.io.js"></script>

// Listen for balance updates
socket.on('balance_updated', function(data) {
    // Update the displayed balance
    document.getElementById('balance').innerText = data.balance;
});

function logout() {
    window.location.replace('/logout');
}

function topup(priv) {
    if (priv != 'admin' && priv != 'banker') {
        if (confirm("Are you sure you want to top up your account?")) {
            window.location.replace('/topup');
        }
    } else {
        window.location.replace('/topup');
    }
}