document.getElementById("fetchData").addEventListener("click", async function() {
    let roomId = await extractMatchId();  // Hämta Room ID från URL
    if (!roomId) {
        document.getElementById("result").innerText = "❌ Ingen matchlobby hittades! Gå till en Faceit-lobby först.";
        return;
    }

    let apiUrl = `https://faceit-match-analyzer.onrender.com/analyze?room_id=${roomId}`;

    try {
        let response = await fetch(apiUrl);
        if (!response.ok) throw new Error("Kunde inte hämta matchdata.");
        let data = await response.json();

        // 🚀 Spara datan i chrome.storage.local
        chrome.storage.local.set({ faceitReportData: data }, function() {
            console.log("🔹 Data sparad i chrome.storage.local:", data);
            chrome.tabs.create({ url: "report.html" }); // Öppna analysrapport
        });

    } catch (error) {
        document.getElementById("result").innerHTML = `<p style="color:red;">${error.message}</p>`;
    }
});

// 🕵️‍♂️ Funktion för att hämta Match ID från Faceit-URL
async function extractMatchId() {
    return new Promise((resolve) => {
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            if (tabs.length === 0 || !tabs[0].url) {
                resolve(null);
                return;
            }

            let url = tabs[0].url;
            let matchId = url.match(/\/room\/([a-zA-Z0-9-]+)/);
            resolve(matchId ? matchId[1] : null);
        });
    });
}
