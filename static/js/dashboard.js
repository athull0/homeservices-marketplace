function loadCategories(){
    fetch('/website/get-categories/')//
    .then(response => response.json())
    .then(data => {
        let categoryContainer = document.getElementById('category-data');
        categoryContainer.innerHTML= "";
        data.categories.forEach(category => {
            categoryContainer.innerHTML += `
                    <div class="category-item">
                        <h3>${category.name}</h3>
                        <button onclick="editCategory(${category.id})">Edit</button>
                        <button onclick="deleteCategory(${category.id})">Delete</button>
                    </div>
                `;

        })
    })
    .catch(error => console.log("Error fetching categories:",error));
}



function showAddCategoryForm(){
    fetch('/website/addcat/')
    .then(response => response.text())
    .then(html => {
        console.log("Fetched HTML:", html);
        document.getElementById('category-data').innerHTML = "";
        document.getElementById('category-data').innerHTML = html;
        setupFormSubmission();
    })
    .catch(error => console.log('Error loading add category form:',error))
}
function setupFormSubmission(){
    document.getElementById('addcatform').addEventListener("submit",function(event){
        event.preventDefault();
        let formData = new FormData(this);
        fetch("/website/addcat/",{
            method:'POST',
            body:formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
                document.getElementById('category-data').innerHTML = "";
                loadCategories();
                
            } else{
                alert("Error adding category");
            }
            
        })
        .catch(error => console.log("Error submitting form:",error));
    });
}
function editCategory(categoryId){
    fetch(`/website/editcategory/${categoryId}/`) //
    .then(response => response.text())
    .then(html =>{
        document.getElementById('category-data').innerHTML = html;
        setupEditFormSubmission(categoryId);
    })
    .catch(error => console.log("Error loading edit form:", error));
}
function setupEditFormSubmission(categoryId) {
    document.getElementById('editcatform').addEventListener("submit", function(event) {
        event.preventDefault();  // Prevent default form submission

        let formData = new FormData(this);
        fetch(`/website/editcategory/${categoryId}/`, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
                loadCategories();  // Reload category list after update
            } else {
                alert("Error updating category");
            }
        })
        .catch(error => console.log("Error submitting form:", error));
    });
}
function deleteCategory(categoryId) {
    fetch(`/website/catdel/${categoryId}/`)
    .then(response => response.text())
    .then(html => {
        document.getElementById('category-data').innerHTML = html;
        setupDelete();  // Fixed function name
    });
}

function setupDelete() {
    document.getElementById('confirmDelete').addEventListener('click', function() {
        let categoryId = this.getAttribute('data-id');  // Fixed typo
        
        fetch(`/website/catdel/${categoryId}/`, {  // Fixed URL and method
            method: 'DELETE',
            headers: { 
                "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            window.location.reload();
        })
        .catch(error => console.log('Error:', error));
    });
}

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;  // Fixed CSRF token selection
}

function closeDeletePopup() {
    document.getElementById('category-data').innerHTML = "";
}

   
// function showAddCategoryForm() {
//     fetch('/website/addcat/')  // Fetching the form from Django
//     .then(response => response.text())  // Getting the HTML response
//     .then(data => {
//         let formContainer = document.getElementById('category-data');
//         formContainer.innerHTML = data;  // Placing the form inside the div
//         formContainer.style.display = 'block';  // Making it visible
//     })
//     .catch(error => console.log("Error loading form:", error));
// }
// function submitCategoryForm(event) {
//     event.preventDefault();  // Prevents page reload

//     let form = document.getElementById('addcatform');
//     let formData = new FormData(form);  // Collects form data

//     fetch('/website/addcat/', {
//         method: 'POST',
//         body: formData,
//         headers: {
//             'X-CSRFToken': getCookie('csrftoken')  // Adding CSRF token
//         }
//     })
//     .then(response => response.json())
//     .then(data => {
//         alert(data.message);  // Shows success message
//         document.getElementById('addcatform').style.display = 'none';  // Hides form
//         loadCategories();  // Reloads category list
//     })
//     .catch(error => console.log("Error submitting form:", error));
// }
