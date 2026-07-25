fetch("/api/reports-data")
    .then(response => response.json())
    .then(data => {

        const ctx = document.getElementById("historyChart");

        new Chart(ctx, {
            type: "line",
            data: {
                labels: data.ids,
                datasets: [
                    {
                        label: "SpO₂",
                        data: data.spo2,
                        borderWidth: 2
                    },
                    {
                        label: "FC",
                        data: data.fc,
                        borderWidth: 2
                    },
                    {
                        label: "Temperatura",
                        data: data.temp,
                        borderWidth: 2
                    },
                    {
                        label: "FR",
                        data: data.fr,
                        borderWidth: 2
                    }
                ]
            },
            options: {
                responsive: true
            }
        });

    });
