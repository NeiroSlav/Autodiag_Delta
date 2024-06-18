function onIgmpHover () {
    const button = document.getElementById('igmpButton');
    const hoverDiv = document.getElementById('igmpFullInfo');
    console.log(button);
    
    button.addEventListener('mouseover', () => {
        const rect = button.getBoundingClientRect();
        hoverDiv.style.top = `${rect.top + window.scrollY - 40}px`;
        hoverDiv.style.left = `${rect.left + window.scrollX - 30}px`;
        hoverDiv.classList.remove('hidden');
        setTimeout(function() {hoverDiv.style.opacity = 1;}, 10);
    });

    hoverDiv.addEventListener('mouseout', () => {
        hoverDiv.style.opacity = 0;
        setTimeout(function() {hoverDiv.classList.add('hidden');}, 300);
    });
}
