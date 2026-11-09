const DATA_FILE = 'data.json';
let previousData = null; 

async function updateOverlay() {
    try {
        const response = await fetch(`${DATA_FILE}?t=${new Date().getTime()}`);
        if (!response.ok) return;

        const data = await response.json();

        if (!previousData) {
            applyDataToDOM(data);
            previousData = JSON.parse(JSON.stringify(data));
            return;
        }

        const currentDataString = JSON.stringify(data);
        const previousDataString = JSON.stringify(previousData);

        if (currentDataString !== previousDataString) {
            
            const elementsToFade = [];

            // --- League Check ---
            if (data.league !== previousData.league) {
                elementsToFade.push(document.getElementById('league-content'));
            }

            // --- Series Check ---
            if (data.seriesText !== previousData.seriesText) {
                elementsToFade.push(document.getElementById('series-label'));
            }

            // --- Left Side Checks ---
            if (data.left.score !== previousData.left.score) {
                elementsToFade.push(document.getElementById('left-score'));
            }
            if (data.left.team !== previousData.left.team) {
                elementsToFade.push(document.getElementById('left-team'));
            }
            if (data.left.name !== previousData.left.name) {
                elementsToFade.push(document.getElementById('left-name'));
            }
            if (data.left.bgImage !== previousData.left.bgImage) {
                elementsToFade.push(document.getElementById('left-bg'));
            }
            
            const leftVisualsChanged = data.left.logo !== previousData.left.logo || 
                                       data.left.showLogo !== previousData.left.showLogo || 
                                       data.left.color !== previousData.left.color;
            if (leftVisualsChanged) {
                elementsToFade.push(document.querySelector('.left-side .player-info'));
            }

            // --- Right Side Checks ---
            if (data.right.score !== previousData.right.score) {
                elementsToFade.push(document.getElementById('right-score'));
            }
            if (data.right.team !== previousData.right.team) {
                elementsToFade.push(document.getElementById('right-team'));
            }
            if (data.right.name !== previousData.right.name) {
                elementsToFade.push(document.getElementById('right-name'));
            }
            if (data.right.bgImage !== previousData.right.bgImage) {
                elementsToFade.push(document.getElementById('right-bg'));
            }
            
            const rightVisualsChanged = data.right.logo !== previousData.right.logo || 
                                        data.right.showLogo !== previousData.right.showLogo || 
                                        data.right.color !== previousData.right.color;
            if (rightVisualsChanged) {
                elementsToFade.push(document.querySelector('.right-side .player-info'));
            }

            elementsToFade.forEach(el => {
                if(el) el.classList.add('fade-out');
            });

            setTimeout(() => {
                applyDataToDOM(data);
                elementsToFade.forEach(el => {
                    if(el) el.classList.remove('fade-out');
                });
            }, 150);

            previousData = JSON.parse(JSON.stringify(data));
        }

    } catch (error) {
        console.error("Error fetching data.json: ", error);
    }
}

function applyDataToDOM(data) {
    // --- Update Series Text (NEW) ---
    const seriesEl = document.getElementById('series-label');
    if (seriesEl) {
        // Use the text provided or default to empty
        const seriesVal = data.seriesText !== undefined ? data.seriesText : "BEST OF 3";
        seriesEl.textContent = seriesVal;
        // Hide the black box completely if the text is deleted
        seriesEl.style.display = seriesVal ? 'block' : 'none'; 
    }

    // --- Update League ---
    const leagueBox = document.getElementById('league-label');
    const leagueContent = document.getElementById('league-content');
    
    if (leagueBox && leagueContent) {
        const leagueValue = data.league || "";
        
        if (leagueValue.toUpperCase() === "NACE") {
            leagueContent.innerHTML = `<img src="nace.png" class="league-logo" alt="NACE">`;
        } else if (leagueValue.toUpperCase() === "GLEC") {
            leagueContent.innerHTML = `<img src="glec.png" class="league-logo" alt="GLEC">`;
        } else {
            leagueContent.textContent = leagueValue;
        }
        leagueBox.style.display = leagueValue ? 'flex' : 'none'; 
    }

    // --- Update Left Player ---
    const leftTeamEl = document.getElementById('left-team');
    leftTeamEl.textContent = data.left.team;
    
    if(data.left.color) {
        leftTeamEl.style.color = data.left.color;
        document.querySelector('.left-score-box').style.color = data.left.color;
        document.querySelector('.left-side').style.setProperty('--team-color', data.left.color);
    }

    document.getElementById('left-name').textContent = data.left.name;
    document.getElementById('left-score').textContent = data.left.score;
    
    if(data.left.bgImage) {
        document.getElementById('left-bg').style.backgroundImage = `url('${data.left.bgImage}')`;
        const yOffset = data.left.bgOffsetY !== undefined ? data.left.bgOffsetY : 20;
        const zoom = data.left.bgZoom !== undefined ? data.left.bgZoom : 100;
        document.getElementById('left-bg').style.backgroundPosition = `center ${yOffset}%`;
        document.getElementById('left-bg').style.backgroundSize = zoom === 100 ? 'cover' : `${zoom}%`;
    } else {
        document.getElementById('left-bg').style.backgroundImage = 'none';
    }

    const leftLogo = document.getElementById('left-logo');
    if(data.left.logo && data.left.showLogo) {
        leftLogo.src = data.left.logo;
        leftLogo.style.display = 'block';
    } else {
        leftLogo.style.display = 'none';
    }

    document.getElementById('left-win-1').className = data.left.setWins >= 1 ? 'diamond filled' : 'diamond';
    document.getElementById('left-win-2').className = data.left.setWins >= 2 ? 'diamond filled' : 'diamond';


    // --- Update Right Player ---
    const rightTeamEl = document.getElementById('right-team');
    rightTeamEl.textContent = data.right.team;
    
    if(data.right.color) {
        rightTeamEl.style.color = data.right.color;
        document.querySelector('.right-score-box').style.color = data.right.color;
        document.querySelector('.right-side').style.setProperty('--team-color', data.right.color);
    }

    document.getElementById('right-name').textContent = data.right.name;
    document.getElementById('right-score').textContent = data.right.score;
    
    if(data.right.bgImage) {
        document.getElementById('right-bg').style.backgroundImage = `url('${data.right.bgImage}')`;
        const yOffset = data.right.bgOffsetY !== undefined ? data.right.bgOffsetY : 20;
        const zoom = data.right.bgZoom !== undefined ? data.right.bgZoom : 100;
        document.getElementById('right-bg').style.backgroundPosition = `center ${yOffset}%`;
        document.getElementById('right-bg').style.backgroundSize = zoom === 100 ? 'cover' : `${zoom}%`;
    } else {
        document.getElementById('right-bg').style.backgroundImage = 'none';
    }

    const rightLogo = document.getElementById('right-logo');
    if(data.right.logo && data.right.showLogo) {
        rightLogo.src = data.right.logo;
        rightLogo.style.display = 'block';
    } else {
        rightLogo.style.display = 'none';
    }

    document.getElementById('right-win-1').className = data.right.setWins >= 1 ? 'diamond filled' : 'diamond';
    document.getElementById('right-win-2').className = data.right.setWins >= 2 ? 'diamond filled' : 'diamond';
}

setInterval(updateOverlay, 500);
updateOverlay();