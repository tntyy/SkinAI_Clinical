let stream = null;
let cropper = null;

const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const image = document.getElementById("preview");

// bắt buộc để video tự phát trong Chrome mà không cần user gesture thêm lần nữa
video.muted = true;
video.setAttribute("playsinline", "");

async function startCamera() {

    console.log("[camera] Bấm Mở Camera...");

    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert("Trình duyệt không hỗ trợ camera.");
        console.error("[camera] navigator.mediaDevices.getUserMedia không tồn tại");
        return;
    }

    // nếu đang có stream cũ chưa tắt -> tắt trước khi mở lại, tránh xung đột
    if (stream) {
        console.log("[camera] Đang tắt stream cũ trước khi mở lại...");
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }

    try {

        console.log("[camera] Đang gọi getUserMedia...");

        stream = await navigator.mediaDevices.getUserMedia({ video: true });

        console.log("[camera] getUserMedia THÀNH CÔNG, tracks:", stream.getVideoTracks());

        video.srcObject = stream;

        video.onloadedmetadata = function () {
            console.log("[camera] video metadata loaded, kích thước:", video.videoWidth, "x", video.videoHeight);
        };

        try {
            await video.play();
            console.log("[camera] video.play() thành công");
        } catch (playErr) {
            console.error("[camera] video.play() bị lỗi:", playErr);
            alert("Không thể phát video camera: " + playErr.message);
        }

    } catch (err) {

        console.error("[camera] getUserMedia LỖI:", err.name, err.message);

        if (err.name === "NotAllowedError") {
            alert("Bạn đã từ chối quyền truy cập camera. Vui lòng cấp quyền trong trình duyệt và thử lại.");
        } else if (err.name === "NotFoundError") {
            alert("Không tìm thấy camera trên thiết bị này.");
        } else if (err.name === "NotReadableError") {
            alert("Camera đang bị chiếm dụng bởi ứng dụng/tab khác. Đóng app đó rồi thử lại.");
        } else {
            alert("Không thể mở camera: " + err.name + " - " + err.message);
        }
    }
}

function captureImage() {

    console.log("[camera] Bấm Chụp ảnh, video size hiện tại:", video.videoWidth, "x", video.videoHeight);

    if (!video.videoWidth || !video.videoHeight) {
        alert("Camera chưa sẵn sàng (chưa có hình). Vui lòng đợi camera hiện hình rồi mới bấm Chụp ảnh.");
        return;
    }

    const ctx = canvas.getContext("2d");

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    image.src = canvas.toDataURL("image/png");
    image.style.display = "block";

    document.getElementById("cropContainer").style.display = "block";

    image.onload = function () {

        if (cropper) {
            cropper.destroy();
        }

        cropper = new Cropper(image, {
            aspectRatio: 1,
            viewMode: 1,
            autoCropArea: 1,
            movable: true,
            zoomable: true,
            scalable: true,
            cropBoxResizable: true
        });
    };

    uploadBtn.style.display = "inline-block";
}

function stopCamera() {

    console.log("[camera] Tắt camera");

    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
        video.srcObject = null;
    }
}

const uploadBtn = document.getElementById("uploadCropBtn");

uploadBtn.onclick = function () {

    if (!cropper) {
        alert("Chưa có ảnh.");
        return;
    }

    cropper.getCroppedCanvas({ width: 224, height: 224 }).toBlob(function (blob) {

        const formData = new FormData();

        formData.append("image", blob, "capture.png");

        formData.append(
            "csrf_token",
            document.querySelector('input[name="csrf_token"]').value
        );

        fetch(window.location.pathname, { method: "POST", body: formData })
            .then(response => {

                if (response.ok) {
                    window.location.href = window.location.pathname.replace("/upload", "");
                } else {
                    alert("Upload thất bại");
                }

            })
            .catch(err => {
                console.error(err);
                alert("Có lỗi khi upload ảnh.");
            });

    });
};