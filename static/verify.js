document.addEventListener("DOMContentLoaded", () => {
    document.getElementById('cardForm').addEventListener('submit', function(event) {
      const name = document.getElementById('name').value();
      const type = document.getElementById('type').value();
      const rarity = document.getElementById('rarity').value();
      const image = document.getElementById('image').value();
      if (!name || !type || !rarity || !image) {
        alert("All fields are required!");
        event.preventDefault();
      }
    });
  });