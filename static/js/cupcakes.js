$list = $("#cupcakes-list");

const addCupcake = (cupcake) => {
    // add to the list
    $list.append(
    `<div class="col">
        <div class="card w-50">
            <img src="${cupcake.image}" class="card-img-top" alt="${cupcake.flavor}-flavored-cupcake-image">
            <div class="card-body">
                <h5 class="card-title">${cupcake.flavor}</h5>
                <p class="card-text">Size: ${cupcake.size}</p>
                <p class="card-text"><small class="text-body-secondary">Rating: ${cupcake.rating}</small></p>  
                <button class="btn btn-danger" id="delete-cupcake-${cupcake.id}">Delete</button>
            </div>
        </div>
    </div>`
    );
    $deleteBtn = $(`#delete-cupcake-${cupcake.id}`);
    $deleteBtn.on("click", async function () {
        await axios.delete(`/api/cupcakes/${cupcake.id}`);
        $(this).parent().parent().parent().remove();
    });
};

async function showCupcakes() {
    const response = await axios.get("/api/cupcakes");
    for (let cupcake of response.data.cupcakes) {
        addCupcake(cupcake);
    }
}

$form = $("#new-cupcake-form");
$form.on("submit", async function (evt) {
    evt.preventDefault();

    let flavor = $("#flavor").val();
    let size = $("#size").val();
    let rating = $("#rating").val();
    let image = $("#image").val();

    [flavor, size, rating, image].forEach((val) => {
        if (!val) {
            alert("Please fill out all fields.");
            return;
        }
    });

    const newCupcake = {
        flavor,
        size,
        rating,
        image,
    };

    const response = await axios.post("/api/cupcakes", newCupcake);
    addCupcake(response.data.cupcake);
    $form.trigger("reset");
});

showCupcakes();
