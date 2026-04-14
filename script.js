async function findRoom() {
  const file = document.getElementById("file").files[0];
  const roll = document.getElementById("roll").value;
  const result = document.getElementById("result");

  if (!file || !roll) {
    result.innerText = "Upload file and enter roll number";
    return;
  }

  let formData = new FormData();
  formData.append("file", file);
  formData.append("roll", roll);

  result.innerText = "Processing...";

  try {
    const response = await fetch(https://exam-room-finder-7oow.onrender.com/find", {
      method: "POST",
      body: formData
    });

    const data = await response.json();
    result.innerText = data.result;

  } catch (error) {
    console.error(error);
    result.innerText = "Cannot connect to backend";
  }
}
