// Wait until page loads
document.addEventListener("DOMContentLoaded", function(){

const form = document.getElementById("uploadForm");
const status = document.getElementById("status");

form.addEventListener("submit", function(e){

e.preventDefault();

let formData = new FormData();

let file = document.querySelector("input[name='file']").files[0];
let script = document.querySelector("textarea[name='script']").value;
let images = document.querySelector("input[name='images']").files;
let platform = document.querySelector("select[name='platform']").value;
let voice = document.querySelector("select[name='voice']").value;
let style = document.querySelector("select[name='style']").value;

/* Validation */

if(!file && script.trim()===""){
status.innerText = "Please upload a file or enter a script.";
return;
}

/* Add data */

if(file){
formData.append("file", file);
}

formData.append("script", script);
formData.append("platform", platform);
formData.append("voice", voice);
formData.append("style", style);

/* Multiple images */

for(let i=0;i<images.length;i++){
formData.append("images", images[i]);
}

/* Processing Animation */

status.innerHTML = "⏳ Generating AI video... Please wait";

let dots = 0;

let loading = setInterval(function(){

dots++;

if(dots>3){
dots=0;
}

status.innerHTML = "⏳ Generating AI video" + ".".repeat(dots);

},500);

/* Send to backend */

fetch("/upload",{

method:"POST",
body:formData

})

.then(response=>response.json())

.then(data=>{

clearInterval(loading);

if(data.success){

status.innerHTML =
"✅ Video Generated! <br><a href='"+data.video_url+"' target='_blank'>Download Video</a>";

}else{

status.innerText = "❌ Error: " + data.message;

}

})

.catch(error=>{

clearInterval(loading);

status.innerText = "❌ Error occurred while generating video.";

console.error(error);

});

});

});
