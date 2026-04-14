async function findRoom() {
const file = document.getElementById("file").files[0];
const roll = document.getElementById("roll").value.trim();
const result = document.getElementById("result");

// Validation
if (!file) {
result.innerText = "❗ Please upload a file";
return;
}

if (!roll) {
result.innerText = "❗ Please enter roll number";
return;
}

const formData = new FormData();
formData.append("file", file);
formData.append("roll", roll);

result.innerText = "⏳ Processing... (first time may take 30 sec)";

try {
const response = await fetch("https://exam-room-finder-7oow.onrender.com/find", {
method: "POST",
body: formData
});

```
if (!response.ok) {
  throw new Error("Server error");
}

const data = await response.json();

result.innerText = data.result || "⚠️ No response from server";
```

} catch (error) {
console.error(error);
result.innerText = "❌ Cannot connect to backend. Wait and try again.";
}
}
