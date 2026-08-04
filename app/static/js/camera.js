let stream = null;
let cropper = null;

const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const image = document.getElementById("preview");

async function startCamera() {

    stream = await navigator.mediaDevices.getUserMedia({

        video: true

    });

    video.srcObject = stream;

}

function captureImage() {

    const ctx = canvas.getContext("2d");

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    ctx.drawImage(
        video,
        0,
        0,
        canvas.width,
        canvas.height
    );

    image.src = canvas.toDataURL("image/png");

    image.style.display = "block";

    document.getElementById("cropContainer").style.display = "block";

    image.onload = function(){

        if(cropper){

            cropper.destroy();

        }

        cropper = new Cropper(image,{

            aspectRatio:1,

            viewMode:1,

            autoCropArea:1,

            movable:true,

            zoomable:true,

            scalable:true,

            cropBoxResizable:true

        });
    
    }

    uploadBtn.style.display="inline-block";

}



function stopCamera(){

    if(stream){

        stream.getTracks().forEach(track=>track.stop());

    }

}


const uploadBtn = document.getElementById("uploadCropBtn");

uploadBtn.onclick = function () {

    if(!cropper){

        alert("Chưa có ảnh.");

        return;

    }

    cropper.getCroppedCanvas({

        width:224,
        height:224

    }).toBlob(function(blob){

        const formData = new FormData();

        formData.append(
            "image",
            blob,
            "capture.png"
        );

        formData.append(
            "csrf_token",
            document.querySelector(
                'input[name="csrf_token"]'
            ).value
        );

        fetch(window.location.pathname,{
            method:"POST",
            body:formData
        })
        .then(response=>{

            if(response.ok){

                window.location.href =
                window.location.pathname.replace(
                    "/upload",
                    ""
                );

            }else{

                alert("Upload thất bại");

            }

        });

    });

};