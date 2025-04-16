function switchGeneration(gen) {
    const imageContainer = document.getElementById('pokemon-images');
    const images = imageContainer.getElementsByTagName('img');

    let startId = 0;
    if (gen === 1) startId = 1;
    else if (gen === 2) startId = 152;
    else if (gen === 3) startId = 252;
    else if (gen === 4) startId = 387;
    else if (gen === 5) startId = 494;
    else if (gen === 6) startId = 650;
    else if (gen === 7) startId = 722;

    for (let i = 0; i < images.length; i++) {
        const pokeId = startId + i;
        images[i].src = `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${pokeId}.png`;
    }
}