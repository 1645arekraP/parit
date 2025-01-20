const csrftoken = Cookies.get('csrftoken');
console.log(csrftoken)
document.addEventListener("visibilitychange", (event) => {
    if (document.visibilityState == "visible") {
        const xhr = new XMLHttpRequest();
        const data = JSON.stringify({ username: username});

        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
              const jsonData = JSON.parse(xhr.responseText);
              console.log(jsonData);
            }
        }
        xhr.open("POST", `${base_url}/account/update-solution/${username}/`, true);
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        xhr.send(data);
        console.log(`Sent request using ${data}`)
    }
  });

  