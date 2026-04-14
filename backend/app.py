async function findRoom() {
const fileInput = document.getElementById("file");
const rollInput = document.getElementById("roll");
const result = document.getElementById("result");

const file = fileInput.files[0];
const roll = rollInput.value.trim();

// Validation
if (!file) {
result.innerText = "❗ Please upload a file";
return;
}

if (!roll) {
result.innerText = "❗ Please enter roll number";
return;
}

let formData = new FormData();
formData.append("file", file);
formData.append("roll", roll);

result.innerText = "⏳ Processing... Please wait";

try {
const response = await fetch("https://exam-room-finder-7oow.onrender.com/find", {
method: "POST",
body: formData
});

```
// Handle server errors
if (!response.ok) {
  throw new Error("Server error");
}

const data = await response.json();

if (data.result) {
  result.innerText = data.result;
} else {
  result.innerText = "⚠️ Unexpected response from server";
}
```

} catch (error) {
console.error("Error:", error);
result.innerText = "❌ Cannot connect to backend. Try again in a few seconds.";
}
}
