document.addEventListener("DOMContentLoaded", function () {
    chrome.storage.local.get("faceitReportData", function (data) {
        console.log("🔍 Data hämtad från storage:", data);

        let reportDiv = document.getElementById("teamAnalysis");

        if (!data.faceitReportData || Object.keys(data.faceitReportData).length === 0) {
            reportDiv.innerHTML = "<p style='color:red;'>❌ Ingen data hittades. Se till att hämta en match först!</p>";
            return;
        }

        let reportData = data.faceitReportData;
        let teams = reportData.teams;
        let playersMaps = reportData.players_maps;
        let teamAnalysis = reportData.team_analysis;

        Object.keys(teams).forEach((teamKey) => {
            let teamName = teams[teamKey];

            let teamCard = document.createElement("div");
            teamCard.classList.add("team-card");

            let teamTitle = document.createElement("h2");
            teamTitle.textContent = `🏆 ${teamName}`;
            teamCard.appendChild(teamTitle);

            // 📌 Ban-sektion
            let banSection = document.createElement("div");
            banSection.classList.add("ban-section");

            let banTitle = document.createElement("h3");
            banTitle.textContent = "🚫 Mest sannolika bans:";
            banSection.appendChild(banTitle);

            let banList = document.createElement("ul");

            if (teamAnalysis[teamKey] && teamAnalysis[teamKey].ban_probabilities) {
                teamAnalysis[teamKey].ban_probabilities.forEach((ban) => {
                    let listItem = document.createElement("li");
                    listItem.innerHTML = `<strong>${ban.map}:</strong> ${ban.count} spelare har aldrig spelat denna karta`;
                    banList.appendChild(listItem);
                });
            } else {
                let listItem = document.createElement("li");
                listItem.innerHTML = `Ingen ban-data tillgänglig`;
                banList.appendChild(listItem);
            }

            banSection.appendChild(banList);
            teamCard.appendChild(banSection);

            // 🎮 Spelare och deras kartor
            let teamPlayers = playersMaps[teamKey] || {};
            Object.keys(teamPlayers).forEach((player) => {
                let playerData = teamPlayers[player];

                let playerCard = document.createElement("div");
                playerCard.classList.add("player-card");

                let playerTitle = document.createElement("h3");
                playerTitle.textContent = `🎮 ${player}`;
                playerCard.appendChild(playerTitle);

                let playerTable = document.createElement("table");
                playerTable.classList.add("styled-table");

                let tableHead = document.createElement("thead");
                tableHead.innerHTML = "<tr><th>Karta</th><th>Matcher</th><th>Win Rate</th></tr>";
                playerTable.appendChild(tableHead);

                let tableBody = document.createElement("tbody");

                if (playerData.maps) {
                    playerData.maps.forEach((mapObj) => {
                        let row = document.createElement("tr");
                        let matches = mapObj.matches || 0;
                        let winRate = mapObj.win_rate || 0;

                        let cssClass = matches === 0 ? "low-played" : matches < 10 ? "medium-played" : "high-played";

                        row.innerHTML = `<td>${mapObj.map}</td><td class="${cssClass}">${matches}</td><td>${winRate}%</td>`;
                        tableBody.appendChild(row);
                    });
                } else {
                    let row = document.createElement("tr");
                    row.innerHTML = `<td colspan="3">Ingen data tillgänglig</td>`;
                    tableBody.appendChild(row);
                }

                playerTable.appendChild(tableBody);
                playerCard.appendChild(playerTable);
                teamCard.appendChild(playerCard);
            });

            reportDiv.appendChild(teamCard);
        });
    });
});
