window.onload = function () {
        var textForm = document.getElementById("memeForm");
        var container = document.getElementById("memes-container");
        textForm.addEventListener("submit", function (event) {
        event.preventDefault();
        var url = document.getElementById('MemeImage').value;
        var div = document.createElement('div');
        var img = document.createElement('img');
        div.className="meme";
        img.src = url;
        img.setAttribute("width", "400");
        img.setAttribute("height", "400");
        if(url.length ===0) return alert ("Please add an image URL");


        const deleteIcon = document.createElement('img');
        const deleteButton = document.createElement('button');
        deleteButton.className = 'delete';
            deleteIcon.setAttribute("src", "https://s3.us-east-2.amazonaws.com/upload-icon/uploads/icons/png/14965250021536572523-256.png");



        var meme = document.createElement("div");
        meme.className = "wrapper";
        var topText = document.createElement("div");
        topText.setAttribute("id","top");
        topText.innerText = document.getElementById("upper_text").value.toUpperCase();



        var botText = document.createElement("div");
        botText.setAttribute("id","bot");
        botText.innerText = document.getElementById("lower_text").value.toUpperCase();

        deleteButton.append(deleteIcon);
        meme.append(topText, botText,deleteButton);
        div.append(meme, img);
        container.append(div);
        textForm.reset();

        })
    container.addEventListener("click", function (event) {
        const btns = document.querySelectorAll('.delete');
        for (var btn of btns) {

            if (event.target.parentElement === btn) {
                event.target.parentElement.parentElement.parentElement.remove();
            }
        }
    });
}
