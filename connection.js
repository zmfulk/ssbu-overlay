const DATA_FILE = 'data.json';
let previousDataString = "";

async function updateOverlay() {
    try {
        const response = await fetch(`${DATA_FILE}?t=${new Date().getTime()}`);
        if (!response.ok) return;

        const data = await response.json();
        const currentDataString = JSON.stringify(data);

        if (currentDataString !== previousDataString) {
            
            // --- Update Left Player ---
            const leftTeamEl = document.getElementById('left-team');
            leftTeamEl.textContent = data.left.team;
            
            // Apply color to Left Team Name and Left Score Box
            if(data.left.color) {
                leftTeamEl.style.color = data.left.color;
                document.querySelector('.left-score-box').style.color = data.left.color;
            }

            document.getElementById('left-name').textContent = data.left.name;
            document.getElementById('left-score').textContent = data.left.score;
            
            if(data.left.bgImage) {
                document.getElementById('left-bg').style.backgroundImage = `url('${data.left.bgImage}')`;
            } else {
                document.getElementById('left-bg').style.backgroundImage = 'none';
            }

            const leftLogo = document.getElementById('left-logo');
            if(data.left.logo) {
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
            
            // Apply color to Right Team Name and Right Score Box
            if(data.right.color) {
                rightTeamEl.style.color = data.right.color;
                document.querySelector('.right-score-box').style.color = data.right.color;
            }

            document.getElementById('right-name').textContent = data.right.name;
            document.getElementById('right-score').textContent = data.right.score;
            
            if(data.right.bgImage) {
                document.getElementById('right-bg').style.backgroundImage = `url('${data.right.bgImage}')`;
            } else {
                document.getElementById('right-bg').style.backgroundImage = 'none';
            }

            const rightLogo = document.getElementById('right-logo');
            if(data.right.logo) {
                rightLogo.src = data.right.logo;
                rightLogo.style.display = 'block';
            } else {
                rightLogo.style.display = 'none';
            }

            document.getElementById('right-win-1').className = data.right.setWins >= 1 ? 'diamond filled' : 'diamond';
            document.getElementById('right-win-2').className = data.right.setWins >= 2 ? 'diamond filled' : 'diamond';

            previousDataString = currentDataString;
        }

    } catch (error) {
        console.error("Error fetching data.json: ", error);
    }
}

setInterval(updateOverlay, 500);
updateOverlay();