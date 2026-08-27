async function fetchJson(url) {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`${url}: HTTP ${response.status}`);
    }
    return response.json();
}

async function refresh() {
    try {
        const [registers, device, system] = await Promise.all([
            fetchJson("/api/registers"),
            fetchJson("/api/device"),
            fetchJson("/api/system"),
        ]);

        document.getElementById("status").innerHTML =
            `🟢 Online &nbsp;&nbsp;|&nbsp;&nbsp; ${registers.length} Register`;

        document.getElementById("device-model").textContent = device.model;
        document.getElementById("device-technology").textContent =
            `Technik: ${device.technology}`;

        document.getElementById("system-mode").textContent =
            `${system.raw ?? "–"} – ${system.mode}`;

        renderFavorites(registers);
        renderTable(registers);
    }
    catch (error) {
        document.getElementById("status").innerHTML =
            "🔴 Verbindung zum Server verloren";
        console.error(error);
    }
}

function renderFavorites(registers) {
    const favorites = document.getElementById("favorites");
    favorites.innerHTML = "";

    registers
        .filter(r => r.favorite)
        .sort((a, b) => a.register - b.register)
        .forEach(r => {
            favorites.innerHTML += `
                <div class="card">
                    <div class="card-title">🌡 ${r.name}</div>
                    <div class="card-value">${Number(r.scaled).toFixed(1)}</div>
                    <div class="card-unit">${r.unit}</div>
                    <div class="card-register">
                        Register R${String(r.register).padStart(3, "0")}
                    </div>
                </div>
            `;
        });
}

function renderTable(registers) {
    const tbody = document.querySelector("#registers tbody");
    tbody.innerHTML = "";

    registers
        .sort((a, b) => a.register - b.register)
        .forEach(r => {
            tbody.innerHTML += `
                <tr>
                    <td>R${String(r.register).padStart(3, "0")}</td>
                    <td>${r.name}</td>
                    <td>${Number(r.scaled).toFixed(1)} ${r.unit}</td>
                </tr>
            `;
        });
}

refresh();
setInterval(refresh, 5000);
