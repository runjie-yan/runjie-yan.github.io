function select_sample(selectElement) {
    const selectedValue = selectElement.value;

    // Define the paths for each method
    const paths = {
        "VSD": `./assets/videos/samples/vsd/${selectedValue}.mp4`,
        "CFD": `./assets/videos/samples/cfd/${selectedValue}.mp4`
    };

    // Update the source of each video element
    document.querySelector("#sect-2-sample-0 source").src = paths["VSD"];
    document.querySelector("#sect-2-sample-2 source").src = paths["CFD"];

    // Reload the video elements to reflect the new sources
    document.getElementById("sect-2-sample-0").load();
    document.getElementById("sect-2-sample-2").load();

    // Update the description
    document.getElementById("sect-2-prompt").innerText = getPrompt(selectedValue);
}

// Function to return description based on selected sample
function getPrompt(selectedValue) {
    const prompts = {
        "stone_castle": "A highly detailed DSLR photo of a 3d model of historical stone castle",
        "cottage": "A zoomed out DSLR photo of 3d model of an adorable cottage with a thatched roof, high resolution, sharp",
        "cheesecake_castle": "A Matte painting of a castle made of cheesecake surrounded by a moat made of ice cream",
        "victorian_house": "A detailed photo of a 3d model of classic Victorian house, high resolution, sharp",
        "icecream": "A DSLR photo of an ice cream sundae",
        "tower": "A high-resolution image of a 3d model of traditional Japanese pagoda",
        "chair": "A wooden chair, detailed, high resolution, high quality, sharp",
        "strawberry": "A ripe strawberry",
        "pineapple": "A pineapple, detailed, high resolution, high quality, sharp",
        "rose": "A close-up photo of a single red rose",
        "chest": "A DSLR photo of 3D model of a treasure chest full of gold coins and jewels, high resolution, sharp",
    };

    return prompts[selectedValue] || "Description not available.";
}
